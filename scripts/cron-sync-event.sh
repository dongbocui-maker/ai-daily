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

# LLM endpoint 单一可信源：从 openclaw.json 解析（换 endpoint 只改 openclaw.json 一处）
# shellcheck disable=SC1091
source "$REPO/scripts/lib/llm-endpoint.sh" || echo "[event-sync] WARN: LLM endpoint 解析失败，sync 翻译将走 offline"

{
  echo "===== $(date '+%F %T %Z') [event-driven] ====="
  echo "[event-sync] starting (called from cron subagent Step H)"

  # 2026-07-12 改造：砍掉飞书文档中转，日报由 cron 子代理 Step D 直接写本地
  # src/data/daily/YYYY-MM-DD.json。本步不再拉飞书解析（pnpm sync 已移除），
  # 只负责：schema 校验已改动的 JSON → commit → push。
  # 弃用说明：sync.ts / parse.ts / feishu.ts / append-to-doc.sh 已弃用于日报流程，
  #           保留文件（遵铁律17不删），pnpm sync 仍在 package.json 供人工/历史用途。

  # Schema 校验门禄：校验失败则不 commit（但仍完成自归档，不当整体失败）
  # 参考 AUDIT-2026-06-11 H1：坏数据不能上线，等 09:00 系统 cron 修复后重试
  if ! python3 scripts/validate-daily-schema.py --changed; then
    echo "[event-sync] ❌ schema 校验失败，拒绝 commit（坏数据不上线）"
    exit 0
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
  # 2026-07-25 体检修复：失败后先 pull --rebase --autostash 再重试——
  # 多写手（dashboard/X/github/podcast/GHA）并发 push 会导致 non-fast-forward，
  # 光重试不 rebase 必然 5 连败（当天日报就发作过）。autostash 兼容工作区脏文件。
  PUSH_OK=0
  for attempt in 1 2 3 4 5; do
    if git push origin main 2>&1; then
      echo "[event-sync] pushed (attempt $attempt)."
      PUSH_OK=1
      break
    else
      echo "[event-sync] push attempt $attempt failed, pull --rebase then retry in 20s"
      git pull --rebase --autostash origin main 2>&1 || echo "[event-sync] ⚠️ rebase failed (will still retry push)"
      sleep 20
    fi
  done

  if [[ "$PUSH_OK" == "0" ]]; then
    echo "[event-sync] ⚠️  push failed after 5 attempts, will rely on 09:00 system cron fallback"
    # 不 exit 1——push 失败不算整体失败，commit 还在本地，下次系统 cron 会带上一起 push
  fi

  echo "[event-sync] done"
} 2>&1 | tee -a "$LOG"
