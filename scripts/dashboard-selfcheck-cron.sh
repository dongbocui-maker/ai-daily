#!/usr/bin/env bash
# S.H.R.I.M.P. Dashboard 每日自检 cron。
# 跑 dashboard-selfcheck.py：dead-link / stale-data / unpriced / config-drift。
# 有异常（rc=1）→ 推飞书给 Jason，附异常清单。健康则静默。
set -uo pipefail

# cron 裸 PATH 没有 node，openclaw CLI (pnpm shim) 需要它（2026-11-21 修：node: not found 导致 11-16 起自检告警 6 天没推出去；同 agents-pricing-sync-cron.sh 2026-09-12 的修法）
export PATH="/root/.nvm/versions/node/v22.22.2/bin:$PATH"

REPO=/root/.openclaw/workspace/projects/ai-daily
JASON_OPENID="ou_dbee86fe0e62ee834c7d7225015a1317"
REPORT=/tmp/shrimp-selfcheck-report.txt

cd "$REPO" || exit 1
echo "[$(date '+%F %T')] dashboard selfcheck start"

python3 scripts/dashboard-selfcheck.py
RC=$?

if [ "$RC" -eq 1 ]; then
  SUMMARY=$(grep -A30 '🔴' "$REPORT" 2>/dev/null | head -35)
  [ -z "$SUMMARY" ] && SUMMARY=$(head -40 "$REPORT")
  MSG="🩺 Dashboard 自检发现异常（每日自动体检）：

${SUMMARY}

详细报告：${REPORT}（VM 本地）"
  if openclaw message send --channel feishu --target "user:$JASON_OPENID" --message "$MSG" 2>&1; then
    echo "[$(date '+%F %T')] selfcheck found issues -> pushed feishu"
  else
    echo "[$(date '+%F %T')] WARN: selfcheck found issues but feishu push FAILED，报告在 $REPORT"
  fi
else
  echo "[$(date '+%F %T')] selfcheck healthy, silent"
fi
