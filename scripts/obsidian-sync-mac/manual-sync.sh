#!/usr/bin/env bash
# manual-sync.sh - Obsidian Shell Commands 插件调用的同步脚本
#
# 行为模式（2026-05-18 v3.1 — 已读不再发，POSIX 兼容）：
#   vault 是「一次性收件箱」——精读首次发到 vault 后，无论你 move/删/改名都不会再发。
#   - 用 ledger（.obsidian-synced-files）记录"已发过的文件名"
#   - ledger 里有的文件 → 永远不再复制（即使 vault 里现在没有）
#   - vault 里已存在的同名文件 → 跳过 + 加进 ledger（不覆盖你的笔记）
#
# 兼容 macOS 自带 bash 3.2（不依赖 declare -A 关联数组）

set -euo pipefail

# ============ 配置（必须和 setup.sh 一致） ============

REPO_DIR="$HOME/repos/ai-daily"
VAULT_DIR="$HOME/Library/CloudStorage/OneDrive-Accenture(China)/Desktop/KB/KB"
TARGET_SUBDIR="raw/AI Reads"
TARGET_FULL="$VAULT_DIR/$TARGET_SUBDIR"
LEDGER_FILE="$REPO_DIR/.obsidian-synced-files"
SOURCE_SUBDIR="obsidian-export/reads"

# ============ 检查 ============

if [ ! -d "$REPO_DIR/.git" ]; then
  echo "❌ Repo 未 setup: $REPO_DIR"
  echo "请先跑 setup.sh"
  exit 1
fi

if [ ! -d "$VAULT_DIR" ]; then
  echo "❌ Vault 路径不存在: $VAULT_DIR"
  exit 1
fi

# ============ Git pull ============

cd "$REPO_DIR"

OLD_HEAD=$(git rev-parse HEAD)
git fetch origin main --quiet
NEW_HEAD=$(git rev-parse origin/main)

if [ "$OLD_HEAD" != "$NEW_HEAD" ]; then
  git reset --hard origin/main --quiet
fi

mkdir -p "$TARGET_FULL"

# ============ Ledger 初始化 ============

FIRST_RUN=0
if [ ! -f "$LEDGER_FILE" ]; then
  FIRST_RUN=1
  : > "$LEDGER_FILE"
  # vault 里现存的精读 → 视为"已读"
  if [ -d "$TARGET_FULL" ]; then
    # 用 find + basename（兼容 BSD find，不用 GNU printf）
    find "$TARGET_FULL" -maxdepth 1 -name '*.md' -print0 2>/dev/null | \
      while IFS= read -r -d '' f; do
        basename "$f"
      done | sort -u > "$LEDGER_FILE"
  fi
fi

# 把 ledger 内容读到一个 sorted 临时文件，待会用 grep -Fxq 查找（兼容 bash 3.2）
LEDGER_SORTED=$(mktemp -t obsidian-sync-ledger.XXXXXX)
trap 'rm -f "$LEDGER_SORTED"' EXIT
sort -u "$LEDGER_FILE" > "$LEDGER_SORTED"

# 计数器和列表（普通数组，bash 3.2 OK）
NEW_FILES=()
SKIPPED_LEDGER_COUNT=0
SKIPPED_VAULT_HAS_COUNT=0

# ============ 扫描 source，决定发哪些 ============

# 用临时文件累积要追加进 ledger 的文件名（避免子 shell pipe 问题）
LEDGER_ADD=$(mktemp -t obsidian-sync-add.XXXXXX)
trap 'rm -f "$LEDGER_SORTED" "$LEDGER_ADD"' EXIT

find "$REPO_DIR/$SOURCE_SUBDIR" -maxdepth 1 -name '*.md' -print0 2>/dev/null | \
while IFS= read -r -d '' src; do
  filename=$(basename "$src")
  dst="$TARGET_FULL/$filename"

  # 已在 ledger（曾经发过）→ 永远跳过
  if grep -Fxq "$filename" "$LEDGER_SORTED"; then
    echo "SKIP_LEDGER:$filename" >> "$LEDGER_ADD.events"
    continue
  fi

  # vault 已有同名文件（ledger 不知道）→ 视为已读，加进 ledger + 跳过
  if [ -f "$dst" ]; then
    echo "SKIP_VAULT:$filename" >> "$LEDGER_ADD.events"
    echo "$filename" >> "$LEDGER_ADD"
    continue
  fi

  # 真新文件 → 复制 + 加进 ledger
  cp "$src" "$dst"
  echo "NEW:$filename" >> "$LEDGER_ADD.events"
  echo "$filename" >> "$LEDGER_ADD"
done

# 把新增的文件名追加进 ledger
if [ -s "$LEDGER_ADD" ]; then
  cat "$LEDGER_ADD" >> "$LEDGER_FILE"
fi

# ============ 汇总事件 ============

NEW_COUNT=0
if [ -f "$LEDGER_ADD.events" ]; then
  NEW_COUNT=$(grep -c '^NEW:' "$LEDGER_ADD.events" 2>/dev/null || true)
  SKIPPED_LEDGER_COUNT=$(grep -c '^SKIP_LEDGER:' "$LEDGER_ADD.events" 2>/dev/null || true)
  SKIPPED_VAULT_HAS_COUNT=$(grep -c '^SKIP_VAULT:' "$LEDGER_ADD.events" 2>/dev/null || true)
fi

VAULT_TOTAL=$(ls -1 "$TARGET_FULL"/*.md 2>/dev/null | wc -l | tr -d ' ')
LEDGER_TOTAL=$(wc -l < "$LEDGER_FILE" | tr -d ' ')

# ============ 汇报 ============

if [ "$FIRST_RUN" = "1" ]; then
  echo "🆕 Ledger 初始化（首次跑新脚本）"
  echo "   将 vault 现存的 ${VAULT_TOTAL} 篇视为「已读」记入 ledger"
fi

if [ "$NEW_COUNT" -eq 0 ]; then
  echo "✅ 没有新精读（vault ${VAULT_TOTAL} 篇 / ledger ${LEDGER_TOTAL} 篇已读）"
else
  echo "✅ 同步完成"
  echo "📥 新增 $NEW_COUNT 篇到 vault："
  grep '^NEW:' "$LEDGER_ADD.events" 2>/dev/null | sed 's/^NEW:/  - /' | sed 's/\.md$//'
  echo "📊 vault ${VAULT_TOTAL} 篇 / ledger ${LEDGER_TOTAL} 篇已读"
fi

# 清理
rm -f "$LEDGER_ADD.events"
