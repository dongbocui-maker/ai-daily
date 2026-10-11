#!/usr/bin/env python3
"""Validate Arena's Text/Overall/style-controlled RSC leaderboard, fail closed.

Usage: parse-lmarena.py INPUT_HTML FETCH_METADATA OUTPUT_JSON
FETCH_METADATA is written by fetch-lmarena.sh; dates come from the capture, not
an arbitrary filename. Output is atomic. No networking or repository writes.
"""
import hashlib
import json
import math
import re
import sys
from datetime import datetime, timedelta
from html.parser import HTMLParser
from pathlib import Path

SOURCE_URL = 'https://arena.ai/leaderboard/chat/text'
BASIS = 'arena-text-overall-style-control-v1'
LEADERBOARD_ID = 'leaderboard-sets/public/leaderboards/text-overall-style_control/leaderboard-snapshots/latest'
TOP_N = 50
MIN_MODELS = 100
MAX_MODELS = 5000


class InvalidSource(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise InvalidSource(message)


class Scripts(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.inside = False
        self.parts = []

    def handle_starttag(self, tag, attrs):
        self.inside = tag == 'script'

    def handle_endtag(self, tag):
        if tag == 'script':
            self.inside = False

    def handle_data(self, data):
        if self.inside:
            self.parts.append(data)


def walk(node):
    if isinstance(node, dict):
        yield node
        for value in node.values():
            yield from walk(value)
    elif isinstance(node, list):
        for value in node:
            yield from walk(value)


def extract_leaderboard(html):
    scripts = Scripts()
    scripts.feed(html)
    chunks = []
    decoder = json.JSONDecoder()
    for script in scripts.parts:
        for match in re.finditer(r'self\.__next_f\.push\(', script):
            try:
                value, _ = decoder.raw_decode(script[match.end():])
            except ValueError as exc:
                raise InvalidSource('Malformed Next.js Flight chunk') from exc
            if isinstance(value, list) and len(value) == 2 and value[0] == 1:
                require(isinstance(value[1], str), 'Non-string Flight chunk')
                chunks.append(value[1])
    require(chunks, 'No Next.js Flight data (HTTP 200 may be an empty shell)')
    boards = []
    for match in re.finditer(r'^[0-9a-f]+:(.+)$', ''.join(chunks), re.M):
        # Flight module/text records are not JSON trees; never eval JS.
        payload = match[1]
        if not payload.startswith(('[', '{')):
            continue
        try:
            root = json.loads(payload)
        except ValueError:
            continue
        for node in walk(root):
            board = node.get('leaderboard')
            if isinstance(board, dict) and board.get('arenaSlug') == 'text':
                boards.append(board)
    require(len(boards) == 1, f'Expected one text leaderboard, got {len(boards)}')
    return boards[0]


def integer(value, label, low, high):
    require(type(value) is int and low <= value <= high, f'Invalid {label}: {value!r}')


def number(value, label):
    require(type(value) in (int, float) and math.isfinite(value) and 0 < value < 10000,
            f'Invalid {label}: {value!r}')


def timestamp(value, label):
    require(isinstance(value, str), f'Missing {label}')
    try:
        result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError as exc:
        raise InvalidSource(f'Invalid {label}') from exc
    require(result.tzinfo is not None, f'{label} must have timezone')
    return result


def validate_entries(board):
    require(board.get('id') == LEADERBOARD_ID, 'Unexpected leaderboard ID / ranking basis')
    require(board.get('leaderboardSlug') == 'overall', 'Not overall leaderboard')
    require(board.get('params') == {'category': 'overall', 'styleControl': True},
            'Unexpected category or style-control setting')
    total = board.get('totalModels')
    integer(total, 'totalModels', MIN_MODELS, MAX_MODELS)
    integer(board.get('totalVotes'), 'totalVotes', 1, 10**12)
    entries = board.get('entries')
    require(isinstance(entries, list), 'Missing entries')
    by_key, by_name = {}, {}
    for entry in entries:
        require(isinstance(entry, dict), 'Entry is not an object')
        for field in ('modelKey', 'modelDisplayName'):
            require(isinstance(entry.get(field), str) and entry[field].strip(), f'Missing {field}')
        # 50 legacy models have a source-provided empty org. Preserve as unknown,
        # but a missing field is schema breakage, not permission to invent an org.
        require(isinstance(entry.get('modelOrganization'), str), 'Missing modelOrganization')
        key, name = entry['modelKey'], entry['modelDisplayName']
        if key in by_key:
            require(by_key[key] == entry, f'Conflicting duplicate key: {key}')
            continue
        require(name not in by_name, f'Duplicate display name: {name}')
        for field in ('rank', 'rankUpper', 'rankLower'):
            integer(entry.get(field), field, 1, total)
        require(entry['rankUpper'] <= entry['rank'] <= entry['rankLower'], 'Invalid rank interval')
        for field in ('rating', 'ratingUpper', 'ratingLower'):
            number(entry.get(field), field)
        require(entry['ratingLower'] <= entry['rating'] <= entry['ratingUpper'], 'Invalid rating interval')
        integer(entry.get('votes'), 'votes', 1, 10**12)
        by_key[key], by_name[name] = entry, key
    require(len(by_key) == total, f'Unique entries {len(by_key)} != declared totalModels {total}')
    ordered = sorted(by_key.values(), key=lambda m: m['rank'])
    require([m['rank'] for m in ordered] == list(range(1, total + 1)),
            'Ranks must be unique, complete positions 1..totalModels (schema changes need review)')
    require(all(a['rating'] >= b['rating'] for a, b in zip(ordered, ordered[1:])),
            'Ratings are inconsistent with ranks')
    return ordered


def build_snapshot(raw, metadata):
    require(metadata.get('curlExitCode') == 0, 'Capture transport did not complete successfully')
    require(metadata.get('httpStatus') == 200, 'Capture was not HTTP 200')
    require(metadata.get('sourceUrl') == SOURCE_URL and metadata.get('effectiveUrl') == SOURCE_URL,
            'Capture URL must be the official Text leaderboard; unexpected redirects rejected')
    digest = hashlib.sha256(raw).hexdigest()
    require(metadata.get('sha256') == digest, 'Source SHA-256 mismatch')
    require(metadata.get('bytes') == len(raw), 'Source byte count mismatch')
    captured = timestamp(metadata.get('fetchedAt'), 'fetchedAt')
    board = extract_leaderboard(raw.decode('utf-8'))
    entries = validate_entries(board)
    cutoff = board.get('voteCutoffISOString')
    if cutoff is not None:
        cutoff_time = timestamp(cutoff, 'voteCutoffISOString')
        require(cutoff_time <= captured + timedelta(minutes=5), 'Source cutoff is in the future')
        require(captured - cutoff_time <= timedelta(days=45), 'Source data is over 45 days old')
    models = []
    for entry in entries[:TOP_N]:
        models.append({
            'rank': entry['rank'], 'name': entry['modelDisplayName'], 'modelKey': entry['modelKey'],
            'org': entry['modelOrganization'] or '未披露',
            'scores': {'overall': entry['rank']},
            'rating': entry['rating'], 'ratingLower': entry['ratingLower'],
            'ratingUpper': entry['ratingUpper'], 'rankUpper': entry['rankUpper'],
            'rankLower': entry['rankLower'], 'votes': entry['votes'],
            'highlight': [], 'summary': f'文本总榜 #{entry["rank"]}（风格控制）',
        })
    return {
        'schemaVersion': 2, 'snapshotDate': captured.date().isoformat(),
        'fetchedAt': metadata['fetchedAt'], 'sourceUpdatedAt': cutoff,
        'sourceTimeMeaning': 'vote cutoff' if cutoff else 'unknown',
        'sourceTimeNote': '源站投票截止时间；不是抓取日期' if cutoff else '源站未提供数据时间，不能确认数据新鲜度',
        'rankingBasis': BASIS, 'rankingLabel': '文本总榜（风格控制）',
        'sourceLeaderboardId': board['id'], 'styleControl': True,
        'totalModelsObserved': len(entries),
        'totalModelsShown': len(models), 'sourceTotalVotes': board['totalVotes'],
        'categoryLabels': {'overall': '文本综合'},
        'sourceUrl': SOURCE_URL, 'sourceSha256': digest, 'sourceBytes': len(raw),
        'sourceFormat': 'Next.js Flight leaderboard.entries',
        'coverageNote': '仅文本总榜；新页面不含旧版跨分项排名，不生成优势赛道。与无 rankingBasis 的历史快照不直接比较。',
        'models': models,
    }


def main():
    if len(sys.argv) != 4:
        print(__doc__, file=sys.stderr)
        return 1
    source, metadata_path, output_path = map(Path, sys.argv[1:])
    try:
        snapshot = build_snapshot(source.read_bytes(), json.loads(metadata_path.read_text()))
        output_path.parent.mkdir(parents=True, exist_ok=True)
        # Do not truncate an existing candidate if parsing/validation fails.
        temporary = output_path.with_name(output_path.name + '.tmp')
        temporary.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        temporary.replace(output_path)
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(f'ARENA_PARSE_FAILED {exc}; raw source retained: {source}', file=sys.stderr)
        return 2
    print(f'ARENA_CANDIDATE_OK observed={snapshot["totalModelsObserved"]} shown={snapshot["totalModelsShown"]} '
          f'captured={snapshot["fetchedAt"]} cutoff={snapshot["sourceUpdatedAt"]} output={output_path}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
