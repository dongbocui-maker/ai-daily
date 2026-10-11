"""Offline, deterministic regression tests; no real proxy/service/GitHub writes.
Run: python3 -m unittest discover -s tests -p 'test_lmarena.py' -v
"""
import copy
import gzip
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
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


class ShellTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.repo = self.base/'repo'
        (self.repo/'scripts').mkdir(parents=True)
        (self.repo/'src/data/lmarena/snapshots').mkdir(parents=True)
        for name in ('fetch-lmarena.sh', 'parse-lmarena.py'):
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
                        REAL_GIT=self.real_git, REAL_PYTHON=self.real_python)
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
    --dump-header) echo 'HTTP/2 200' > "$2"; shift 2;;
    *) shift;;
  esac
done
printf '%s\\n%s\\n' "${MOCK_HTTP:-200}" 'https://arena.ai/leaderboard/chat/text'
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
        result = self.run_script()
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


if __name__ == '__main__':
    unittest.main()
