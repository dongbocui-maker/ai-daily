#!/usr/bin/env bash
# Local cron job: PUSH 兑底 (2026-07-12 改造：飞书文档中转已弃用).
# Triggered by crontab daily at 09:00 Asia/Shanghai.
#
# ╔══ 改造说明 (2026-07-12) ══╗
# 旧行为：git fetch → pnpm sync (拉飞书解析→写 src/data/daily) → 校验 → commit → push。
# 新行为：日报已改为 cron 子代理 (06:18) 直接写本地 JSON + cron-sync-event.sh 事件驱动 push。
#         飞书文档已不存在，pnpm sync 会拉到空/失败并可能覆盖子代理写好的好 JSON——因此移除。
#         本脚本降级为纯「push 兑底」：若事件驱动 push 因国内网络抛错 5 次失败，
#         09:00 这条再把已 commit 的本地日报推上去；并塑带 commit 任何未提交的已校验 src/data/daily 改动。
#         绝不再重新生成/拉取数据。

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

# LLM endpoint 单一可信源：从 openclaw.json 解析（换 endpoint 只改 openclaw.json 一处）
# shellcheck disable=SC1091
source "$REPO/scripts/lib/llm-endpoint.sh" || echo "[cron] WARN: LLM endpoint 解析失败，sync 翻译将走 offline"

{
  echo "===== $(date '+%F %T %Z') ====="
  echo "[cron] starting sync"

  # 不再 git fetch/ff-only（事件驱动 cron-sync-event.sh 已处理主路径）；
  # 本兑底只关心把本地 commit push 上去，避免 fetch 时 GitHub 国内网络阻塞。

  # 不再 pnpm sync（飞书文档已弃用；日报由子代理直写本地 JSON）。

  # Schema 校验门禄：若有未提交的 src/data/daily 改动，校验失败则拒绝提交坏数据
  if ! python3 scripts/validate-daily-schema.py --changed; then
    echo "[cron] ❌ schema 校验失败，拒绝提交坏数据"
    exit 1
  fi

  # Commit any uncommitted (已校验) src/data/daily changes if anything changed
  if [[ -n "$(git status --porcelain src/data/daily)" ]]; then
    git -c user.name="ai-daily-cron" -c user.email="cron@local" \
        add src/data/daily
    git -c user.name="ai-daily-cron" -c user.email="cron@local" \
        commit -m "chore(data): daily sync $(TZ=Asia/Shanghai date +%F) (local cron push-fallback)"
  else
    echo "[cron] no uncommitted src/data/daily changes."
  fi

  # 兑底核心：无论本次是否新增 commit，只要本地领先 origin/main（事件驱动 push 曾失败）就重试 push。
  if [[ -n "$(git log origin/main..HEAD --oneline 2>/dev/null)" ]]; then
    echo "[cron] 检测到未推送的本地 commit，开始 push兑底"
    # Push with retry (China network can be flaky)
    PUSH_OK=0
    for attempt in 1 2 3; do
      if git push origin main; then
        echo "[cron] pushed (attempt $attempt)."
        PUSH_OK=1
        break
      else
        echo "[cron] push attempt $attempt failed, pull --rebase then retry in 30s"
        git pull --rebase --autostash origin main 2>&1 || echo "[cron] WARN: rebase failed (will still retry push)"
        sleep 30
      fi
    done
    [[ $PUSH_OK -eq 1 ]] || echo "[cron] WARN: all push attempts failed"
  else
    echo "[cron] 本地与 origin/main 一致，无需 push。"
  fi

  echo "[cron] done"
} >>"$LOG" 2>&1
