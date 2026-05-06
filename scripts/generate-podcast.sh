#!/bin/bash
# generate-podcast.sh — 单篇精读 → NotebookLM 播客 → COS → 网站 全自动化
#
# 用法：
#   ./generate-podcast.sh <slug>
#   ./generate-podcast.sh karpathy-agi-decade-away
#
# 流程：
#   1. 检查/创建本月 notebook（命名：AI 日报精读 YYYY-MM）
#   2. 把精读 JSON 转成中文 markdown
#   3. notebooklm source add → 拿 source-id
#   4. notebooklm generate audio -s <source-id> --wait → 拿 artifact-id
#   5. notebooklm download audio → /tmp/<slug>.m4a
#   6. publish-audio.sh reads <m4a> <slug> → 上传 COS + 写回 JSON
#
# 关键铁律（MEMORY.md 已记录）：
#   - 月度 notebook（不是每篇一个）
#   - 必须 -s <source-id> 锁定本篇 source（不能全选）
#
# 返回码：0 成功 / 1 失败 / 2 部分失败（例如音频生成 OK 但发布失败，留有 m4a）

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NOTEBOOKLM="/root/.openclaw/workspace/projects/ai-fireside/.venv/bin/notebooklm"
PROXY="http://127.0.0.1:7890"

# ===== 参数 =====
if [[ $# -ne 1 ]]; then
    echo "用法：$0 <slug>" >&2
    exit 1
fi
SLUG="$1"
MONTH=$(TZ=Asia/Shanghai date +%Y-%m)
NOTEBOOK_TITLE="AI 日报精读 ${MONTH}"
WORK_DIR=$(mktemp -d -t podcast-${SLUG}-XXXXXX)
SOURCE_MD="${WORK_DIR}/source.md"
AUDIO_FILE="${WORK_DIR}/podcast.m4a"

trap 'echo "[!] 工作目录保留：$WORK_DIR" >&2' EXIT

# ===== 启动 mihomo =====
if ! pgrep mihomo > /dev/null; then
    nohup /usr/local/bin/mihomo -d /root/.config/mihomo > /root/.config/mihomo/mihomo.log 2>&1 &
    sleep 3
fi
export HTTPS_PROXY="$PROXY"
export HTTP_PROXY="$PROXY"

echo "===================================================================" >&2
echo "🎙️  生成精读播客：$SLUG" >&2
echo "📂  本月 notebook：$NOTEBOOK_TITLE" >&2
echo "📁  工作目录：$WORK_DIR" >&2
echo "===================================================================" >&2

# ===== Step 1: 检查/创建本月 notebook =====
echo "" >&2
echo "[1/6] 检查本月 notebook..." >&2
NOTEBOOK_ID=$($NOTEBOOKLM list --json 2>/dev/null \
    | python3 -c "
import sys, json
data = json.load(sys.stdin)
items = data if isinstance(data, list) else data.get('notebooks', [])
for n in items:
    if n.get('title') == '${NOTEBOOK_TITLE}':
        print(n['id'])
        break
" || echo "")

if [[ -z "$NOTEBOOK_ID" ]]; then
    echo "  → 本月 notebook 不存在，创建中..." >&2
    $NOTEBOOKLM create "$NOTEBOOK_TITLE" 2>&1 | head -3 >&2
    # 创建后重查（获取 ID 最可靠的方式）
    NOTEBOOK_ID=$($NOTEBOOKLM list --json 2>/dev/null \
        | python3 -c "
import sys, json
data = json.load(sys.stdin)
items = data if isinstance(data, list) else data.get('notebooks', [])
for n in items:
    if n.get('title') == '${NOTEBOOK_TITLE}':
        print(n['id']); break
")
    if [[ -z "$NOTEBOOK_ID" ]]; then
        echo "ERROR: 创建后重查仍未找到 notebook" >&2
        exit 1
    fi
    echo "  ✅ 创建成功：$NOTEBOOK_ID" >&2
else
    echo "  ✅ 已存在：$NOTEBOOK_ID" >&2
fi

# 切到这个 notebook 作为当前 context
$NOTEBOOKLM use "$NOTEBOOK_ID" 2>&1 | head -3 >&2

# ===== Step 2: 精读 JSON → markdown =====
echo "" >&2
echo "[2/6] 精读 JSON → source markdown..." >&2
python3 "$SCRIPT_DIR/build-podcast-source.py" "$SLUG" -o "$SOURCE_MD"

# 拿标题作为 source title
SOURCE_TITLE=$(python3 -c "
import json, glob
fp = glob.glob('${SCRIPT_DIR%/scripts}/src/data/reads/*-${SLUG}.json')[0]
print(json.load(open(fp))['titleZh'])
")
echo "  source title: $SOURCE_TITLE" >&2

# ===== Step 3: 加 source（如果已存在同名 source 则复用）=====
# CLI 语义：`source add <文件路径>` 直接传路径（不是 --file）。
echo "" >&2
echo "[3/6] 添加 source 到 notebook..." >&2

# 检查是否已有同名 source（重跑场景）
EXISTING_SOURCE_ID=$($NOTEBOOKLM source list --json 2>/dev/null | python3 -c "
import sys, json
data = json.load(sys.stdin)
for s in data.get('sources', []):
    if s.get('title') == '${SOURCE_TITLE}':
        print(s['id']); break
")

if [[ -n "$EXISTING_SOURCE_ID" ]]; then
    SOURCE_ID="$EXISTING_SOURCE_ID"
    echo "  ♻️  同名 source 已存在，复用：$SOURCE_ID" >&2
    SKIP_RENAME=1
else
    SKIP_RENAME=0
    # 重命名 markdown，让 source title 更贴近中文标题
    NAMED_MD="${WORK_DIR}/${SOURCE_TITLE}.md"
    cp "$SOURCE_MD" "$NAMED_MD"

    SOURCE_ADD_JSON=$($NOTEBOOKLM source add "$NAMED_MD" --json 2>&1)
SOURCE_ID=$(echo "$SOURCE_ADD_JSON" | python3 -c "
import sys, json
try:
    data = json.loads(sys.stdin.read())
except Exception as e:
    print(f'ERROR parsing source-add output: {e}', file=sys.stderr)
    sys.exit(1)
sid = (data.get('source') or {}).get('id') or data.get('id')
if not sid:
    print('ERROR: no source id in response', file=sys.stderr)
    print(json.dumps(data, indent=2)[:1500], file=sys.stderr)
    sys.exit(1)
print(sid)
")
    echo "  ✅ source-id: $SOURCE_ID" >&2
fi

# 试图重命名 source title（有 rename 命令）——不作为硬要求，失败不阉
if [[ "$SKIP_RENAME" != "1" && -n "$SOURCE_TITLE" ]]; then
    $NOTEBOOKLM source rename "$SOURCE_ID" "$SOURCE_TITLE" 2>&1 | head -2 >&2 || true
fi

# 等 source 索引完成（NotebookLM 内部要 fulltext 索引）
echo "  → 等 source 索引完成（最多 60 秒）..." >&2
$NOTEBOOKLM source wait "$SOURCE_ID" --timeout 90 2>&1 | head -3 >&2 || echo "  ⚠️ wait 超时但继续（NotebookLM 一般也能用）" >&2

# ===== Step 4: 生成 audio（关键：-s <source-id> 锁定单篇）=====
echo "" >&2
echo "[4/6] 生成播客（deep-dive long zh，-s 锁定本篇 source）..." >&2
echo "  ⏳ 预计 15-25 分钟，请耐心等待..." >&2

ARTIFACT_JSON=$($NOTEBOOKLM generate audio \
    -s "$SOURCE_ID" \
    --format deep-dive \
    --length long \
    --language zh_Hans \
    --wait \
    --retry 2 \
    --json \
    "中文深度讲解《${SOURCE_TITLE}》核心观点，双主持人对谈风格，深入分析作者论点、关键论据、行业影响、对企业 AI 落地的启示" 2>&1)

ARTIFACT_ID=$(echo "$ARTIFACT_JSON" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    aid = data.get('id') or (data.get('artifact') or {}).get('id')
    if not aid:
        print('ERROR: no artifact id', file=sys.stderr)
        print(json.dumps(data, indent=2)[:2000], file=sys.stderr)
        sys.exit(1)
    print(aid)
except Exception as e:
    print(f'ERROR parsing artifact json: {e}', file=sys.stderr)
    sys.exit(1)
")
echo "  ✅ artifact-id: $ARTIFACT_ID" >&2

# ===== Step 5: 下载 m4a =====
echo "" >&2
echo "[5/6] 下载 m4a..." >&2
$NOTEBOOKLM download audio "$ARTIFACT_ID" -o "$AUDIO_FILE" 2>&1 | tail -3 >&2

if [[ ! -f "$AUDIO_FILE" ]]; then
    echo "ERROR: 下载失败，文件不存在：$AUDIO_FILE" >&2
    exit 2
fi
SIZE_MB=$(du -m "$AUDIO_FILE" | cut -f1)
echo "  ✅ 下载完成：$AUDIO_FILE（${SIZE_MB} MB）" >&2

# ===== Step 6: 上传 COS + 写回 JSON =====
echo "" >&2
echo "[6/6] 上传到 COS + 写回 reads JSON..." >&2
"$SCRIPT_DIR/publish-audio.sh" reads "$AUDIO_FILE" "$SLUG"

echo "" >&2
echo "===================================================================" >&2
echo "🎉 全流程完成！" >&2
echo "===================================================================" >&2
echo "Slug:        $SLUG" >&2
echo "Notebook:    $NOTEBOOK_TITLE ($NOTEBOOK_ID)" >&2
echo "Source ID:   $SOURCE_ID" >&2
echo "Artifact ID: $ARTIFACT_ID" >&2
echo "Local m4a:   $AUDIO_FILE（${SIZE_MB} MB，保留供调试）" >&2
echo "===================================================================" >&2

# 不清理工作目录——留着调试。手动清理：rm -rf $WORK_DIR
trap - EXIT
