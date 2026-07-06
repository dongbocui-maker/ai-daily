#!/usr/bin/env bash
# S.H.R.I.M.P. OS Dashboard — 事件驱动刷新触发器
# 由 systemd path unit (inotify) 监听 /root/.openclaw/cron/jobs-state.json 变化后调用。
# 每个 cron 跑完、状态落盘 → 文件变 → 本脚本触发 → 聚合最新状态 → 部署。
# 设计要点：
#   1. 去抖：短时间内多个 cron 状态写入只跑一次 deploy（settle 等待 + flock 防并发）
#   2. 时段保护：深夜(0-7点)不 push（避免夜间无谓 commit / Pages rebuild）
#   3. 幂等：底层 deploy 脚本无变化时自动 skip commit
set -uo pipefail

REPO=/root/.openclaw/workspace/projects/ai-daily
LOG=/tmp/shrimp-dash-event.log
LOCK=/tmp/shrimp-dash-event.lock
SETTLE=10   # 去抖：先静置 N 秒，吸收同一批次的多次状态写入

# flock 防并发：若已有一次刷新在跑（含 settle），本次直接退出
exec 9>"$LOCK"
if ! flock -n 9; then
  echo "[$(date '+%F %T')] another refresh in-flight, skip" >> "$LOG"
  exit 0
fi

# 时段保护：0:00-6:59 不刷新（cron 本就不该夜里跑；夜间状态变化留到白天）
H=$(date '+%H')
if [ "$H" -lt 7 ]; then
  echo "[$(date '+%F %T')] quiet hours (H=$H), skip dashboard refresh" >> "$LOG"
  exit 0
fi

# 去抖静置：等同批写入落定，再统一刷新一次
sleep "$SETTLE"

# push 冷却：距上次 push 不足 10 分钟则等到满 10 分钟再刷新（持锁期间后续触发自动吸收）
# 背景：短时间连续 push 会让 GitHub Pages 部署互顶，频发 "Deployment failed, try again later"
STAMP=/tmp/shrimp-dash-last-push
COOLDOWN=600
if [ -f "$STAMP" ]; then
  LAST=$(stat -c %Y "$STAMP" 2>/dev/null || echo 0)
  NOW=$(date +%s)
  ELAPSED=$((NOW - LAST))
  if [ "$ELAPSED" -lt "$COOLDOWN" ]; then
    WAIT=$((COOLDOWN - ELAPSED))
    echo "[$(date '+%F %T')] cooldown: last push ${ELAPSED}s ago, wait ${WAIT}s" >> "$LOG"
    sleep "$WAIT"
  fi
fi

echo "[$(date '+%F %T')] cron-state changed -> dashboard refresh" >> "$LOG"
cd "$REPO" || exit 1
bash scripts/agents-dashboard-deploy.sh >> "$LOG" 2>&1
RC=$?
# 仅当真正 push 了才刷新冷却戳（无变化 skip commit 不计入冷却）
if tail -3 "$LOG" | grep -q "pushed — Pages will rebuild"; then
  touch "$STAMP"
fi
echo "[$(date '+%F %T')] refresh done (rc=$RC)" >> "$LOG"
