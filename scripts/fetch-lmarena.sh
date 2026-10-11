#!/usr/bin/env bash
# Arena monthly job: default = fetch a QC candidate ONLY (no build/commit/push).
# System crontab: 10:30 Asia/Shanghai, day 1. Scheduling is not managed here.
# Uses the ALREADY RUNNING proxy; never starts/stops/kills shared services.
# See docs/arena-pipeline.md for review/publish and local status/alert limitations.
set -euo pipefail
export PATH="/root/.nvm/versions/node/v22.22.2/bin:$PATH"
export TZ=Asia/Shanghai
PROJECT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
STATE_DIR=${ARENA_STATE_DIR:-"$PROJECT_DIR/.cron-logs/lmarena"}
PROXY="http://127.0.0.1:7890"
SOURCE_URL="https://arena.ai/leaderboard/chat/text"
MODE=${1:-fetch}
RUN_DIR=""
PHASE=initializing
RESULT=failed
ROLLBACK_FILE=""
mkdir -p "$STATE_DIR"

finish() {
  local rc=$?
  trap - EXIT
  if [[ -n "$ROLLBACK_FILE" ]]; then
    # Only a new file created by THIS invocation, and never a pre-existing file.
    git -C "$PROJECT_DIR" restore --staged -- "$ROLLBACK_FILE" 2>/dev/null || true
    rm -f -- "$PROJECT_DIR/$ROLLBACK_FILE"
  fi
  python3 - "$STATE_DIR" "$RUN_DIR" "$MODE" "$PHASE" "$RESULT" "$rc" <<'PY'
import json, sys
from datetime import datetime
from pathlib import Path
state, run, mode, phase, result, code = sys.argv[1:]
record = {'finishedAt': datetime.now().astimezone().isoformat(), 'mode': mode,
          'phase': phase, 'status': result if code == '0' else 'failed',
          'exitCode': int(code), 'runDir': run,
          'notificationDelivered': False}
for dest in [Path(state) / 'latest-status.json'] + ([Path(run) / 'status.json'] if run else []):
    tmp = dest.with_suffix('.tmp')
    tmp.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
    tmp.replace(dest)
PY
  local status_rc=$?
  if [[ "$status_rc" -ne 0 ]]; then rc=$status_rc; fi
  if [[ "$rc" -eq 0 ]]; then
    echo "ARENA_${RESULT^^} run=$RUN_DIR (local status only; no notification sent)"
  else
    echo "ARENA_FAILED mode=$MODE phase=$PHASE exit=$rc raw=$RUN_DIR (local status only)" >&2
  fi
  exit "$rc"
}
trap finish EXIT
fail() { echo "$*" >&2; exit 2; }
parse() {
  python3 "$PROJECT_DIR/scripts/parse-lmarena.py" "$RUN_DIR/source.html" \
    "$RUN_DIR/fetch.json" "$1"
}
check_proxy() {
  PHASE=proxy-check
  python3 - <<'PY'
import socket
try:
    with socket.create_connection(('127.0.0.1', 7890), timeout=3): pass
except OSError as exc:
    raise SystemExit(f'Existing proxy unavailable at 127.0.0.1:7890: {exc}; no service changes attempted')
PY
}

# Serialize invocations without touching the shared proxy or daemon.
exec 8>"$STATE_DIR/run.lock"
flock -n 8 || fail 'Another Arena invocation is running'
case "$MODE" in
  fetch)
    [[ $# -le 1 ]] || fail 'Usage: fetch-lmarena.sh [fetch]'
    RUN_DIR=$(mktemp -d "$STATE_DIR/$(date +%Y-%m-%dT%H%M%S)-XXXXXX")
    check_proxy
    PHASE=fetch
    CAPTURED=$(date --iso-8601=seconds)
    # Preserve the body and headers even for non-200 or parser failure.
    curl_rc=0
    curl --silent --show-error --location --proto '=https' --proto-redir '=https' \
      --proxy "$PROXY" --connect-timeout 15 --max-time 90 \
      --dump-header "$RUN_DIR/response.headers" --output "$RUN_DIR/source.html" \
      --write-out '%{http_code}\n%{url_effective}\n' "$SOURCE_URL" \
      > "$RUN_DIR/transport.txt" || curl_rc=$?
    python3 - "$RUN_DIR" "$CAPTURED" "$SOURCE_URL" "$curl_rc" <<'PY'
import hashlib, json, sys
from pathlib import Path
run, captured, url, code = sys.argv[1:]
p = Path(run)
raw = (p/'source.html').read_bytes() if (p/'source.html').exists() else b''
transport = (p/'transport.txt').read_text().splitlines()
meta = {'fetchedAt': captured, 'sourceUrl': url,
        'effectiveUrl': transport[1] if len(transport)>1 else '',
        'httpStatus': int(transport[0]) if transport and transport[0].isdigit() else 0,
        'curlExitCode': int(code), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
(p/'fetch.json').write_text(json.dumps(meta, indent=2)+'\n')
PY
    [[ "$curl_rc" -eq 0 ]] || exit "$curl_rc"
    PHASE=parse
    parse "$RUN_DIR/candidate.json"
    RESULT=candidate_ready
    ;;
  parse)
    [[ $# -eq 2 ]] || fail 'Usage: fetch-lmarena.sh parse RUN_DIR'
    RUN_DIR=$(cd "$2" && pwd)
    PHASE=parse
    parse "$RUN_DIR/candidate.json"
    RESULT=candidate_ready
    ;;
  publish)
    [[ $# -eq 4 && "$3" == --approved-sha256 ]] || fail 'Usage: fetch-lmarena.sh publish RUN_DIR --approved-sha256 QC_APPROVED_CANDIDATE_SHA256'
    RUN_DIR=$(cd "$2" && pwd)
    PHASE=qc-gate
    [[ "$4" =~ ^[a-f0-9]{64}$ ]] || fail 'Invalid approval hash'
    ACTUAL=$(sha256sum "$RUN_DIR/candidate.json" | cut -d' ' -f1)
    [[ "$ACTUAL" == "$4" ]] || fail 'QC approval hash does not match candidate'
    parse "$RUN_DIR/revalidated.json"
    cmp "$RUN_DIR/candidate.json" "$RUN_DIR/revalidated.json" || fail 'Candidate differs from raw source reparse'
    check_proxy
    PHASE=repository-gate
    cd "$PROJECT_DIR"
    # Same publication lock as daily-watchdog; never autostash/rebase a dirty tree.
    exec 9>/tmp/ai-daily-publish.lock
    flock -w 300 9 || fail 'Publication lock timed out'
    [[ "$(git branch --show-current)" == main ]] || fail 'Publish requires main branch'
    [[ -z "$(git status --porcelain)" ]] || fail 'Publish requires a clean working tree (including untracked files)'
    DATE=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["snapshotDate"])' "$RUN_DIR/candidate.json")
    TARGET="src/data/lmarena/snapshots/$DATE.json"
    if [[ -e "$TARGET" ]]; then
      cmp "$RUN_DIR/candidate.json" "$TARGET" || fail 'A different snapshot already exists for this date; refusing overwrite'
    else
      ROLLBACK_FILE="$TARGET"
      cp "$RUN_DIR/candidate.json" "$TARGET"
    fi
    PHASE=build
    # Avoid package prebuild's unrelated agent-chain data writes.
    pnpm exec astro build > "$RUN_DIR/build.log" 2>&1
    PHASE=commit
    git add -- "$TARGET"
    if ! git diff --cached --quiet; then
      git commit -m "chore(lmarena): reviewed snapshot $DATE" -- "$TARGET"
    fi
    ROLLBACK_FILE=""
    PHASE=push
    # No pull/rebase/autostash. Non-fast-forward => human reconciliation.
    for attempt in 1 2 3; do
      if git -c http.proxy="$PROXY" push origin main; then
        RESULT=published
        exit 0
      fi
      echo "ARENA_PUSH_RETRY attempt=$attempt/3 (no rebase)" >&2
      if [[ "$attempt" -lt 3 ]]; then sleep 10; fi
    done
    fail 'All 3 pushes failed; reviewed local commit retained for manual retry'
    ;;
  *) fail 'Modes: fetch (default), parse RUN_DIR, publish RUN_DIR --approved-sha256 SHA256' ;;
esac
