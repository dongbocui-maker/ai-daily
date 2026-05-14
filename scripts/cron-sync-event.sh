#!/usr/bin/env bash
# Event-driven sync: 由 OpenClaw cron 子代理在 Step H 中调用
# 与 cron-sync.sh 区别：
#   1. 跳过 git fetch（避免 GitHub 国内网络问题阻塞同步）
#   2. 失败不视为整体失败（让 GitHub 抖动时 cron 仍标 ok，系统 crontab 09:30 兜底）
#   3. 输出格式以 [event-sync] 开头便于区分

set -uo pipefail  # 注意：不用 -e，让 push 失败时仍能完成自归档

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
  echo "===== $(date '+%F %T %Z') [event-driven] ====="
  echo "[event-sync] starting (called from cron subagent Step H)"

  # 跳过 git fetch——直接 pnpm sync 即可
  # 如果飞书 → src/data/daily 拉数据失败，是 fatal（必报错）
  if ! pnpm sync; then
    echo "[event-sync] ❌ pnpm sync failed (fatal)"
    exit 1
  fi

  # 检查是否有变更
  if [[ -z "$(git status --porcelain src/data/daily)" ]]; then
    echo "[event-sync] no changes in src/data/daily, skip commit"
    exit 0
  fi

  # Commit
  git -c user.name="ai-daily-cron" -c user.email="cron@local" \
      add src/data/daily
  git -c user.name="ai-daily-cron" -c user.email="cron@local" \
      commit -m "chore(data): daily sync $(TZ=Asia/Shanghai date +%F) (event-driven from cron subagent)"

  # Push with retry (China network can be flaky)
  PUSH_OK=0
  for attempt in 1 2 3 4 5; do
    if git push origin main 2>&1; then
      echo "[event-sync] pushed (attempt $attempt)."
      PUSH_OK=1
      break
    else
      echo "[event-sync] push attempt $attempt failed, retry in 20s"
      sleep 20
    fi
  done

  if [[ "$PUSH_OK" == "0" ]]; then
    echo "[event-sync] ⚠️  push failed after 5 attempts, will rely on 09:00 system cron fallback"
    # 不 exit 1——push 失败不算整体失败，commit 还在本地，下次系统 cron 会带上一起 push
  fi

  echo "[event-sync] done"
} 2>&1 | tee -a "$LOG"
