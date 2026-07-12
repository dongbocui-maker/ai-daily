#!/usr/bin/env bash
# verify-publish.sh — 日报发布结果的确定性校验门（Step I.1 调用）
#
# 用途：日报 cron 子代理在 Step H(cron-sync-event.sh) 跑完 + 等 build 后，
#       用本脚本做**机器判定**（不靠子代理主观感觉）是否真的发布成功。
#       只做「确认发成功」，绝不重新生成/改写内容。
#
# 退出码（Step I 依赖）：
#   exit 0 = 全绿（schema PASS + push 完成 + 站点含当天日期 + 首页可抓）
#   exit 2 = 有内容失败项——stdout 明确列出失败项 + 关键字，供子代理对照 I.2 自愈表：
#            关键字：`schema FAIL`（透传 validate-daily-schema.py 输出）/
#                    `git push 未完成` / `站点未含当天日期` / `线上首页抓取失败`
#   exit 1 = 脚本自身环境异常（python/git 不可用、代理没起导致无法校验），非内容失败
#
# 4 项校验（对齐 I.2 自愈表）：
#   1. schema：validate-daily-schema.py <今天日期>
#   2. git push 完成：origin/main..HEAD 为空 且 src/data/daily 工作区干净
#   3. 站点含当天日期：抓 https://aidigest.club/ 检查 HTML 含 YYYY-MM-DD
#   4. 首页可抓：curl 返回 200 且非空（此项优先于第 3 项——抓不到就没法判断日期）
#
# 参考 cron-sync-event.sh / validate-daily-schema.py 的路径/日期/代理用法保持一致。

set -uo pipefail  # 不用 -e：要能收集多项失败后统一判退出码

REPO="/root/.openclaw/workspace/projects/ai-daily"
TODAY="$(TZ=Asia/Shanghai date +%F)"
SITE_URL="https://aidigest.club/"
PROXY="http://127.0.0.1:7890"

# nvm PATH（与 cron-sync-event.sh 一致，保证 cron 裸 PATH 下也有 node/git）
export NVM_DIR="/root/.nvm"
# shellcheck disable=SC1091
[[ -s "$NVM_DIR/nvm.sh" ]] && . "$NVM_DIR/nvm.sh"
export PATH="/root/.nvm/versions/node/v22.22.2/bin:$PATH"

cd "$REPO" || { echo "[verify] ❌ 环境异常：无法进入 REPO $REPO"; exit 1; }

# 失败收集：CONTENT_FAIL 累计内容失败项数；ENV_FAIL 标记环境异常
CONTENT_FAIL=0
ENV_FAIL=0

echo "[verify] ===== $(date '+%F %T %Z') 发布校验 today=$TODAY ====="

# ── 环境前置检查 ─────────────────────────────────────────
if ! command -v python3 >/dev/null 2>&1; then
  echo "[verify] ❌ 环境异常：python3 不可用"; ENV_FAIL=1
fi
if ! command -v git >/dev/null 2>&1; then
  echo "[verify] ❌ 环境异常：git 不可用"; ENV_FAIL=1
fi
if [[ "$ENV_FAIL" == "1" ]]; then
  echo "[verify] 环境不满足，无法校验，exit 1"
  exit 1
fi

# ── 项 1：schema 校验 ────────────────────────────────────
echo "[verify] --- 项1 schema 校验 (validate-daily-schema.py $TODAY) ---"
SCHEMA_OUT="$(python3 scripts/validate-daily-schema.py "$TODAY" 2>&1)"
SCHEMA_RC=$?
echo "$SCHEMA_OUT"
if [[ "$SCHEMA_RC" -eq 0 ]]; then
  echo "[verify] ✅ 项1 schema"
else
  # 透传原始输出（含 validate-daily-schema.py 的 [TAG] 前缀，如
  # [MISSING_TOP_FIELD]/[ITEM_MISSING_FIELD]/[BODY_TOO_SHORT]/[MISSING_SECTION]/[CLOSING_TOO_FEW] 等），
  # 供子代理对照 I.2 自愈表。关键字 `schema FAIL`。此处直接透传，不过滤方括号/tag。
  echo "schema FAIL: $SCHEMA_OUT"
  echo "[verify] ❌ 项1 schema"
  CONTENT_FAIL=$((CONTENT_FAIL + 1))
fi

# ── 项 2：git push 完成 ──────────────────────────────────
# 需要先 fetch 拿最新 origin 引用才能准确比较 origin/main..HEAD。
# fetch 国内网络可能慢/失败：用 timeout 30 包一下。fetch 本身失败**不算内容 fail**，
# 降级为「跳过 origin/main..HEAD 精确比较」，仅用「工作区是否干净」这一半判断，
# 并把不确定性标为环境异常倾向（见汇总逻辑）——避免因 fetch 抖动误报 push 未完成。
echo "[verify] --- 项2 git push 完成 ---"
FETCH_OK=1
if ! timeout 30 git fetch origin main >/dev/null 2>&1; then
  echo "[verify] ⚠️  git fetch origin main 失败/超时（国内网络），跳过 origin/main..HEAD 精确比较"
  FETCH_OK=0
fi

# 2a. 工作区是否有未提交的 src/data/daily 改动（无论 fetch 成功与否都能判）
DIRTY="$(git status --porcelain src/data/daily 2>/dev/null)"
# 2b. 是否有未推送 commit（依赖 fetch 成功才准确）
UNPUSHED=""
if [[ "$FETCH_OK" == "1" ]]; then
  UNPUSHED="$(git log origin/main..HEAD --oneline 2>/dev/null)"
fi

if [[ -n "$DIRTY" ]]; then
  echo "git push 未完成: src/data/daily 有未提交改动:"
  echo "$DIRTY"
  echo "[verify] ❌ 项2 git push（未提交改动）"
  CONTENT_FAIL=$((CONTENT_FAIL + 1))
elif [[ "$FETCH_OK" == "1" && -n "$UNPUSHED" ]]; then
  echo "git push 未完成: 存在未推送的本地 commit:"
  echo "$UNPUSHED"
  echo "[verify] ❌ 项2 git push（未推送 commit）"
  CONTENT_FAIL=$((CONTENT_FAIL + 1))
elif [[ "$FETCH_OK" == "0" ]]; then
  # 工作区干净但 fetch 失败：无法确认远端是否已同步，标为环境异常而非内容 fail
  echo "[verify] ⚠️  项2 工作区干净，但 fetch 失败无法确认 origin 同步状态（标环境异常）"
  ENV_FAIL=1
else
  echo "[verify] ✅ 项2 git push（工作区干净 + 无未推送 commit）"
fi

# ── 项 4 先行：首页可抓（抓不到就没法判断项 3 日期）────────
echo "[verify] --- 项4 首页可抓 ($SITE_URL 经代理 $PROXY) ---"
# 代理未起 → 抓取项无法进行，算环境异常
if ! ss -tlnp 2>/dev/null | grep -q 7890; then
  echo "[verify] ⚠️  代理 7890 未监听，无法抓取站点（环境异常）"
  ENV_FAIL=1
  SITE_OK=0
else
  HTML_FILE="$(mktemp)"
  HTTP_CODE="$(timeout 40 curl -x "$PROXY" -s --max-time 30 "$SITE_URL" -o "$HTML_FILE" -w '%{http_code}' 2>/dev/null)"
  CURL_RC=$?
  SITE_SIZE="$(wc -c < "$HTML_FILE" 2>/dev/null || echo 0)"
  if [[ "$CURL_RC" -ne 0 || "$HTTP_CODE" != "200" || "$SITE_SIZE" -lt 100 ]]; then
    echo "线上首页抓取失败: curl_rc=$CURL_RC http=$HTTP_CODE size=$SITE_SIZE"
    echo "[verify] ❌ 项4 首页可抓"
    CONTENT_FAIL=$((CONTENT_FAIL + 1))
    SITE_OK=0
  else
    echo "[verify] ✅ 项4 首页可抓 (http=$HTTP_CODE size=$SITE_SIZE)"
    SITE_OK=1
  fi
fi

# ── 项 3：站点含当天日期（依赖项 4 抓取成功）──────────────
echo "[verify] --- 项3 站点含当天日期 ($TODAY) ---"
if [[ "${SITE_OK:-0}" != "1" ]]; then
  echo "[verify] ⚠️  项3 跳过：首页未成功抓取，无法判断日期"
  # 不额外计 CONTENT_FAIL——首页抓取失败已在项4计过（或环境异常）
else
  # 前提：站点 HTML 含 YYYY-MM-DD 格式日期（当前 Astro 渲染确含；若前端改日期格式（如只显示 July 12, 2026）需同步改此匹配）
  if grep -q "$TODAY" "$HTML_FILE"; then
    echo "[verify] ✅ 项3 站点含当天日期 $TODAY"
  else
    echo "站点未含当天日期: 首页 HTML 未匹配 $TODAY（build 可能未完成/失败）"
    echo "[verify] ❌ 项3 站点含当天日期"
    CONTENT_FAIL=$((CONTENT_FAIL + 1))
  fi
fi
# 清理临时文件
[[ -n "${HTML_FILE:-}" && -f "${HTML_FILE:-}" ]] && rm -f "$HTML_FILE"

# ── 汇总：判退出码 ───────────────────────────────────────
echo "[verify] ===== 汇总 content_fail=$CONTENT_FAIL env_fail=$ENV_FAIL ====="
if [[ "$CONTENT_FAIL" -gt 0 ]]; then
  echo "[verify] 结果：有内容失败项，exit 2"
  exit 2
elif [[ "$ENV_FAIL" == "1" ]]; then
  # 无内容 fail 但存在环境不确定（fetch 失败 / 代理没起）→ 无法保证全绿，标环境异常
  echo "[verify] 结果：无内容失败，但存在环境异常（校验不完整），exit 1"
  exit 1
else
  echo "[verify] 结果：全绿，exit 0"
  exit 0
fi
