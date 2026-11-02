"""Offline, deterministic regression tests; no real proxy/service/GitHub writes.
Run with the dedicated venv (HF parser needs pyarrow; missing pyarrow FAILS, never skips):
  /root/.venvs/arena/bin/python -m unittest discover -s tests -p 'test_lmarena.py' -v
"""
import copy
import gzip
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / 'tests/fixtures/lmarena'
spec = importlib.util.spec_from_file_location('arena_parser', ROOT / 'scripts/parse-lmarena.py')
parser = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parser)
RAW = gzip.decompress((FIXTURE / 'text-2026-10-11.html.gz').read_bytes())
META = json.loads((FIXTURE / 'text-2026-10-11.fetch.json').read_text())
BOARD = parser.extract_leaderboard(RAW.decode())


def synthetic(board):
    flight = 'a:' + json.dumps(['$', 'test', None, {'leaderboard': board}]) + '\n'
    # Split across push calls to exercise Flight stream concatenation.
    parts = [flight[:130], flight[130:]]
    raw = ('<html>' + ''.join('<script>self.__next_f.push(' + json.dumps([1, p]) + ')</script>'
                             for p in parts) + '</html>').encode()
    meta = dict(META, sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw))
    return raw, meta


class ParserTests(unittest.TestCase):
    def test_real_official_capture(self):
        snapshot = parser.build_snapshot(RAW, META)
        candidate = json.loads((ROOT/'state/lmarena-candidates/2026-10-11.json').read_text())
        self.assertEqual(snapshot, candidate)
        self.assertEqual(snapshot['totalModelsObserved'], 414)
        self.assertEqual(snapshot['totalModelsShown'], 50)
        self.assertEqual(snapshot['sourceUpdatedAt'], '2026-10-08T14:00:00.000Z')
        self.assertEqual(snapshot['snapshotDate'], '2026-10-11')
        self.assertEqual(snapshot['models'][0]['name'], 'gemini-4-argon-high')
        self.assertEqual(snapshot['models'][0]['rating'], BOARD['entries'][0]['rating'])
        self.assertEqual(snapshot['categoryLabels'], {'overall': '文本综合'})
        self.assertTrue(all(not m['highlight'] for m in snapshot['models']))

    def test_small_valid_structured_payload_not_size_gate(self):
        raw, meta = synthetic(BOARD)
        self.assertLess(len(raw), 1000000)
        self.assertEqual(parser.build_snapshot(raw, meta)['totalModelsObserved'], 414)

    def test_empty_shell_and_non_rsc(self):
        for raw in (b'<html>HTTP 200 app shell</html>', b'', b'{}'):
            with self.subTest(raw=raw), self.assertRaises(parser.InvalidSource):
                parser.build_snapshot(raw, dict(META, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest()))

    def test_metadata_failure(self):
        for changes in ({'curlExitCode': 28}, {'httpStatus': 403}, {'sha256': '0'*64}, {'bytes': 0},
                        {'effectiveUrl': 'https://example.org'}, {'fetchedAt': '2026-10-11'},
                        {'fetchedAt': '2026-10-01T10:30:00+08:00'},
                        {'fetchedAt': '2026-12-01T10:30:00+08:00'}):
            with self.subTest(changes=changes), self.assertRaises(parser.InvalidSource):
                parser.build_snapshot(RAW, dict(META, **changes))

    def test_missing_fields(self):
        for field in ('entries', 'params', 'id', 'totalModels', 'totalVotes', 'leaderboardSlug'):
            board = copy.deepcopy(BOARD)
            del board[field]
            with self.subTest(field=field), self.assertRaises(parser.InvalidSource):
                parser.build_snapshot(*synthetic(board))
        for field in ('modelDisplayName', 'modelKey', 'modelOrganization', 'rank', 'rating',
                      'votes', 'rankUpper', 'rankLower', 'ratingLower', 'ratingUpper'):
            board = copy.deepcopy(BOARD)
            del board['entries'][0][field]
            with self.subTest(field=field), self.assertRaises(parser.InvalidSource):
                parser.build_snapshot(*synthetic(board))

    def test_zero_partial_and_wrong_basis(self):
        for changes in ({'entries': []}, {'entries': BOARD['entries'][:50]},
                        {'totalModels': 0}, {'params': {'category': 'overall', 'styleControl': False}},
                        {'arenaSlug': 'image'}):
            with self.subTest(changes=list(changes)), self.assertRaises(parser.InvalidSource):
                parser.build_snapshot(*synthetic(dict(BOARD, **changes)))

    def test_invalid_rank_rating_votes(self):
        for field, value in (('rank', 0), ('rank', True), ('rank', 2), ('rank', 999),
                             ('rating', float('nan')), ('rating', float('inf')), ('rating', -1),
                             ('ratingLower', 9000), ('rankUpper', 2), ('votes', 0),
                             ('modelDisplayName', '')):
            board = copy.deepcopy(BOARD)
            board['entries'][0][field] = value
            with self.subTest(field=field, value=value), self.assertRaises(parser.InvalidSource):
                parser.build_snapshot(*synthetic(board))
        board = copy.deepcopy(BOARD)
        # Valid individual intervals but order contradicts rank.
        for field in ('rating', 'ratingLower', 'ratingUpper'):
            board['entries'][1][field] += 100
        with self.assertRaises(parser.InvalidSource):
            parser.build_snapshot(*synthetic(board))

    def test_dedup_and_conflicts(self):
        board = copy.deepcopy(BOARD)
        board['entries'].append(copy.deepcopy(board['entries'][0]))
        self.assertEqual(parser.build_snapshot(*synthetic(board))['totalModelsObserved'], 414)
        board['entries'][-1]['votes'] += 1
        with self.assertRaises(parser.InvalidSource):
            parser.build_snapshot(*synthetic(board))
        board = copy.deepcopy(BOARD)
        board['entries'][1]['modelDisplayName'] = board['entries'][0]['modelDisplayName']
        with self.assertRaises(parser.InvalidSource):
            parser.build_snapshot(*synthetic(board))

    def test_unknown_source_time_is_explicit(self):
        board = copy.deepcopy(BOARD)
        del board['voteCutoffISOString']
        result = parser.build_snapshot(*synthetic(board))
        self.assertIsNone(result['sourceUpdatedAt'])
        self.assertEqual(result['sourceTimeMeaning'], 'unknown')
        self.assertIn('不能确认', result['sourceTimeNote'])

    def test_cli_does_not_replace_output_on_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            raw = b'<html>empty</html>'
            (tmp/'source.html').write_bytes(raw)
            (tmp/'meta.json').write_text(json.dumps(dict(META, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())))
            output = tmp/'output.json'
            cmd = ['python3', str(ROOT/'scripts/parse-lmarena.py'), str(tmp/'source.html'), str(tmp/'meta.json'), str(output)]
            self.assertNotEqual(subprocess.run(cmd, capture_output=True).returncode, 0)
            self.assertFalse(output.exists())
            output.write_text('previous candidate')
            self.assertNotEqual(subprocess.run(cmd, capture_output=True).returncode, 0)
            self.assertEqual(output.read_text(), 'previous candidate')
            self.assertEqual((tmp/'source.html').read_bytes(), raw)


# ---- HF parquet path (default since 2026-11) -------------------------------
import pyarrow as pa  # noqa: E402  (hard dependency: ImportError fails the suite, no skip)
import pyarrow.parquet as pq  # noqa: E402

hf_spec = importlib.util.spec_from_file_location('arena_hf_parser', ROOT / 'scripts/parse-lmarena-hf.py')
hf = importlib.util.module_from_spec(hf_spec)
hf_spec.loader.exec_module(hf)
HF_RAW = (FIXTURE / 'hf-text-style-control-2026-11-02.parquet').read_bytes()
HF_META = json.loads((FIXTURE / 'hf-text-style-control-2026-11-02.fetch.json').read_text())
HF_TABLE = pq.read_table(pa.BufferReader(HF_RAW))
HF_ROWS = HF_TABLE.to_pylist()
HF_OVERALL = sorted((r for r in HF_ROWS if r['category'] == 'overall'), key=lambda r: r['rank'])


def hf_bytes(rows, schema=None):
    sink = io.BytesIO()
    pq.write_table(pa.Table.from_pylist(rows, schema=schema or HF_TABLE.schema), sink)
    return sink.getvalue()


def hf_synthetic(rows, schema=None, **meta_changes):
    raw = hf_bytes(rows, schema)
    meta = dict(HF_META, sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw),
                hubLinkedEtag=hashlib.sha256(raw).hexdigest(), hubLinkedSize=len(raw))
    meta.update(meta_changes)
    return raw, meta


def today_str():
    # Same clock/zone as fetch-lmarena.sh's capture timestamp.
    return subprocess.run(['date', '+%Y-%m-%d'], env=dict(os.environ, TZ='Asia/Shanghai'),
                          capture_output=True, text=True, check=True).stdout.strip()


def overall_copy():
    return copy.deepcopy(HF_OVERALL)


class HFParserTests(unittest.TestCase):
    def test_real_hf_capture(self):
        self.assertEqual(hashlib.sha256(HF_RAW).hexdigest(), HF_META['sha256'])
        snapshot = hf.build_snapshot(HF_RAW, HF_META)
        candidate = json.loads((ROOT/'state/lmarena-candidates/2026-11-02.json').read_text())
        self.assertEqual(snapshot, candidate)
        self.assertEqual(snapshot['totalModelsObserved'], 419)
        self.assertEqual(snapshot['totalModelsShown'], 50)
        self.assertEqual(snapshot['sourceUpdatedAt'], '2026-10-28')
        self.assertEqual(snapshot['sourceTimeMeaning'], 'leaderboard publish date')
        self.assertEqual(snapshot['snapshotDate'], '2026-11-02')
        self.assertEqual([m['name'] for m in snapshot['models'][:3]],
                         ['Gemini 4 Carbon (High)', 'Gemini 4 Argon (High)', 'Claude Opus 5.5 (High)'])
        self.assertIsNone(snapshot['sourceTotalVotes'])
        self.assertTrue(all(m['modelKey'] is None and m['rankUpper'] is None for m in snapshot['models']))
        self.assertEqual(snapshot['unmappedOrganizations'], [])
        self.assertNotIn('未披露', {m['org'] for m in snapshot['models']})
        self.assertTrue(all(type(m['votes']) is int for m in snapshot['models']))
        # Multi-category shard: only 'overall' is used.
        self.assertGreater(len(HF_ROWS), 10 * len(HF_OVERALL))

    def test_same_statistics_as_arena_page_on_shared_publish(self):
        """HF 2026-10-08 publish == arena.ai capture with voteCutoff 2026-10-08, row-for-row."""
        rows = pq.read_table(FIXTURE/'hf-full-overall-2026-10-08.derived.parquet').to_pylist()
        web = sorted(BOARD['entries'], key=lambda e: e['rank'])
        self.assertEqual(len(rows), len(web))
        for row, entry in zip(sorted(rows, key=lambda r: r['rank']), web):
            self.assertEqual((row['model_name'], row['rank'], row['rating'], row['rating_lower'],
                              row['rating_upper'], int(row['vote_count'])),
                             (entry['modelDisplayName'], entry['rank'], entry['rating'],
                              entry['ratingLower'], entry['ratingUpper'], entry['votes']))
            self.assertEqual(hf.ORG_DISPLAY.get(row['organization'], row['organization']),
                             entry['modelOrganization'])
        # And the whole v2 pipeline accepts it (capture date inside the 45-day window).
        result = hf.build_snapshot(*hf_synthetic(rows, fetchedAt='2026-10-11T23:41:46+08:00'))
        expected = parser.build_snapshot(RAW, META)
        for new, old in zip(result['models'], expected['models']):
            for key in ('rank', 'name', 'org', 'rating', 'ratingLower', 'ratingUpper', 'votes'):
                self.assertEqual(new[key], old[key], key)

    def test_non_parquet_bodies(self):
        for raw in (b'', b'<html>Just a moment...</html>', b'PAR1garbagePAR1', b'{"error":"x"}'):
            with self.subTest(raw=raw[:20]), self.assertRaises(hf.InvalidSource):
                hf.build_snapshot(raw, dict(HF_META, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest(),
                                            hubLinkedEtag=None, hubLinkedSize=None))

    def test_metadata_failure(self):
        for changes in ({'curlExitCode': 28}, {'httpStatus': 403}, {'sha256': '0'*64}, {'bytes': 1},
                        {'hubLinkedEtag': '1'*64}, {'hubLinkedSize': 5}, {'hubRepoCommit': 'main'},
                        {'sourceKind': None}, {'sourceUrl': hf.SOURCE_URL.replace('text_style_control', 'text')},
                        {'effectiveUrl': 'https://evil.example/x.parquet'},
                        {'effectiveUrl': 'http://us.aws.cdn.hf.co/x'},
                        {'effectiveUrl': 'https://huggingface.co.evil.example/x'},
                        {'fetchedAt': '2026-11-02'},
                        {'fetchedAt': '2026-10-27T23:00:00+08:00'},   # publish date in the future
                        {'fetchedAt': '2026-12-13T10:30:00+08:00'}):  # > 45 days old
            with self.subTest(changes=changes), self.assertRaises(hf.InvalidSource):
                hf.build_snapshot(HF_RAW, dict(HF_META, **changes))
        # Boundaries that must pass: same day, exactly 45 days, Hub headers absent.
        for changes in ({'fetchedAt': '2026-10-28T00:00:00+08:00'},
                        {'fetchedAt': '2026-12-12T23:59:59+08:00'},
                        {'hubLinkedEtag': None, 'hubLinkedSize': None, 'hubRepoCommit': None},
                        {'effectiveUrl': hf.SOURCE_URL}):
            with self.subTest(ok=changes):
                hf.build_snapshot(HF_RAW, dict(HF_META, **changes))

    def test_missing_or_retyped_columns(self):
        for column in hf.REQUIRED_COLUMNS:
            table = HF_TABLE.drop_columns([column])
            with self.subTest(drop=column), self.assertRaises(hf.InvalidSource):
                hf.build_snapshot(*hf_synthetic(table.to_pylist(), table.schema))
        schema = HF_TABLE.schema.set(HF_TABLE.schema.get_field_index('rank'), pa.field('rank', pa.float64()))
        with self.assertRaises(hf.InvalidSource):
            hf.build_snapshot(*hf_synthetic(HF_OVERALL, schema))

    def test_model_count_and_category(self):
        for rows in ([], HF_OVERALL[:99], [dict(r, category='english') for r in HF_OVERALL]):
            with self.subTest(n=len(rows)), self.assertRaises(hf.InvalidSource):
                hf.build_snapshot(*hf_synthetic(rows))
        # Exactly 100 contiguous ranks is accepted; other categories are ignored.
        noise = [dict(r, category='coding', rank=999) for r in HF_OVERALL[:5]]
        self.assertEqual(hf.build_snapshot(*hf_synthetic(HF_OVERALL[:100] + noise))['totalModelsObserved'], 100)

    def test_invalid_rows(self):
        cases = (('rank', 0), ('rank', 3), ('rank', 999), ('rank', None),
                 ('rating', float('nan')), ('rating', float('inf')), ('rating', -1.0), ('rating', None),
                 ('rating_lower', 9000.0), ('rating_upper', 1.0),
                 ('vote_count', 0.0), ('vote_count', 1.5), ('vote_count', float('nan')), ('vote_count', None),
                 ('model_name', ''), ('model_name', '  '), ('model_name', None),
                 ('organization', None), ('leaderboard_publish_date', None),
                 ('leaderboard_publish_date', '2026-13-01'), ('leaderboard_publish_date', '20261028'),
                 ('leaderboard_publish_date', '2026-10-27'))  # mixed publish dates
        for field, value in cases:
            rows = overall_copy()
            rows[1][field] = value
            with self.subTest(field=field, value=value), self.assertRaises(hf.InvalidSource):
                hf.build_snapshot(*hf_synthetic(rows))

    def test_rank_rating_consistency_and_duplicates(self):
        rows = overall_copy()
        for field in ('rating', 'rating_lower', 'rating_upper'):
            rows[1][field] += 100  # each interval valid, order contradicts rank
        with self.assertRaises(hf.InvalidSource):
            hf.build_snapshot(*hf_synthetic(rows))
        rows = overall_copy()
        rows[1]['model_name'] = rows[0]['model_name']
        with self.assertRaises(hf.InvalidSource):
            hf.build_snapshot(*hf_synthetic(rows))
        rows = overall_copy() + [copy.deepcopy(HF_OVERALL[0])]  # exact duplicate row also rejected
        with self.assertRaises(hf.InvalidSource):
            hf.build_snapshot(*hf_synthetic(rows))
        rows = overall_copy()
        rows[1]['rank'] = 1  # tie: needs human adaptation, never silently re-ranked
        with self.assertRaises(hf.InvalidSource):
            hf.build_snapshot(*hf_synthetic(rows))
        # Equal ratings with distinct ranks remain monotone and are accepted.
        rows = overall_copy()
        rows[1].update(rating=rows[0]['rating'], rating_lower=rows[0]['rating_lower'] - 1,
                       rating_upper=rows[0]['rating_upper'] + 1)
        hf.build_snapshot(*hf_synthetic(rows))

    def test_organization_mapping_is_not_guessed(self):
        rows = overall_copy()
        rows[0]['organization'] = ''
        rows[1]['organization'] = 'brand-new-lab'
        result = hf.build_snapshot(*hf_synthetic(rows))
        self.assertEqual(result['models'][0]['org'], '未披露')
        self.assertIsNone(result['models'][0]['orgId'])
        self.assertEqual(result['models'][1]['org'], 'brand-new-lab')
        self.assertEqual(result['unmappedOrganizations'], ['brand-new-lab'])

    def test_missing_pyarrow_is_explicit_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp/'pyarrow').mkdir()
            (tmp/'pyarrow/__init__.py').write_text('raise ImportError("simulated missing pyarrow")\n')
            (tmp/'source.parquet').write_bytes(HF_RAW)
            (tmp/'meta.json').write_text(json.dumps(HF_META))
            cmd = [sys.executable, str(ROOT/'scripts/parse-lmarena-hf.py'),
                   str(tmp/'source.parquet'), str(tmp/'meta.json'), str(tmp/'out.json')]
            result = subprocess.run(cmd, capture_output=True, text=True, env=dict(os.environ, PYTHONPATH=str(tmp)))
            self.assertEqual(result.returncode, 3, result.stderr)
            self.assertIn('pyarrow', result.stderr)
            self.assertFalse((tmp/'out.json').exists())

    def test_cli_atomic_and_preserves_raw(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            raw = b'<html>cf challenge</html>'
            (tmp/'source.parquet').write_bytes(raw)
            (tmp/'meta.json').write_text(json.dumps(dict(HF_META, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest(),
                                                         hubLinkedEtag=None, hubLinkedSize=None)))
            output = tmp/'output.json'
            cmd = [sys.executable, str(ROOT/'scripts/parse-lmarena-hf.py'), str(tmp/'source.parquet'),
                   str(tmp/'meta.json'), str(output)]
            self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 2)
            self.assertFalse(output.exists())
            output.write_text('previous candidate')
            self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 2)
            self.assertEqual(output.read_text(), 'previous candidate')
            self.assertEqual((tmp/'source.parquet').read_bytes(), raw)
            self.assertFalse((tmp/'output.json.tmp').exists())


class ShellTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.repo = self.base/'repo'
        (self.repo/'scripts').mkdir(parents=True)
        (self.repo/'src/data/lmarena/snapshots').mkdir(parents=True)
        for name in ('fetch-lmarena.sh', 'parse-lmarena.py', 'parse-lmarena-hf.py'):
            shutil.copyfile(ROOT/'scripts'/name, self.repo/'scripts'/name)
        # In the sandbox only, keep mock executables ahead of the host's pnpm
        # and use a private publish lock. Production script is not altered.
        script = self.repo/'scripts/fetch-lmarena.sh'
        script.write_text(script.read_text().replace(
            'export PATH="/root/.nvm/versions/node/v22.22.2/bin:$PATH"',
            'export PATH="$PATH"').replace('/tmp/ai-daily-publish.lock', str(self.base/'publish.lock')))
        (self.repo/'.gitignore').write_text('.cron-logs/\n')
        self.bin = self.base/'bin'
        self.bin.mkdir()
        self.log = self.base/'commands.log'
        self.real_git = shutil.which('git')
        self.real_python = shutil.which('python3')
        self.env = dict(os.environ, PATH=str(self.bin)+':'+os.environ['PATH'],
                        MOCK_LOG=str(self.log), MOCK_RAW=str(self.base/'source.html'),
                        REAL_GIT=self.real_git, REAL_PYTHON=self.real_python,
                        # The test interpreter is the pyarrow venv; mirrors production ARENA_PYTHON.
                        ARENA_PYTHON=sys.executable)
        (self.base/'source.html').write_bytes(RAW)
        self.stub('python3', '''if [[ "$1" == - ]]; then
  script=$(cat)
  if [[ "$script" == *socket.create_connection* ]]; then
    echo proxy-check >> "$MOCK_LOG"
    exit "${MOCK_PROXY_FAIL:-0}"
  fi
  printf '%s' "$script" | "$REAL_PYTHON" "$@"
else exec "$REAL_PYTHON" "$@"; fi''')
        self.stub('curl', '''echo curl >> "$MOCK_LOG"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --output) cp "$MOCK_RAW" "$2"; shift 2;;
    --dump-header)
      if [[ -n "${MOCK_HEADERS:-}" ]]; then cp "$MOCK_HEADERS" "$2"; else echo 'HTTP/2 200' > "$2"; fi
      shift 2;;
    *) shift;;
  esac
done
printf '%s\\n%s\\n' "${MOCK_HTTP:-200}" "${MOCK_EFFECTIVE:-https://arena.ai/leaderboard/chat/text}"
exit "${MOCK_CURL_FAIL:-0}"''')
        self.stub('git', '''echo "git $*" >> "$MOCK_LOG"
if [[ "$*" == *'push origin main'* ]]; then exit "${MOCK_PUSH_FAIL:-0}"; fi
exec "$REAL_GIT" "$@"''')
        self.stub('pnpm', 'echo pnpm >> "$MOCK_LOG"; exit "${MOCK_BUILD_FAIL:-0}"')
        self.stub('sleep', 'echo sleep >> "$MOCK_LOG"')
        for forbidden in ('pkill', 'mihomo', 'nohup'):
            self.stub(forbidden, f'echo FORBIDDEN-{forbidden} >> "$MOCK_LOG"; exit 99')
        subprocess.run([self.real_git, 'init', '-b', 'main', str(self.repo)], check=True, capture_output=True)
        self.git('config', 'user.email', 'test@example.invalid')
        self.git('config', 'user.name', 'Arena Offline Test')
        self.git('add', '.')
        self.git('commit', '-m', 'test fixture')

    def tearDown(self):
        if self.log.exists():
            self.assertNotIn('FORBIDDEN', self.log.read_text())
        self.tmp.cleanup()

    def stub(self, name, script):
        file = self.bin/name
        file.write_text('#!/usr/bin/env bash\nset -eu\n'+script+'\n')
        file.chmod(0o755)

    def git(self, *args):
        return subprocess.run([self.real_git, '-C', str(self.repo), *args], check=True, capture_output=True, text=True)

    def run_script(self, *args, **env):
        return subprocess.run(['bash', str(self.repo/'scripts/fetch-lmarena.sh'), *map(str, args)],
                              env=dict(self.env, **env), capture_output=True, text=True)

    def status(self):
        return json.loads((self.repo/'.cron-logs/lmarena/latest-status.json').read_text())

    def prepared(self):
        # Fixed-time replay prevents test dependence on today's date.
        run = self.repo/'.cron-logs/lmarena/offline'
        run.mkdir(parents=True)
        (run/'source.html').write_bytes(RAW)
        (run/'fetch.json').write_text(json.dumps(META))
        result = self.run_script('parse', run)
        self.assertEqual(result.returncode, 0, result.stderr)
        sha = hashlib.sha256((run/'candidate.json').read_bytes()).hexdigest()
        return run, sha

    def test_fetch_default_never_publishes(self):
        # Use source without a cutoff here: production timestamps advance, fixture doesn't.
        board = copy.deepcopy(BOARD)
        del board['voteCutoffISOString']
        (self.base/'source.html').write_bytes(synthetic(board)[0])
        result = self.run_script('fetch')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.status()['status'], 'candidate_ready')
        self.assertFalse(self.status()['notificationDelivered'])
        self.assertNotIn('git ', self.log.read_text())
        self.assertNotIn('pnpm', self.log.read_text())
        self.assertEqual(list((self.repo/'src/data/lmarena/snapshots').glob('*.json')), [])

    def test_http_200_shell_preserved_and_nonzero(self):
        (self.base/'source.html').write_text('<html>empty shell</html>')
        result = self.run_script('fetch')
        self.assertNotEqual(result.returncode, 0)
        status = self.status()
        self.assertEqual(status['status'], 'failed')
        run = Path(status['runDir'])
        self.assertTrue((run/'source.html').exists())
        self.assertFalse((run/'candidate.json').exists())

    def test_http_200_missing_field_and_zero_models(self):
        for change in ('missing-rating', 'zero-models'):
            board = copy.deepcopy(BOARD)
            if change == 'missing-rating':
                del board['entries'][0]['rating']
            else:
                board['entries'] = []
                board['totalModels'] = 0
            (self.base/'source.html').write_bytes(synthetic(board)[0])
            result = self.run_script('fetch')
            self.assertNotEqual(result.returncode, 0)
            run = Path(self.status()['runDir'])
            self.assertFalse((run/'candidate.json').exists())
            self.assertTrue((run/'source.html').exists())

    def test_approved_but_tampered_candidate_rejected(self):
        run, _ = self.prepared()
        candidate = json.loads((run/'candidate.json').read_text())
        candidate['models'][0]['name'] = 'not-the-source-model'
        (run/'candidate.json').write_text(json.dumps(candidate))
        sha = hashlib.sha256((run/'candidate.json').read_bytes()).hexdigest()
        result = self.run_script('publish', run, '--approved-sha256', sha)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.status()['phase'], 'qc-gate')
        self.assertFalse(self.log.exists())

    def test_proxy_and_http_failures(self):
        result = self.run_script('fetch', MOCK_PROXY_FAIL='3')
        self.assertEqual(result.returncode, 3)
        self.assertNotIn('curl', self.log.read_text())
        result = self.run_script('fetch', MOCK_HTTP='403')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.status()['status'], 'failed')

    def test_qc_hash_and_dirty_tree_gate(self):
        run, sha = self.prepared()
        self.assertNotEqual(self.run_script('publish', run, '--approved-sha256', '0'*64).returncode, 0)
        (self.repo/'unrelated.txt').write_text('do not change')
        result = self.run_script('publish', run, '--approved-sha256', sha)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.status()['phase'], 'repository-gate')
        self.assertEqual((self.repo/'unrelated.txt').read_text(), 'do not change')
        self.assertNotIn('push origin', self.log.read_text())

    def test_build_failure_rolls_back_new_snapshot(self):
        run, sha = self.prepared()
        result = self.run_script('publish', run, '--approved-sha256', sha, MOCK_BUILD_FAIL='7')
        self.assertEqual(result.returncode, 7, result.stderr)
        self.assertEqual(self.git('status', '--porcelain').stdout, '')
        self.assertFalse((self.repo/'src/data/lmarena/snapshots/2026-10-11.json').exists())
        self.assertNotIn('push origin', self.log.read_text())

    def test_three_push_failures_remain_failed_and_retry_is_idempotent(self):
        run, sha = self.prepared()
        result = self.run_script('publish', run, '--approved-sha256', sha, MOCK_PUSH_FAIL='1')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.status()['phase'], 'push')
        self.assertEqual(self.status()['status'], 'failed')
        log = self.log.read_text()
        self.assertEqual(log.count('push origin main'), 3)
        self.assertNotIn('rebase', log)
        self.assertNotIn('pull ', log)
        commits = self.git('rev-list', '--count', 'HEAD').stdout
        result = self.run_script('publish', run, '--approved-sha256', sha)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.status()['status'], 'published')
        self.assertEqual(self.git('rev-list', '--count', 'HEAD').stdout, commits)
        self.assertEqual(self.git('status', '--porcelain').stdout, '')


    # ---- fetch-hf (default) -------------------------------------------------
    def hf_env(self, raw=HF_RAW, etag=None, size=None, commit=HF_META['hubRepoCommit'], **env):
        (self.base/'source.parquet').write_bytes(raw)
        headers = self.base/'hf.headers'
        etag = hashlib.sha256(raw).hexdigest() if etag is None else etag
        size = len(raw) if size is None else size
        headers.write_text('HTTP/1.1 200 Connection established\r\n\r\nHTTP/2 302\r\n'
                           f'x-repo-commit: {commit}\r\nx-linked-size: {size}\r\n'
                           f'x-linked-etag: "{etag}"\r\nlocation: https://us.aws.cdn.hf.co/x\r\n\r\n'
                           'HTTP/2 200\r\ncontent-length: 1\r\n\r\n')
        return dict({'MOCK_EFFECTIVE': 'https://us.aws.cdn.hf.co/xet-bridge-us/abc?Signature=x'},
                    MOCK_RAW=str(self.base/'source.parquet'), MOCK_HEADERS=str(headers), **env)

    def test_default_mode_is_fetch_hf_and_never_publishes(self):
        # Fixture rows re-dated to "today" so the 45-day freshness gate is exercised for real.
        rows = [dict(r, leaderboard_publish_date=today_str()) for r in HF_ROWS]
        result = self.run_script(**self.hf_env(hf_bytes(rows)))
        self.assertEqual(result.returncode, 0, result.stderr)
        status = self.status()
        self.assertEqual((status['mode'], status['status']), ('fetch-hf', 'candidate_ready'))
        run = Path(status['runDir'])
        meta = json.loads((run/'fetch.json').read_text())
        self.assertEqual(meta['sourceKind'], 'hf-parquet')
        self.assertEqual(meta['sha256'], hashlib.sha256((run/'source.parquet').read_bytes()).hexdigest())
        self.assertEqual(meta['hubLinkedEtag'], meta['sha256'])
        self.assertEqual(meta['hubRepoCommit'], HF_META['hubRepoCommit'])
        self.assertEqual(meta['sourceUrl'], hf.SOURCE_URL)
        candidate = json.loads((run/'candidate.json').read_text())
        self.assertEqual(candidate['totalModelsObserved'], 419)
        self.assertFalse((run/'source.html').exists())
        log = self.log.read_text()
        self.assertIn('proxy-check', log)
        self.assertNotIn('git ', log)
        self.assertNotIn('pnpm', log)
        self.assertEqual(list((self.repo/'src/data/lmarena/snapshots').glob('*.json')), [])

    def test_fetch_hf_failures_preserve_raw_and_are_nonzero(self):
        # Lazy: hf_env writes the shared mock body, so build each env right before its run.
        fresh = [dict(r, leaderboard_publish_date=today_str()) for r in HF_ROWS]
        cases = {
            'cloudflare-html-200': lambda: self.hf_env(b'<html>Just a moment...</html>'),
            'hub-etag-mismatch': lambda: self.hf_env(hf_bytes(fresh), etag='0'*64),
            'stale-data': lambda: self.hf_env(),  # fixture publish 2026-10-28 vs today's capture
            'http-403': lambda: self.hf_env(hf_bytes(fresh), MOCK_HTTP='403'),
            'offsite-redirect': lambda: self.hf_env(hf_bytes(fresh), MOCK_EFFECTIVE='https://evil.example/x.parquet'),
            'unexpected-category-shape': lambda: self.hf_env(hf_bytes([dict(r, category='english') for r in fresh])),
        }
        if today_str() < '2026-12-13':
            del cases['stale-data']  # only meaningful once the fixture is >45 days old
        for name, make_env in cases.items():
            with self.subTest(name):
                result = self.run_script('fetch-hf', **make_env())
                self.assertNotEqual(result.returncode, 0)
                status = self.status()
                self.assertEqual((status['status'], status['phase']), ('failed', 'parse'))
                run = Path(status['runDir'])
                self.assertTrue((run/'source.parquet').exists())
                self.assertTrue((run/'fetch.json').exists())
                self.assertFalse((run/'candidate.json').exists())

    def test_fetch_hf_curl_failure_and_proxy_missing(self):
        result = self.run_script('fetch-hf', **self.hf_env(MOCK_CURL_FAIL='28'))
        self.assertEqual(result.returncode, 28)
        self.assertEqual(self.status()['phase'], 'fetch')
        self.assertTrue((Path(self.status()['runDir'])/'fetch.json').exists())
        self.log.unlink()
        result = self.run_script('fetch-hf', MOCK_PROXY_FAIL='3', **self.hf_env())
        self.assertEqual(result.returncode, 3)
        self.assertNotIn('curl', self.log.read_text())

    def test_fetch_hf_missing_dependency_fails_before_network(self):
        result = self.run_script('fetch-hf', ARENA_PYTHON=str(self.base/'no-such-python'), **self.hf_env())
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.status()['phase'], 'dependency-check')
        self.assertFalse(self.log.exists())
        result = self.run_script('fetch-hf', ARENA_PYTHON=self.real_python, **self.hf_env())  # system python, no pyarrow
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('pyarrow', result.stderr)
        self.assertFalse(self.log.exists())

    def hf_prepared(self):
        run = self.repo/'.cron-logs/lmarena/offline-hf'
        run.mkdir(parents=True)
        (run/'source.parquet').write_bytes(HF_RAW)
        (run/'fetch.json').write_text(json.dumps(HF_META))
        result = self.run_script('parse', run)
        self.assertEqual(result.returncode, 0, result.stderr)
        return run, hashlib.sha256((run/'candidate.json').read_bytes()).hexdigest()

    def test_hf_parse_replay_and_publish_gates(self):
        run, sha = self.hf_prepared()
        self.assertEqual((run/'candidate.json').read_bytes(),
                         (ROOT/'state/lmarena-candidates/2026-11-02.json').read_bytes())
        candidate = json.loads((run/'candidate.json').read_text())
        candidate['models'][0]['rating'] += 1
        (run/'candidate.json').write_text(json.dumps(candidate))
        tampered = hashlib.sha256((run/'candidate.json').read_bytes()).hexdigest()
        result = self.run_script('publish', run, '--approved-sha256', tampered)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.status()['phase'], 'qc-gate')
        self.assertFalse(self.log.exists())
        (run/'source.html').write_text('x')
        self.assertNotEqual(self.run_script('parse', run).returncode, 0)

    def test_hf_publish_success_path(self):
        run, sha = self.hf_prepared()
        result = self.run_script('publish', run, '--approved-sha256', sha)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.status()['status'], 'published')
        self.assertEqual((self.repo/'src/data/lmarena/snapshots/2026-11-02.json').read_bytes(),
                         (run/'candidate.json').read_bytes())
        self.assertEqual(self.git('status', '--porcelain').stdout, '')


if __name__ == '__main__':
    unittest.main()
