#!/usr/bin/env bash
# manual-sync.sh - Obsidian Shell Commands 插件调用的同步脚本
# 单次拉取最新精读到 vault，弹通知告诉你结果
#
# 安装在：~/repos/ai-daily/scripts/obsidian-sync-mac/manual-sync.sh
# 调用方式：在 Obsidian Shell Commands 插件里配置这个脚本路径

set -euo pipefail

# ============ 配置（必须和 setup.sh 一致） ============

REPO_DIR="$HOME/repos/ai-daily"
VAULT_DIR="$HOME/Library/CloudStorage/OneDrive-Accenture(China)/Desktop/KB/KB"
TARGET_SUBDIR="raw/AI Reads"
TARGET_FULL="$VAULT_DIR/$TARGET_SUBDIR"

# ============ 主流程 ============

# 检查 repo
if [ ! -d "$REPO_DIR/.git" ]; then
  echo "❌ Repo 未 setup: $REPO_DIR"
  echo "请先跑 setup.sh"
  exit 1
fi

# 检查 vault
if [ ! -d "$VAULT_DIR" ]; then
  echo "❌ Vault 路径不存在: $VAULT_DIR"
  exit 1
fi

# 记录 pull 前的 commit
cd "$REPO_DIR"
OLD_HEAD=$(git rev-parse HEAD)

# Pull
git fetch origin main --quiet
NEW_HEAD=$(git rev-parse origin/main)

# 执行 pull（用 reset 避免分叉）
if [ "$OLD_HEAD" != "$NEW_HEAD" ]; then
  git reset --hard origin/main --quiet
fi

# 准备目标目录
mkdir -p "$TARGET_FULL"

# 总是跑 rsync（不依赖 git diff）——防止 "git 拉了但 vault 没同步" 的问题
# 用 -i 选项能输出变化的文件
RSYNC_OUT=$(rsync -avi --delete "$REPO_DIR/obsidian-export/reads/" "$TARGET_FULL/" 2>&1)
NEW_FILES=$(echo "$RSYNC_OUT" | grep '^>f+++++++++' | awk '{print $2}' | sed 's|\.md$||')
MOD_FILES=$(echo "$RSYNC_OUT" | grep '^>f\.st\.\.\.\.\.' | awk '{print $2}' | sed 's|\.md$||')
DEL_FILES=$(echo "$RSYNC_OUT" | grep '^\*deleting' | awk '{print $2}' | sed 's|\.md$||')

# 汇报
NEW_COUNT=$(echo "$NEW_FILES" | grep -c . || true)
MOD_COUNT=$(echo "$MOD_FILES" | grep -c . || true)
DEL_COUNT=$(echo "$DEL_FILES" | grep -c . || true)
TOTAL=$(ls -1 "$TARGET_FULL"/*.md 2>/dev/null | wc -l | tr -d ' ')

if [ "$NEW_COUNT" -eq 0 ] && [ "$MOD_COUNT" -eq 0 ] && [ "$DEL_COUNT" -eq 0 ]; then
  echo "✅ 已经是最新 — vault 里共 ${TOTAL} 篇精读"
else
  echo "✅ 同步完成（vault 里现有 ${TOTAL} 篇精读）"
  if [ "$NEW_COUNT" -gt 0 ]; then
    echo "📥 新增 $NEW_COUNT 篇："
    echo "$NEW_FILES" | sed 's/^/  - /'
  fi
  if [ "$MOD_COUNT" -gt 0 ]; then
    echo "✏️  更新 $MOD_COUNT 篇"
  fi
  if [ "$DEL_COUNT" -gt 0 ]; then
    echo "🗑️  删除 $DEL_COUNT 篇"
  fi
fi
