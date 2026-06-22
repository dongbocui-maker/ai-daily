#!/usr/bin/env bash
# ============================================================================
# check-endpoints.sh —— LLM endpoint 健康检查
# ============================================================================
# 用途：探活 ai-daily 当前使用的 LLM endpoint（从 openclaw.json 解析）。
#       endpoint 挂了立即可见，不必等数据停更数周才发现（对应 6/22 GitHub
#       榜单因 endpoint 关停静默停更 3 周的事故）。
#
# 用法：
#   bash scripts/check-endpoints.sh            # 人工跑，打印结果
#   bash scripts/check-endpoints.sh --quiet    # 只在失败时输出（cron 友好）
#
# 退出码：0 = endpoint 健康；1 = 不健康（cron 可据此告警）。
# ============================================================================

set -uo pipefail
REPO="/root/.openclaw/workspace/projects/ai-daily"
QUIET=0
[[ "${1:-}" == "--quiet" ]] && QUIET=1

log() { [[ $QUIET -eq 0 ]] && echo "$@"; }

# 解析 endpoint
# shellcheck disable=SC1091
if ! source "$REPO/scripts/lib/llm-endpoint.sh" 2>/dev/null; then
  echo "❌ [check-endpoints] LLM endpoint 解析失败（openclaw.json provider 配置异常）"
  exit 1
fi

log "🔍 探活: $LLM_MODEL @ $LLM_API_BASE (protocol=$LLM_PROTOCOL)"

# 构造最小探活请求（anthropic-messages vs openai 两种协议）
HTTP_CODE=""
RESP=""
if [[ "$LLM_PROTOCOL" == "anthropic" ]]; then
  RESP=$(curl -s -m 30 -w '\n%{http_code}' -X POST "$LLM_API_BASE/messages" \
    -H "x-api-key: $LLM_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "Content-Type: application/json" \
    -d "{\"model\":\"$LLM_MODEL\",\"max_tokens\":8,\"messages\":[{\"role\":\"user\",\"content\":\"ping\"}]}" 2>&1)
else
  RESP=$(curl -s -m 30 -w '\n%{http_code}' -X POST "$LLM_API_BASE/chat/completions" \
    -H "Authorization: Bearer $LLM_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"model\":\"$LLM_MODEL\",\"max_tokens\":8,\"messages\":[{\"role\":\"user\",\"content\":\"ping\"}]}" 2>&1)
fi
HTTP_CODE=$(echo "$RESP" | tail -1)

if [[ "$HTTP_CODE" == "200" ]]; then
  log "✅ endpoint 健康 (HTTP 200)"
  exit 0
else
  BODY=$(echo "$RESP" | head -n -1 | head -c 400)
  echo "❌ [check-endpoints] LLM endpoint 不健康！"
  echo "   provider model : $LLM_MODEL"
  echo "   base           : $LLM_API_BASE"
  echo "   HTTP code      : ${HTTP_CODE:-无响应}"
  echo "   响应片段        : $BODY"
  echo "   → 修复：改 openclaw.json 的 aigw-claude-48-main provider，切到可用 endpoint/key"
  exit 1
fi
