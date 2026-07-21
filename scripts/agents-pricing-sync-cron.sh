#!/usr/bin/env bash
# S.H.R.I.M.P. 单价复核 cron（每周六 10:00，crontab 已引用）。
# 跑 agents-pricing-check.py：抓官方定价页 diff + 检 estimated / stale 价。
# 有异动（退出码 1）→ 推飞书给 Jason，附报告摘要。无异动静默。
# 设计：不自动改价，只提醒；Jason 确认后改 src/data/pricing.json 一处。
set -uo pipefail

REPO=/root/.openclaw/workspace/projects/ai-daily
JASON_OPENID="ou_dbee86fe0e62ee834c7d7225015a1317"
REPORT=/tmp/shrimp-pricing-report.txt

cd "$REPO" || exit 1
echo "[$(date '+%F %T')] pricing check start"

python3 scripts/agents-pricing-check.py
RC=$?

if [ "$RC" -eq 1 ]; then
  # 有异动：推飞书。只发前 ~20 行摘要，避免刷屏。
  SUMMARY=$(grep -A20 '🔴 需人工处理' "$REPORT" 2>/dev/null | head -25)
  [ -z "$SUMMARY" ] && SUMMARY=$(head -30 "$REPORT")
  MSG="💰 单价复核发现异动（每周六自动核对）：

${SUMMARY}

改价：编辑 src/data/pricing.json（single source of truth）→ 更新 price + verified + source。"
  openclaw message send --channel feishu --target "user:$JASON_OPENID" --message "$MSG" 2>&1 \
    || echo "[$(date '+%F %T')] WARN: feishu push 失败，报告仍在 $REPORT"
  echo "[$(date '+%F %T')] pricing drift detected -> pushed feishu"
elif [ "$RC" -eq 0 ]; then
  echo "[$(date '+%F %T')] pricing OK, no drift, silent"
else
  # 脚本自身错误（读不到 pricing.json 等）→ 也告警，属于自我维护范畴
  openclaw message send --channel feishu --target "user:$JASON_OPENID" \
    --message "⚠️ 单价复核脚本异常（rc=$RC），dashboard 成本可能不准，请查 $REPORT" 2>&1 \
    || echo "[$(date '+%F %T')] WARN: feishu push 失败"
  echo "[$(date '+%F %T')] pricing check error rc=$RC"
fi
