#!/usr/bin/env bash
# setup.sh - Mac 端一次性 setup（纯 F 方案：on-demand 同步）
#
# 做的事：
#   1. clone ai-daily repo 到 ~/repos/
#   2. 首次同步精读到 Obsidian vault
#   3. 给你打印 Shell Commands 插件配置说明
#
# 不做的事：
#   - 不装任何定时任务（launchd / cron）
#   - 不动 OneDrive 同步规则
#
# 同步触发方式：你在 Obsidian 里按快捷键（参考末尾说明配置 Shell Commands 插件）

set -euo pipefail

# ============ 配置区 ============

REPO_URL="https://github.com/dongbocui-maker/ai-daily.git"
REPO_DIR="$HOME/repos/ai-daily"
VAULT_DIR="$HOME/Library/CloudStorage/OneDrive-Accenture(China)/Desktop/KB/KB"
TARGET_SUBDIR="AI 精读"

# ============ 主流程 ============

echo "🚀 aidigest.club → Obsidian 同步 setup（纯按需触发版）"
echo ""

# 1. 检查 vault 存在
if [ ! -d "$VAULT_DIR" ]; then
  echo "❌ Vault 路径不存在: $VAULT_DIR"
  echo "   请确认 OneDrive 已同步 + 路径正确"
  exit 1
fi
echo "✅ Vault 路径: $VAULT_DIR"

# 2. clone repo
if [ -d "$REPO_DIR/.git" ]; then
  echo "✅ Repo 已存在: $REPO_DIR（更新中）"
  cd "$REPO_DIR"
  git fetch origin
  git checkout main
  git reset --hard origin/main
else
  mkdir -p "$(dirname "$REPO_DIR")"
  echo "📥 Clone repo..."
  git clone "$REPO_URL" "$REPO_DIR"
fi

# 3. 第一次跑转换器（如果 markdown 不存在）
cd "$REPO_DIR"
if [ ! -d "obsidian-export/reads" ] || [ -z "$(ls -A obsidian-export/reads 2>/dev/null)" ]; then
  if command -v node >/dev/null 2>&1; then
    echo "🔄 本地生成 markdown..."
    node scripts/reads-to-obsidian.mjs
  else
    echo "⚠️  Node.js 没装——GitHub Actions 会在云端生成，几分钟后再跑一次 setup.sh"
  fi
fi

# 4. 准备 vault 目标目录
TARGET_FULL="$VAULT_DIR/$TARGET_SUBDIR"
mkdir -p "$TARGET_FULL"
echo "✅ Vault 目标目录: $TARGET_FULL"

# 5. 首次 rsync
if [ -d "$REPO_DIR/obsidian-export/reads" ]; then
  echo "📋 首次同步 markdown 到 vault..."
  rsync -av --delete "$REPO_DIR/obsidian-export/reads/" "$TARGET_FULL/" 2>&1 | tail -5
  COUNT=$(ls "$TARGET_FULL"/*.md 2>/dev/null | wc -l | tr -d ' ')
  echo "✅ 已同步 ${COUNT} 篇精读到 vault"
fi

# 6. 打印 Shell Commands 插件配置说明
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "✅ Repo + vault 已就绪"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "📂 同步脚本位置（Obsidian 插件会调用它）："
echo "   ${REPO_DIR}/scripts/obsidian-sync-mac/manual-sync.sh"
echo ""
echo "下一步：在 Obsidian 里配置 Shell Commands 插件"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📌 步骤 1：装 Shell Commands 插件"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  1. 打开 Obsidian → 左下齿轮 (Settings)"
echo "  2. Community plugins → Turn on (如果第一次用)"
echo "  3. Browse → 搜 'Shell commands' (作者 Taitava)"
echo "  4. Install → Enable"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📌 步骤 2：配置同步按钮"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  1. Settings → Shell commands (左侧栏新增项)"
echo "  2. 点 'New shell command'"
echo "  3. 在 Command 框粘贴："
echo ""
echo "     ${REPO_DIR}/scripts/obsidian-sync-mac/manual-sync.sh"
echo ""
echo "  4. 点这条命令展开详细配置："
echo "     - Alias: 🔄 同步 AI 精读"
echo "     - Output channel: Notification balloons"
echo "     - 把 'Confirm before execution' 关闭"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📌 步骤 3：绑快捷键（可选但推荐）"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  1. Settings → Hotkeys"
echo "  2. 搜 '同步 AI 精读' (或 'Shell commands: Execute...')"
echo "  3. 点 + 号 → 按 Cmd+Shift+R (推荐) 或你喜欢的组合"
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "🎉 完成后："
echo "  - 想看新精读 → 按 Cmd+Shift+R → 2 秒后 vault 是最新的"
echo "  - 不按就不动，零后台任务"
echo "═══════════════════════════════════════════════════════════════"
