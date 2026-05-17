#!/usr/bin/env bash
# manual-sync.sh - Obsidian Shell Commands 插件调用的同步脚本
# 单次拉取最新精读到 vault，弹通知告诉你结果
#
# 安装在：~/repos/ai-daily/scripts/obsidian-sync-mac/manual-sync.sh
# 调用方式：在 Obsidian Shell Commands 插件里配置这个脚本路径

set -euo pipefail

# ============ 配置（必须和 setup.sh 一致） ============

REPO_DIR="$HOME/repos/ai-daily"
VAULT_DIR="$HOME/Library/CloudStorage/OneDrive-Accenture(China)/Desktop/KB"
TARGET_SUBDIR="AI 精读"
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

if [ "$OLD_HEAD" = "$NEW_HEAD" ]; then
  echo "✅ 已经是最新 — 没有新精读"
  exit 0
fi

# 看看变化了什么
CHANGED_FILES=$(git diff --name-only "$OLD_HEAD" "$NEW_HEAD" -- 'obsidian-export/reads/' || echo "")
NEW_COUNT=$(git diff --name-only --diff-filter=A "$OLD_HEAD" "$NEW_HEAD" -- 'obsidian-export/reads/' | wc -l | tr -d ' ')
MOD_COUNT=$(git diff --name-only --diff-filter=M "$OLD_HEAD" "$NEW_HEAD" -- 'obsidian-export/reads/' | wc -l | tr -d ' ')

# 执行 pull（用 reset 而不是 merge，避免分叉）
git reset --hard origin/main --quiet

# 准备目标目录
mkdir -p "$TARGET_FULL"

# rsync
rsync -a --delete "$REPO_DIR/obsidian-export/reads/" "$TARGET_FULL/" 2>&1

# 汇报
if [ -z "$CHANGED_FILES" ]; then
  echo "✅ 同步完成 — repo 变了但 obsidian-export/ 没变"
else
  echo "✅ 同步完成"
  if [ "$NEW_COUNT" -gt 0 ]; then
    echo "📥 新增 $NEW_COUNT 篇精读："
    git diff --name-only --diff-filter=A "$OLD_HEAD" "$NEW_HEAD" -- 'obsidian-export/reads/' | sed 's|obsidian-export/reads/|  - |;s|\.md$||'
  fi
  if [ "$MOD_COUNT" -gt 0 ]; then
    echo "✏️  更新 $MOD_COUNT 篇精读"
  fi
fi
