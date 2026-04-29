#!/usr/bin/env bash
# Local cron job: sync AI daily from Feishu, commit & push to GitHub.
# Triggered by crontab daily at 09:30 Asia/Shanghai.

set -euo pipefail

REPO="/root/.openclaw/workspace/projects/ai-daily"
LOG_DIR="$REPO/.cron-logs"
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/$(date +%Y-%m-%d).log"

# Load nvm so we get node/pnpm in cron's bare PATH
export NVM_DIR="/root/.nvm"
# shellcheck disable=SC1091
[[ -s "$NVM_DIR/nvm.sh" ]] && . "$NVM_DIR/nvm.sh"
export PATH="/root/.nvm/versions/node/v22.22.2/bin:$PATH"

cd "$REPO"

{
  echo "===== $(date '+%F %T %Z') ====="
  echo "[cron] starting sync"

  # Make sure remote is reachable & up-to-date
  git fetch --quiet origin main
  git reset --hard origin/main --quiet

  # Run the sync
  pnpm sync

  # Commit & push if anything changed
  if [[ -n "$(git status --porcelain src/data/daily)" ]]; then
    git -c user.name="ai-daily-cron" -c user.email="cron@local" \
        add src/data/daily
    git -c user.name="ai-daily-cron" -c user.email="cron@local" \
        commit -m "chore(data): daily sync $(TZ=Asia/Shanghai date +%F) (local cron)"
    git push origin main
    echo "[cron] pushed."
  else
    echo "[cron] no changes."
  fi

  echo "[cron] done"
} >>"$LOG" 2>&1
