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

  # Make sure remote is reachable & up-to-date.
  # 用 ff-only 而非 reset --hard：若本地有未推送 commit 会停下报错，
  # 不会静默吞掉数据（AUDIT-2026-06-11 M1）。
  git fetch --quiet origin main
  if ! git merge --ff-only origin/main --quiet; then
    echo "[cron] ❌ 本地与 origin/main 分叉（有未推送 commit?），拒绝自动 reset，需人工介入"
    git status --short
    exit 1
  fi

  # Run the sync (飞书 → src/data/daily)
  # GitHub Trending 独立 cron 走 cron-github.sh
  pnpm sync

  # Schema 校验门禄：校验失败则拒绝提交坏数据（参考 AUDIT-2026-06-11 H1）
  if ! python3 scripts/validate-daily-schema.py --changed; then
    echo "[cron] ❌ schema 校验失败，拒绝提交坏数据"
    exit 1
  fi

  # Commit & push if anything changed
  if [[ -n "$(git status --porcelain src/data/daily)" ]]; then
    git -c user.name="ai-daily-cron" -c user.email="cron@local" \
        add src/data/daily
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
