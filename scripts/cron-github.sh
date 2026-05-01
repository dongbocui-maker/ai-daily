#!/usr/bin/env bash
# Local cron job: refresh GitHub board(s) and push to GitHub.
# Usage: cron-github.sh <board>
#   board: daily | weekly | monthly | yearly
# Triggered by crontab entries.

set -euo pipefail

BOARD="${1:-daily}"
case "$BOARD" in
  daily|weekly|monthly|yearly) ;;
  *) echo "ERROR: invalid board '$BOARD' (use daily/weekly/monthly/yearly)"; exit 1 ;;
esac

REPO="/root/.openclaw/workspace/projects/ai-daily"
LOG_DIR="$REPO/.cron-logs"
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/github-$BOARD-$(date +%Y-%m-%d).log"

# Load nvm so we get node/pnpm in cron's bare PATH
export NVM_DIR="/root/.nvm"
# shellcheck disable=SC1091
[[ -s "$NVM_DIR/nvm.sh" ]] && . "$NVM_DIR/nvm.sh"
export PATH="/root/.nvm/versions/node/v22.22.2/bin:$PATH"

cd "$REPO"

# Load .env (LLM key + GITHUB_TOKEN if present)
if [[ -f .env ]]; then
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
fi

# GITHUB_TOKEN —— 用专门的 PAT 避免 60 req/h rate limit
if [[ -z "${GITHUB_TOKEN:-}" ]] && [[ -f /root/.openclaw/secrets/github-ai-daily.token ]]; then
  GITHUB_TOKEN=$(cat /root/.openclaw/secrets/github-ai-daily.token)
  export GITHUB_TOKEN
fi

{
  echo "===== $(date '+%F %T %Z') board=$BOARD ====="
  echo "[cron-github] starting refresh of $BOARD board"

  # Stay in sync with origin
  git fetch --quiet origin main
  git reset --hard origin/main --quiet

  # Run only the requested board
  npx tsx scripts/github-trending.ts --${BOARD}-only

  # Commit & push if anything changed
  if [[ -n "$(git status --porcelain src/data/github)" ]]; then
    git -c user.name="ai-daily-cron" -c user.email="cron@local" \
        add src/data/github
    git -c user.name="ai-daily-cron" -c user.email="cron@local" \
        commit -m "chore(github): refresh $BOARD board ($(TZ=Asia/Shanghai date +%F))"

    # Push with retry (China network is flaky for github.com)
    PUSH_OK=0
    for attempt in 1 2 3; do
      if git push origin main; then
        echo "[cron-github] pushed (attempt $attempt)."
        PUSH_OK=1
        break
      else
        echo "[cron-github] push attempt $attempt failed, retry in 30s"
        sleep 30
      fi
    done
    [[ $PUSH_OK -eq 1 ]] || echo "[cron-github] WARN: all push attempts failed"
  else
    echo "[cron-github] no changes for $BOARD."
  fi

  echo "[cron-github] done"
} >>"$LOG" 2>&1
