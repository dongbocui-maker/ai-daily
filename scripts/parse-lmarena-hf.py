#!/usr/bin/env python3
"""Validate LMArena's official Hugging Face leaderboard parquet, fail closed.

Usage: parse-lmarena-hf.py INPUT_PARQUET FETCH_METADATA OUTPUT_JSON

Source: lmarena-ai/leaderboard-dataset, text_style_control/latest, rows with
category == 'overall' (= Text / Overall / style control, same statistical basis
as the arena.ai page; verified row-for-row on the 2026-10-08 publish).
FETCH_METADATA is written by `fetch-lmarena.sh fetch-hf`. Output is atomic;
an existing output is never truncated on failure. No networking or repo writes.
Requires pyarrow (dedicated venv, default /root/.venvs/arena); missing => exit 3.
"""
import hashlib
import io
import json
import math
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from urllib.parse import urlsplit

try:
    import pyarrow as pa
    import pyarrow.parquet as pq
except ImportError:  # Explicit, distinct failure; never fall back silently.
    pa = pq = None

DATASET = 'lmarena-ai/leaderboard-dataset'
DATA_FILE = 'text_style_control/latest-00000-of-00001.parquet'
SOURCE_URL = f'https://huggingface.co/datasets/{DATASET}/resolve/main/{DATA_FILE}'
SOURCE_PAGE = f'https://huggingface.co/datasets/{DATASET}'
# Hub resolve endpoint redirects to its CDN; any other host is rejected.
ALLOWED_HOST_SUFFIXES = ('huggingface.co', '.huggingface.co', '.hf.co')
CATEGORY = 'overall'
# v2: identical statistical basis to v1 (text/overall/style-control), but the
# model identity namespace changed (HF display names, no modelKey). The page
# compares months by `name`, so v1<->v2 must not be diffed. See docs.
BASIS = 'arena-text-overall-style-control-v2'
TOP_N = 50
MIN_MODELS = 100
MAX_MODELS = 5000
MAX_AGE = timedelta(days=45)
REQUIRED_COLUMNS = {
    'model_name': 'string', 'organization': 'string', 'rating': 'double',
    'rating_lower': 'double', 'rating_upper': 'double', 'vote_count': 'double',
    'rank': 'int64', 'category': 'string', 'leaderboard_publish_date': 'string',
}
# Display names, verified 1:1 against arena.ai modelOrganization on the
# 2026-10-08 publish (both sources contain identical rows). Unknown ids are
# shown verbatim and listed in unmappedOrganizations; never guessed.
ORG_DISPLAY = {
    'alibaba': 'Alibaba', 'allenai': 'Ai2', 'amazon': 'Amazon', 'ant-group': 'Ant Group',
    'anthropic': 'Anthropic', 'baidu': 'Baidu', 'bytedance': 'Bytedance', 'cohere': 'Cohere',
    'deepseek': 'DeepSeek', 'google': 'Google', 'ibm': 'IBM', 'inception-ai': 'Inception AI',
    'meituan': 'Meituan', 'meta': 'Meta', 'microsoft': 'Microsoft', 'minimax': 'MiniMax',
    'mistral': 'Mistral', 'moonshot': 'Moonshot', 'nvidia': 'Nvidia', 'openai': 'OpenAI',
    'stepfun': 'StepFun', 'tencent': 'Tencent', 'thinky': 'Thinky', 'upstage': 'Upstage',
    'xai': 'SpaceXAI', 'xiaomi': 'Xiaomi', 'zai': 'Z.ai',
}
UNKNOWN_ORG = '未披露'


class InvalidSource(ValueError):
    pass


class MissingDependency(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise InvalidSource(message)


def timestamp(value, label):
    require(isinstance(value, str), f'Missing {label}')
    try:
        result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError as exc:
        raise InvalidSource(f'Invalid {label}') from exc
    require(result.tzinfo is not None, f'{label} must have timezone')
    return result


def finite(value, label, low=0, high=10000):
    require(type(value) in (int, float) and math.isfinite(value) and low < value < high,
            f'Invalid {label}: {value!r}')


def check_transport(raw, metadata):
    require(metadata.get('sourceKind') == 'hf-parquet', 'Metadata is not an HF parquet capture')
    require(metadata.get('curlExitCode') == 0, 'Capture transport did not complete successfully')
    require(metadata.get('httpStatus') == 200, 'Capture was not HTTP 200')
    require(metadata.get('sourceUrl') == SOURCE_URL, 'Unexpected source URL / dataset file')
    effective = urlsplit(metadata.get('effectiveUrl') or '')
    host = (effective.hostname or '').lower()
    require(effective.scheme == 'https' and any(
        host == s.lstrip('.') or host.endswith(s) for s in ALLOWED_HOST_SUFFIXES),
        f'Unexpected effective host: {host!r}')
    digest = hashlib.sha256(raw).hexdigest()
    require(metadata.get('sha256') == digest, 'Source SHA-256 mismatch')
    require(metadata.get('bytes') == len(raw), 'Source byte count mismatch')
    # HF exposes the stored object's sha256/size; when present they must agree.
    etag = metadata.get('hubLinkedEtag')
    if etag is not None:
        require(etag == digest, 'Downloaded bytes differ from Hub-declared sha256 (x-linked-etag)')
    size = metadata.get('hubLinkedSize')
    if size is not None:
        require(size == len(raw), 'Downloaded size differs from Hub-declared size')
    revision = metadata.get('hubRepoCommit')
    require(revision is None or re.fullmatch(r'[0-9a-f]{40}', revision or ''), 'Invalid hubRepoCommit')
    return digest


def read_rows(raw):
    if pq is None:
        raise MissingDependency('pyarrow is not installed in this interpreter; use /root/.venvs/arena/bin/python')
    require(len(raw) >= 12 and raw[:4] == b'PAR1' and raw[-4:] == b'PAR1',
            'Not a parquet file (HTTP 200 may be an HTML/error body)')
    try:
        table = pq.read_table(pa.BufferReader(raw))
    except (pa.ArrowException, OSError) as exc:
        raise InvalidSource(f'Unreadable parquet: {exc}') from exc
    for column, kind in REQUIRED_COLUMNS.items():
        require(column in table.schema.names, f'Missing column {column}')
        require(str(table.schema.field(column).type) == kind,
                f'Column {column} type {table.schema.field(column).type} != {kind}')
    return table.select(list(REQUIRED_COLUMNS)).to_pylist()


def validate_rows(rows, captured):
    overall = [r for r in rows if r['category'] == CATEGORY]
    total = len(overall)
    require(MIN_MODELS <= total <= MAX_MODELS, f'Model count {total} outside {MIN_MODELS}-{MAX_MODELS}')
    dates = {r['leaderboard_publish_date'] for r in overall}
    require(len(dates) == 1, f'Expected one leaderboard_publish_date, got {sorted(map(str, dates))}')
    published_text = dates.pop()
    require(isinstance(published_text, str) and re.fullmatch(r'\d{4}-\d{2}-\d{2}', published_text),
            f'Invalid leaderboard_publish_date: {published_text!r}')
    try:
        published = date.fromisoformat(published_text)
    except ValueError as exc:
        raise InvalidSource(f'Invalid leaderboard_publish_date: {published_text!r}') from exc
    # Date-only value; capture is Asia/Shanghai (ahead of UTC/US), so a
    # legitimate publish date can never be later than the local capture date.
    require(published <= captured.date(), 'leaderboard_publish_date is in the future')
    require(captured.date() - published <= MAX_AGE, 'Source data is over 45 days old')
    names = set()
    for row in overall:
        name = row['model_name']
        require(isinstance(name, str) and name.strip(), 'Missing model_name')
        require(name not in names, f'Duplicate display name: {name}')
        names.add(name)
        # Source-provided empty org => unknown; null/missing => schema breakage.
        require(isinstance(row['organization'], str), f'Missing organization: {name}')
        require(type(row['rank']) is int and 1 <= row['rank'] <= total, f'Invalid rank: {name}')
        for field in ('rating', 'rating_lower', 'rating_upper'):
            finite(row[field], f'{field} ({name})')
        require(row['rating_lower'] <= row['rating'] <= row['rating_upper'], f'Invalid rating CI: {name}')
        votes = row['vote_count']
        finite(votes, f'vote_count ({name})', low=0, high=1e12)
        require(float(votes).is_integer() and votes >= 1, f'Invalid vote_count: {name}')
    ordered = sorted(overall, key=lambda r: r['rank'])
    require([r['rank'] for r in ordered] == list(range(1, total + 1)),
            'Ranks must be unique, complete positions 1..N (ties/schema changes need review)')
    require(all(a['rating'] >= b['rating'] for a, b in zip(ordered, ordered[1:])),
            'Ratings are inconsistent with ranks')
    return ordered, published_text


def build_snapshot(raw, metadata):
    digest = check_transport(raw, metadata)
    captured = timestamp(metadata.get('fetchedAt'), 'fetchedAt')
    ordered, published = validate_rows(read_rows(raw), captured)
    models, unmapped = [], set()
    for row in ordered[:TOP_N]:
        org_id = row['organization']
        if org_id and org_id not in ORG_DISPLAY:
            unmapped.add(org_id)
        models.append({
            'rank': row['rank'], 'name': row['model_name'],
            'modelKey': None,  # HF has no stable internal key; not fabricated.
            'org': ORG_DISPLAY.get(org_id, org_id) if org_id else UNKNOWN_ORG,
            'orgId': org_id or None,
            'scores': {'overall': row['rank']},
            'rating': row['rating'], 'ratingLower': row['rating_lower'],
            'ratingUpper': row['rating_upper'],
            'rankUpper': None, 'rankLower': None,  # Not published in HF dataset.
            'votes': int(row['vote_count']),
            'highlight': [], 'summary': f'文本总榜 #{row["rank"]}（风格控制）',
        })
    return {
        'schemaVersion': 2, 'snapshotDate': captured.date().isoformat(),
        'fetchedAt': metadata['fetchedAt'], 'sourceUpdatedAt': published,
        'sourceTimeMeaning': 'leaderboard publish date',
        'sourceTimeLabel': '官方榜单发布日期',
        'sourceTimeNote': ('HF 数据集 leaderboard_publish_date：官方榜单发布日期（仅日期、无时刻/时区）；'
                           '不是投票截止时间，也不是抓取日期。HF 发布通常滞后 arena.ai 官网数天。'),
        'rankingBasis': BASIS, 'rankingLabel': '文本总榜（风格控制）',
        'rankingBasisNote': ('与 arena-text-overall-style-control-v1 统计口径相同（2026-10-08 发布逐行一致），'
                             '但模型名改为 HF 展示名且无 modelKey，名称不可与 v1 快照直接比对，故不计算跨口径升降。'),
        'sourceLeaderboardId': f'hf:{DATASET}/{DATA_FILE}#category={CATEGORY}',
        'styleControl': True,
        'totalModelsObserved': len(ordered), 'totalModelsShown': len(models),
        'sourceTotalVotes': None,
        'sourceTotalVotesNote': ('HF 数据集不提供全局对战总票数；逐模型 vote_count 之和会重复计票'
                                 '（每场对战计入两个模型），不能当作总票数，故置空。'),
        'categoryLabels': {'overall': '文本综合'},
        'sourceUrl': SOURCE_URL, 'sourcePage': SOURCE_PAGE,
        'sourceLabel': 'LMArena 官方 Hugging Face 数据集',
        'sourceRevision': metadata.get('hubRepoCommit'),
        'sourceSha256': digest, 'sourceBytes': len(raw),
        'sourceFormat': f'Hugging Face parquet ({DATASET} {DATA_FILE}, category={CATEGORY})',
        'unmappedOrganizations': sorted(unmapped),
        'coverageNote': ('仅文本总榜（风格控制），来自 LMArena 官方 HF 数据集；不含分项排名，不生成优势赛道；'
                         '不含名次置信区间。与不同 rankingBasis 的历史快照不直接比较。'),
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
        temporary = output_path.with_name(output_path.name + '.tmp')
        temporary.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        temporary.replace(output_path)
    except MissingDependency as exc:
        print(f'ARENA_PARSE_FAILED dependency: {exc}; raw source retained: {source}', file=sys.stderr)
        return 3
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(f'ARENA_PARSE_FAILED {exc}; raw source retained: {source}', file=sys.stderr)
        return 2
    print(f'ARENA_CANDIDATE_OK source=hf observed={snapshot["totalModelsObserved"]} '
          f'shown={snapshot["totalModelsShown"]} captured={snapshot["fetchedAt"]} '
          f'published={snapshot["sourceUpdatedAt"]} output={output_path}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
