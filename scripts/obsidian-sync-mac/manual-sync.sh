#!/usr/bin/env bash
# manual-sync.sh - Obsidian Shell Commands 插件调用的同步脚本
#
# 行为模式（2026-05-18 重构）：
#   vault 是 source 的「收件箱」，不是「镜像」。
#   - 只把 git pull 本次新增/修改的精读 md 复制到 vault
#   - vault 里删了 / move 走了 / 改了的文件——永不被覆盖
#   - vault 里已存在的同名文件——跳过（保留你的笔记/批注）
#   - 上游删除的精读——vault 不动
#
# 安装在：~/repos/ai-daily/scripts/obsidian-sync-mac/manual-sync.sh
# 调用方式：Obsidian Shell Commands 插件配置这个脚本路径

set -euo pipefail

# ============ 配置（必须和 setup.sh 一致） ============

REPO_DIR="$HOME/repos/ai-daily"
VAULT_DIR="$HOME/Library/CloudStorage/OneDrive-Accenture(China)/Desktop/KB/KB"
TARGET_SUBDIR="raw/AI Reads"
TARGET_FULL="$VAULT_DIR/$TARGET_SUBDIR"
STATE_FILE="$REPO_DIR/.obsidian-sync-last-commit"
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

# ============ Git fetch + 计算 diff 范围 ============

cd "$REPO_DIR"

OLD_HEAD=$(git rev-parse HEAD)
git fetch origin main --quiet
NEW_HEAD=$(git rev-parse origin/main)

# 实际同步起点：优先用 state file，没有就用当前 HEAD
if [ -f "$STATE_FILE" ]; then
  SYNC_FROM=$(cat "$STATE_FILE")
  # 验证 SYNC_FROM 是合法 commit；不合法（如 history rewrite）则 fallback
  if ! git cat-file -e "$SYNC_FROM" 2>/dev/null; then
    echo "⚠️  state file 的 commit 已失效，按首次同步处理"
    SYNC_FROM=""
  fi
else
  SYNC_FROM=""
fi

# Pull
if [ "$OLD_HEAD" != "$NEW_HEAD" ]; then
  git reset --hard origin/main --quiet
fi

# 准备目标目录
mkdir -p "$TARGET_FULL"

# ============ 决定要复制哪些文件 ============

declare -a CANDIDATES=()

if [ -z "$SYNC_FROM" ] || [ "$SYNC_FROM" = "$NEW_HEAD" ]; then
  # 情况 A：首次同步（无 state file）
  # 情况 B：state file 等于 HEAD（说明上次已经同步到当前 commit，但可能 vault 缺文件——做一次补齐）
  # 把 obsidian-export/reads/ 下所有 md 当成候选
  FIRST_RUN=1
  while IFS= read -r -d '' f; do
    CANDIDATES+=("$(basename "$f")")
  done < <(find "$REPO_DIR/$SOURCE_SUBDIR" -maxdepth 1 -name '*.md' -print0)
else
  # 情况 C：增量同步
  # 用 git diff 算出 SYNC_FROM..NEW_HEAD 之间 source 路径下的新增/修改
  FIRST_RUN=0
  while IFS= read -r line; do
    status=$(echo "$line" | awk '{print $1}')
    file=$(echo "$line" | awk '{print $2}')
    # 只关心新增(A)和修改(M)；删除(D)和重命名(R)不动 vault
    case "$status" in
      A|M)
        CANDIDATES+=("$(basename "$file")")
        ;;
    esac
  done < <(git diff --name-status "$SYNC_FROM" "$NEW_HEAD" -- "$SOURCE_SUBDIR/" || true)
fi

# ============ 执行复制（跳过 vault 已有的） ============

declare -a NEW_FILES=()
declare -a SKIPPED_EXISTS=()
declare -a SKIPPED_MISSING=()

for filename in "${CANDIDATES[@]}"; do
  src="$REPO_DIR/$SOURCE_SUBDIR/$filename"
  dst="$TARGET_FULL/$filename"

  if [ ! -f "$src" ]; then
    # source 已没了（diff 显示新增/修改但当前 HEAD 已删除——极少见）
    SKIPPED_MISSING+=("$filename")
    continue
  fi

  if [ -f "$dst" ]; then
    # vault 里同名文件已存在——跳过（保留笔记）
    SKIPPED_EXISTS+=("$filename")
    continue
  fi

  # 复制
  cp "$src" "$dst"
  NEW_FILES+=("$filename")
done

# 写入 state file（即使没新增也写，下次基于这个 commit 算 diff）
echo "$NEW_HEAD" > "$STATE_FILE"

# ============ 汇报 ============

TOTAL=$(ls -1 "$TARGET_FULL"/*.md 2>/dev/null | wc -l | tr -d ' ')
NEW_COUNT=${#NEW_FILES[@]}
SKIP_EXISTS_COUNT=${#SKIPPED_EXISTS[@]}

if [ "$FIRST_RUN" = "1" ]; then
  echo "🆕 首次同步（无 state 文件）— 扫描了 ${#CANDIDATES[@]} 个 source 文件"
fi

if [ "$NEW_COUNT" -eq 0 ]; then
  if [ "$SKIP_EXISTS_COUNT" -gt 0 ]; then
    echo "✅ 已是最新（vault 共 ${TOTAL} 篇）— 跳过 ${SKIP_EXISTS_COUNT} 篇 vault 里已有的"
  else
    echo "✅ 已是最新 — vault 共 ${TOTAL} 篇精读"
  fi
else
  echo "✅ 同步完成（vault 共 ${TOTAL} 篇精读）"
  echo "📥 新增 $NEW_COUNT 篇："
  for f in "${NEW_FILES[@]}"; do
    echo "  - ${f%.md}"
  done
  if [ "$SKIP_EXISTS_COUNT" -gt 0 ]; then
    echo "⏭️  跳过 $SKIP_EXISTS_COUNT 篇（vault 里已有，保留你的笔记）"
  fi
fi
