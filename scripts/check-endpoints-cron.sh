#!/usr/bin/env bash
# ============================================================================
# check-endpoints-cron.sh —— endpoint 健康检查的 cron 包装
# ============================================================================
# 每天 06:05（日报 06:18 之前）探活 LLM endpoint；不健康则通过 OpenClaw
# 发飞书告警给 Jason，便于在日报跑之前就发现 endpoint 故障。
# 健康则静默（不打扰）。
#
# crontab: 5 6 * * *  /root/.openclaw/workspace/projects/ai-daily/scripts/check-endpoints-cron.sh
# ============================================================================

set -uo pipefail
REPO="/root/.openclaw/workspace/projects/ai-daily"
LOG_DIR="$REPO/.cron-logs"
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/check-endpoints-$(date +%Y-%m-%d).log"

JASON_OPENID="ou_dbee86fe0e62ee834c7d7225015a1317"

{
  echo "===== $(date '+%F %T %Z') endpoint 健康检查 ====="
  if OUT=$(bash "$REPO/scripts/check-endpoints.sh" 2>&1); then
    echo "$OUT"
    echo "[check-cron] ✅ 健康，静默退出"
  else
    echo "$OUT"
    echo "[check-cron] ❌ 不健康，发飞书告警"
    # 用 OpenClaw CLI 发飞书消息（如不可用则仅记日志）
    ALERT="🚨 AI 日报 LLM endpoint 健康检查失败（$(date '+%F %T')）

$OUT

→ 改 openclaw.json 的 aigw-claude-48-main provider 切到可用 endpoint。"
    if command -v openclaw >/dev/null 2>&1; then
      openclaw message send --channel feishu --target "user:$JASON_OPENID" --message "$ALERT" 2>&1 || \
        echo "[check-cron] WARN: openclaw message send 失败，仅记日志"
    else
      echo "[check-cron] WARN: openclaw CLI 不可用，仅记日志"
    fi
  fi
  echo "[check-cron] done"
} >>"$LOG" 2>&1
