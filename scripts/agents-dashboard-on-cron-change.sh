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

echo "[$(date '+%F %T')] cron-state changed -> dashboard refresh" >> "$LOG"
cd "$REPO" || exit 1
bash scripts/agents-dashboard-deploy.sh >> "$LOG" 2>&1
echo "[$(date '+%F %T')] refresh done (rc=$?)" >> "$LOG"
