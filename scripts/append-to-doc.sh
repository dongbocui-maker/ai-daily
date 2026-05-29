#!/bin/bash
# append-to-doc.sh - 用主钢铁虾 App tenant token 把 markdown 追加到飞书文档
#
# 用途：替代 cron 里 feishu_doc append 调用，避免 MK2 App 权限不足问题
# 2026-05-29 立，因 5/26-5/29 MK2 App 对文档无写权限导致 cron 失败
#
# Usage: ./append-to-doc.sh <markdown_file> <doc_token>
# Returns: 0 on success, non-zero on failure

set -euo pipefail

MARKDOWN_FILE="${1:?Usage: $0 <markdown_file> <doc_token>}"
DOC_TOKEN="${2:?Usage: $0 <markdown_file> <doc_token>}"

if [ ! -f "$MARKDOWN_FILE" ]; then
  echo "ERROR: markdown file not found: $MARKDOWN_FILE" >&2
  exit 1
fi

# 从 ~/.openclaw/openclaw.json 读主钢铁虾 App credentials（避免硬编码 secret）
CREDS=$(python3 <<'EOF'
import json
with open('/root/.openclaw/openclaw.json') as f:
    cfg = json.load(f)
# 主钢铁虾 App config 在 channels.feishu 顶层
feishu = cfg.get('channels', {}).get('feishu', {})
app_id = feishu.get('appId', '')
app_secret = feishu.get('appSecret', '')
print(f"{app_id}|{app_secret}")
EOF
)

MAIN_APP_ID="${CREDS%|*}"
MAIN_APP_SECRET="${CREDS#*|}"

if [ -z "$MAIN_APP_ID" ] || [ -z "$MAIN_APP_SECRET" ]; then
  echo "ERROR: failed to load main app credentials from openclaw.json" >&2
  exit 2
fi

# 获取 tenant_access_token
TOKEN=$(curl -s -X POST 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal' \
  -H 'Content-Type: application/json' \
  -d "{\"app_id\":\"$MAIN_APP_ID\",\"app_secret\":\"$MAIN_APP_SECRET\"}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin).get('tenant_access_token',''))")

if [ -z "$TOKEN" ]; then
  echo "ERROR: failed to obtain tenant_access_token" >&2
  exit 3
fi

# 调用 markdown → blocks 转换 API
CONVERT_PAYLOAD=$(python3 -c "
import json, sys
content = open('$MARKDOWN_FILE').read()
payload = {
  'content_type': 'markdown',
  'content': content
}
print(json.dumps(payload, ensure_ascii=False))
")

CONVERT_RESP=$(curl -s -X POST 'https://open.feishu.cn/open-apis/docx/v1/documents/blocks/convert' \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "$CONVERT_PAYLOAD")

CONVERT_CODE=$(echo "$CONVERT_RESP" | python3 -c "import sys,json; print(json.load(sys.stdin).get('code', -1))")
if [ "$CONVERT_CODE" != "0" ]; then
  echo "ERROR: convert markdown failed: $CONVERT_RESP" >&2
  exit 4
fi

# 提取 blocks 数组并构建 children create payload
BLOCKS_PAYLOAD=$(echo "$CONVERT_RESP" | python3 -c "
import json, sys
d = json.load(sys.stdin)
blocks = d.get('data', {}).get('blocks', [])
payload = {
  'children': blocks,
  'index': -1
}
print(json.dumps(payload, ensure_ascii=False))
")

APPEND_RESP=$(curl -s -X POST "https://open.feishu.cn/open-apis/docx/v1/documents/$DOC_TOKEN/blocks/$DOC_TOKEN/children" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "$BLOCKS_PAYLOAD")

APPEND_CODE=$(echo "$APPEND_RESP" | python3 -c "import sys,json; print(json.load(sys.stdin).get('code', -1))")
if [ "$APPEND_CODE" != "0" ]; then
  echo "ERROR: append failed: $APPEND_RESP" >&2
  exit 5
fi

BLOCKS_ADDED=$(echo "$APPEND_RESP" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(len(d.get('data', {}).get('children', [])))
")

echo "OK: appended $BLOCKS_ADDED blocks to doc $DOC_TOKEN"
exit 0
