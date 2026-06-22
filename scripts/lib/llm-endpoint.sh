#!/usr/bin/env bash
# ============================================================================
# llm-endpoint.sh —— LLM endpoint 单一可信源解析器
# ============================================================================
# 用途：从 OpenClaw 主配置 (openclaw.json) 读取指定 provider 的 endpoint，
#       export 成 LLM_API_BASE / LLM_API_KEY / LLM_MODEL / LLM_PROTOCOL。
#
# 设计目标（B 方案）：以后更换 LLM endpoint 只需改 openclaw.json 一处，
#       ai-daily 的所有脚本（github-trending / sync）与各 OpenClaw agent
#       共用同一份可信源，杜绝散落多处、改一处漏一处的问题。
#
# 用法（在 cron 脚本里）：
#   source "$(dirname "$0")/lib/llm-endpoint.sh"
#   # 之后 LLM_API_BASE / LLM_API_KEY / LLM_MODEL / LLM_PROTOCOL 已就绪
#
# 可选环境变量（覆盖默认）：
#   AI_DAILY_LLM_PROVIDER   默认 aigw-claude-48-main
#   AI_DAILY_LLM_MODEL      默认取该 provider 的第一个 model
#   OPENCLAW_CONFIG         默认 /root/.openclaw/openclaw.json
#
# 退出码：成功 export 后 return 0；解析失败 return 1（调用方应判断并兜底）。
# ============================================================================

_llm_endpoint_resolve() {
  local config="${OPENCLAW_CONFIG:-/root/.openclaw/openclaw.json}"
  local provider="${AI_DAILY_LLM_PROVIDER:-aigw-claude-48-main}"
  local want_model="${AI_DAILY_LLM_MODEL:-}"

  if [[ ! -f "$config" ]]; then
    echo "[llm-endpoint] ERROR: openclaw.json 不存在: $config" >&2
    return 1
  fi

  # 用 python3 从 openclaw.json 解析 provider 的 baseUrl / apiKey / model / api
  local parsed
  parsed=$(python3 - "$config" "$provider" "$want_model" <<'PY'
import json, sys
config_path, provider, want_model = sys.argv[1], sys.argv[2], sys.argv[3]
try:
    d = json.load(open(config_path))
    p = d.get('models', {}).get('providers', {}).get(provider)
    if not p:
        print("ERR|provider 不存在: %s" % provider); sys.exit(0)
    base = p.get('baseUrl', '')
    key  = p.get('apiKey', '')
    api  = p.get('api', '')  # e.g. anthropic-messages / openai
    models = p.get('models', [])
    model = want_model
    if not model:
        if models and isinstance(models[0], dict):
            model = models[0].get('id', '')
        elif models:
            model = str(models[0])
    # protocol: anthropic-messages → anthropic, 其它 → openai
    proto = 'anthropic' if 'anthropic' in api.lower() else 'openai'
    if not base or not key or not model:
        print("ERR|provider 字段不全 (base/key/model 缺失)"); sys.exit(0)
    # 用 \t 分隔输出（值里不会含 tab）
    print("OK|%s\t%s\t%s\t%s" % (base, key, model, proto))
except Exception as e:
    print("ERR|解析异常: %s" % e)
PY
)

  if [[ "$parsed" == ERR\|* ]]; then
    echo "[llm-endpoint] ERROR: ${parsed#ERR|}" >&2
    return 1
  fi
  if [[ "$parsed" != OK\|* ]]; then
    echo "[llm-endpoint] ERROR: 解析返回异常: $parsed" >&2
    return 1
  fi

  local payload="${parsed#OK|}"
  export LLM_API_BASE="$(echo "$payload" | cut -f1)"
  export LLM_API_KEY="$(echo "$payload" | cut -f2)"
  export LLM_MODEL="$(echo "$payload" | cut -f3)"
  export LLM_PROTOCOL="$(echo "$payload" | cut -f4)"

  echo "[llm-endpoint] resolved provider=$provider model=$LLM_MODEL base=$LLM_API_BASE protocol=$LLM_PROTOCOL" >&2
  return 0
}

_llm_endpoint_resolve
