#!/usr/bin/env bash
# fetch-lmarena.sh — LMArena 月度抓取脚本（决策 3：完全自动化）
#
# 流程：开 mihomo → 抓 arena.ai/leaderboard → 解析 RSC payload → 写 snapshot →
#       关 mihomo → git commit + push
#
# 触发：OpenClaw cron 每月 1 日 09:00
# 失败：以非零退出码退出，stderr 日志会被 cron 捕获给 heartbeat 通知

set -euo pipefail

# 路径配置
# cron 环境 PATH 不含 nvm/pnpm（2026-07-01 build 失败教训），显式补 PATH
export PATH="/root/.nvm/versions/node/v22.22.2/bin:$PATH"
PROJECT_DIR="/root/.openclaw/workspace/projects/ai-daily"
SNAPSHOTS_DIR="$PROJECT_DIR/src/data/lmarena/snapshots"
MIHOMO_BIN="/usr/local/bin/mihomo"
MIHOMO_CONFIG_DIR="/root/.config/mihomo"
LOG_FILE="$MIHOMO_CONFIG_DIR/fetch-lmarena.log"
DATE=$(date +%Y-%m-%d)
SNAPSHOT_FILE="$SNAPSHOTS_DIR/${DATE}.json"
TMP_HTML="/tmp/lmarena-fetch-${DATE}.html"
TMP_JSON="/tmp/lmarena-fetch-${DATE}.json"

# 日志函数
log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

cleanup() {
  log "🧹 清理：关闭 mihomo + 删除临时文件"
  pkill mihomo 2>/dev/null || true
  rm -f "$TMP_HTML" "$TMP_JSON"
}
trap cleanup EXIT

log "===== LMArena 月度抓取启动（$DATE）====="

# Step 1: 启动 mihomo
log "🚀 Step 1: 启动 mihomo 代理"
if [ ! -x "$MIHOMO_BIN" ]; then
  log "❌ mihomo 二进制不存在：$MIHOMO_BIN"
  exit 2
fi
nohup "$MIHOMO_BIN" -d "$MIHOMO_CONFIG_DIR" > "$MIHOMO_CONFIG_DIR/mihomo.log" 2>&1 &
sleep 5

# 验证代理启动
if ! ss -tlnp 2>/dev/null | grep -q "127.0.0.1:7890"; then
  log "❌ mihomo 启动失败（端口 7890 未监听）"
  tail -20 "$MIHOMO_CONFIG_DIR/mihomo.log" | tee -a "$LOG_FILE"
  exit 3
fi
log "✅ mihomo 已启动，监听 127.0.0.1:7890"

# Step 2: 抓 leaderboard
# 注：2026-06 LMArena 域名从 lmarena.ai 迁移到 arena.ai（301 永久重定向）。
# 加 -L 跟随重定向作为双保险，万一域名再变也能跟上。
log "🌐 Step 2: 抓 arena.ai/leaderboard"
HTTP_CODE=$(curl -sS -L -o "$TMP_HTML" -w "%{http_code}" \
  -x http://127.0.0.1:7890 \
  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/130.0.0.0 Safari/537.36" \
  --max-time 60 \
  "https://arena.ai/leaderboard")

if [ "$HTTP_CODE" != "200" ]; then
  log "❌ 抓取失败：HTTP $HTTP_CODE"
  exit 4
fi

SIZE=$(stat -c%s "$TMP_HTML")
log "✅ 抓取成功：HTTP $HTTP_CODE，大小 $SIZE bytes"

if [ "$SIZE" -lt 1000000 ]; then
  log "⚠️  文件大小异常（< 1MB），可能页面结构变化"
  exit 5
fi

# Step 3: 解析 + 写 snapshot
log "🔍 Step 3: 解析 RSC payload + 生成 snapshot"
python3 "$PROJECT_DIR/scripts/parse-lmarena.py" "$TMP_HTML" "$SNAPSHOT_FILE" "$DATE"

if [ ! -f "$SNAPSHOT_FILE" ]; then
  log "❌ snapshot 文件未生成：$SNAPSHOT_FILE"
  exit 6
fi

MODEL_COUNT=$(python3 -c "import json; d=json.load(open('$SNAPSHOT_FILE')); print(d['totalModelsShown'])")
log "✅ snapshot 写入完成：$SNAPSHOT_FILE（Top $MODEL_COUNT）"

# 注：mihomo 不在这里关！GitHub push 走 mihomo 代理（127.0.0.1:7890），
# 提前关会导致 Step 6 push 无代理失败。统一在 push 之后关（trap 也会兑底）。

# Step 5: build + commit + push
log "🛠️  Step 5: pnpm build"
cd "$PROJECT_DIR"
if ! pnpm build > /tmp/lmarena-build.log 2>&1; then
  log "❌ build 失败"
  tail -30 /tmp/lmarena-build.log | tee -a "$LOG_FILE"
  exit 7
fi
log "✅ build 通过"

log "📤 Step 6: git commit + push"
cd "$PROJECT_DIR"
git add "src/data/lmarena/snapshots/${DATE}.json"
if git diff --cached --quiet; then
  log "ℹ️  无新增/变更，跳过 commit"
else
  git commit -m "chore(lmarena): 月度榜单 ${DATE}" -m "🤖 自动抓取自 arena.ai/leaderboard"
  # push 重试 3 次（国内 GitHub push 不稳定）
  for i in 1 2 3; do
    if git push origin main; then
      log "✅ push 成功（第 $i 次尝试）"
      break
    fi
    log "⚠️  push 失败（第 $i 次），10 秒后重试"
    sleep 10
  done
fi

# Step 7: 关 mihomo（push 完成后才关）
log "🔌 Step 7: 关闭 mihomo"
pkill mihomo 2>/dev/null || true
sleep 1

log "===== ✅ LMArena 月度抓取完成 ====="
echo "::lmarena-snapshot-date::$DATE"
echo "::lmarena-model-count::$MODEL_COUNT"
