#!/usr/bin/env bash
# daily-watchdog.sh — AI 日报独立看门狗（2026-09-13 建，根因见 memory/2026-09-13.md）
# 设计原则：发布尾段（commit+push）是确定性操作，用脚本完成，不依赖 LLM。
# 输出标记（供 cron prompt 判断）：
#   WD_OK               当日日报健康（JSON 在 + 站点已含当日日期）
#   WD_HEALED_PUSH      JSON 在但站点没更新 → 已代为 push，站点已恢复
#   WD_PUSH_FAILED      代推后站点仍未更新（build 失败等）→ 需人工
#   WD_RERUN_TRIGGERED  JSON 缺失 → 已触发 cron 重跑（第 N 次）
#   WD_ESCALATE         重跑 2 次仍失败 → 需人工介入
set -uo pipefail
cd /root/.openclaw/workspace/projects/ai-daily

# 防并发：与主 cron Step I 的 push 或另一个 watchdog 实例互斥（MK46 medium-3）
exec 9>/tmp/ai-daily-publish.lock
if ! flock -w 300 9; then
  echo "[watchdog] 获取发布锁超时（300s），疑另一发布流程在跑，退出" >&2
  exit 5
fi

TODAY=$(date +%F)
JSON="src/data/daily/${TODAY}.json"
PROXY="http://127.0.0.1:7890"
CRON_ID="c24f6b6f-3cdd-4773-a61c-3d3b624def52"
STATE_DIR="state/watchdog"; mkdir -p "$STATE_DIR"
ATTEMPT_FILE="${STATE_DIR}/${TODAY}.attempts"
LOG="${STATE_DIR}/${TODAY}.log"

log(){ echo "[watchdog $(date +%H:%M:%S)] $*" | tee -a "$LOG"; }

json_ok(){ [ -f "$JSON" ] && [ "$(stat -c%s "$JSON" 2>/dev/null || echo 0)" -gt 8192 ]; }

site_ok(){
  local html
  html=$(curl -s -m 30 -x "$PROXY" https://aidigest.club/ 2>/dev/null) || html=$(curl -s -m 30 https://aidigest.club/ 2>/dev/null) || return 1
  echo "$html" | grep -q "$TODAY"
}

push_daily(){
  # 幂等：只提交日报相关文件；无变更时跳过 commit 直接 push
  # 分开 add：git add 多 pathspec 时任一不存在会整体失败（2026-09-24 血泪教训）
  git add "$JSON" 2>/dev/null || true
  git add "state/reads-candidates/${TODAY}.json" 2>/dev/null || true
  if ! git diff --cached --quiet 2>/dev/null; then
    git commit -m "feat(daily): AI 日报 ${TODAY}（watchdog 代推）" >>"$LOG" 2>&1
  fi
  git push origin main >>"$LOG" 2>&1
}

attempts(){ cat "$ATTEMPT_FILE" 2>/dev/null || echo 0; }

# ---------- 主逻辑 ----------
if json_ok; then
  if site_ok; then
    log "WD_OK json=$(stat -c%s "$JSON") site=fresh"
    exit 0
  fi
  # JSON 在、站点旧 → 确定性代推（覆盖 push 断掉的场景）
  log "JSON 在但站点未含 ${TODAY}，执行代推"
  if ! push_daily; then
    log "WD_PUSH_FAILED git push 失败，见 $LOG"
    exit 2
  fi
  # 等 GH Pages build（最多 8 分钟，每 60s 查一次）
  for i in 1 2 3 4 5 6 7 8; do
    sleep 60
    if site_ok; then log "WD_HEALED_PUSH 代推成功，站点已恢复（等待 ${i} 分钟）"; exit 0; fi
  done
  log "WD_PUSH_FAILED 代推后 8 分钟站点仍未更新（疑 build 失败），需人工查 GitHub Actions"
  exit 2
fi

# JSON 缺失 → 重跑闭环
N=$(attempts)
if [ "$N" -ge 2 ]; then
  log "WD_ESCALATE 已重跑 ${N} 次仍无 JSON，停止自动重试，需人工介入"
  exit 3
fi
echo $((N+1)) > "$ATTEMPT_FILE"
log "JSON 缺失，触发第 $((N+1)) 次重跑（cron run ${CRON_ID}）"
# 注：openclaw cron run 是异步 enqueue（返回 runId 立即退出），实测确认；下方轮询等待产出
openclaw cron run "$CRON_ID" >>"$LOG" 2>&1
# 等重跑完成（最多 30 分钟，每 2 分钟查一次 JSON；JSON 出现后再给 push+build 留时间）
for i in $(seq 1 15); do
  sleep 120
  if json_ok; then
    log "重跑产出 JSON（等待 $((i*2)) 分钟），再等站点更新"
    for j in 1 2 3 4 5 6; do
      sleep 60
      if site_ok; then log "WD_RERUN_TRIGGERED 第 $((N+1)) 次重跑全程成功，站点已更新"; exit 0; fi
    done
    # 重跑写出 JSON 但又没推（复发今天的断尾）→ 确定性代推
    log "重跑产出 JSON 但站点未更新，watchdog 代推收尾"
    if ! push_daily; then log "WD_PUSH_FAILED git push 失败，见 $LOG"; exit 2; fi
    for j in 1 2 3 4 5 6 7 8; do
      sleep 60
      if site_ok; then log "WD_RERUN_TRIGGERED 重跑+代推成功，站点已更新"; exit 0; fi
    done
    log "WD_PUSH_FAILED 重跑产出 JSON 但代推后站点仍未更新，需人工"
    exit 2
  fi
done
# 30 分钟未见 JSON → 最后再等 15 分钟做一轮终检，避免「重跑慢半拍」留 24h 空窗（MK46 medium-2）
log "30 分钟未见 JSON，最后延长等待 15 分钟做终检"
sleep 900
if json_ok; then
  log "终检发现 JSON 已产出，走代推收尾"
  if ! push_daily; then log "WD_PUSH_FAILED git push 失败，见 $LOG"; exit 2; fi
  for j in 1 2 3 4 5 6 7 8; do
    sleep 60
    if site_ok; then log "WD_RERUN_TRIGGERED 重跑（迟到）+代推成功，站点已更新"; exit 0; fi
  done
  log "WD_PUSH_FAILED 终检代推后站点仍未更新，需人工"
  exit 2
fi
log "WD_ESCALATE 第 $((N+1)) 次重跑触发后 45 分钟仍无 JSON，需人工介入（查主 cron run 日志）"
exit 3
