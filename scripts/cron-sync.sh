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

  # Run the sync (飞书 → src/data/daily)
  pnpm sync

  # Run GitHub trending sync (4 档 → src/data/github)
  echo "[cron] running github-trending sync"
  npx tsx scripts/github-trending.ts || echo "[cron] github sync failed (非致命)"

  # Commit & push if anything changed
  if [[ -n "$(git status --porcelain src/data/)" ]]; then
    git -c user.name="ai-daily-cron" -c user.email="cron@local" \
        add src/data/
    git -c user.name="ai-daily-cron" -c user.email="cron@local" \
        commit -m "chore(data): daily sync $(TZ=Asia/Shanghai date +%F) (local cron)"

    # Push with retry (China network can be flaky)
    PUSH_OK=0
    for attempt in 1 2 3; do
      if git push origin main; then
        echo "[cron] pushed (attempt $attempt)."
        PUSH_OK=1
        break
      else
        echo "[cron] push attempt $attempt failed, retry in 30s"
        sleep 30
      fi
    done
    [[ $PUSH_OK -eq 1 ]] || echo "[cron] WARN: all push attempts failed"
  else
    echo "[cron] no changes."
  fi

  echo "[cron] done"
} >>"$LOG" 2>&1
