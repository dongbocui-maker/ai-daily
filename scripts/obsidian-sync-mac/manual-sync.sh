#!/usr/bin/env bash
# manual-sync.sh - Obsidian Shell Commands 插件调用的同步脚本
#
# 行为模式（2026-05-18 v3 — 已读不再发）：
#   vault 是「一次性收件箱」——精读首次发到 vault 后，无论你 move/删/改名都不会再发。
#   - 用 ledger（.obsidian-synced-files）记录"已发过的文件名"
#   - ledger 里有的文件 → 永远不再复制（即使 vault 里现在没有）
#   - ledger 里没有的文件 → 发到 vault + 加进 ledger
#   - vault 里已存在的同名文件 → 跳过 + 加进 ledger（不覆盖你的笔记）
#
# 安装在：~/repos/ai-daily/scripts/obsidian-sync-mac/manual-sync.sh
# 调用方式：Obsidian Shell Commands 插件配置这个脚本路径

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

# 如果 ledger 不存在 → 首次跑
# 策略：把 vault 里**当前已存在**的精读全部加入 ledger（视为"已读"），不再复制
# 也把 source 里**任何 vault 已有**的文件加进 ledger
# vault 里没有 + ledger 里没有的 source 文件 → 这次发

FIRST_RUN=0
if [ ! -f "$LEDGER_FILE" ]; then
  FIRST_RUN=1
  touch "$LEDGER_FILE"
  # vault 里现存的精读 → 视为"已读"
  if [ -d "$TARGET_FULL" ]; then
    find "$TARGET_FULL" -maxdepth 1 -name '*.md' -printf '%f\n' >> "$LEDGER_FILE" 2>/dev/null || \
    find "$TARGET_FULL" -maxdepth 1 -name '*.md' -exec basename {} \; >> "$LEDGER_FILE"
  fi
fi

# 读 ledger 到 set（用 bash associative array）
declare -A SYNCED
while IFS= read -r name; do
  [ -n "$name" ] && SYNCED["$name"]=1
done < "$LEDGER_FILE"

# ============ 扫描 source，决定发哪些 ============

declare -a NEW_FILES=()
declare -a SKIPPED_LEDGER=()    # ledger 里有，跳过
declare -a SKIPPED_VAULT_HAS=() # ledger 里没有但 vault 已有同名（加进 ledger + 跳过）

while IFS= read -r -d '' src; do
  filename=$(basename "$src")
  dst="$TARGET_FULL/$filename"

  # 已在 ledger（曾经发过）→ 永远跳过
  if [ "${SYNCED[$filename]:-}" = "1" ]; then
    SKIPPED_LEDGER+=("$filename")
    continue
  fi

  # vault 已有同名文件（ledger 不知道，可能是 ledger 丢了或老用户）
  # → 视为已读，加进 ledger + 跳过
  if [ -f "$dst" ]; then
    SKIPPED_VAULT_HAS+=("$filename")
    SYNCED["$filename"]=1
    echo "$filename" >> "$LEDGER_FILE"
    continue
  fi

  # 真新文件 → 复制 + 加进 ledger
  cp "$src" "$dst"
  NEW_FILES+=("$filename")
  SYNCED["$filename"]=1
  echo "$filename" >> "$LEDGER_FILE"
done < <(find "$REPO_DIR/$SOURCE_SUBDIR" -maxdepth 1 -name '*.md' -print0)

# ============ 汇报 ============

VAULT_TOTAL=$(ls -1 "$TARGET_FULL"/*.md 2>/dev/null | wc -l | tr -d ' ')
LEDGER_TOTAL=$(wc -l < "$LEDGER_FILE" | tr -d ' ')
NEW_COUNT=${#NEW_FILES[@]}

if [ "$FIRST_RUN" = "1" ]; then
  echo "🆕 Ledger 初始化（首次跑新脚本）"
  echo "   将 vault 现存的 ${VAULT_TOTAL} 篇视为「已读」记入 ledger"
fi

if [ "$NEW_COUNT" -eq 0 ]; then
  echo "✅ 没有新精读（vault ${VAULT_TOTAL} 篇 / ledger ${LEDGER_TOTAL} 篇已读）"
else
  echo "✅ 同步完成"
  echo "📥 新增 $NEW_COUNT 篇到 vault："
  for f in "${NEW_FILES[@]}"; do
    echo "  - ${f%.md}"
  done
  echo "📊 vault 当前 ${VAULT_TOTAL} 篇 / ledger ${LEDGER_TOTAL} 篇已读"
fi
