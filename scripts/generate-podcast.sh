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

# 失败诊断 trap：保留工作目录 + dump 任何 stderr 文件
on_exit() {
    local code=$?
    if [[ $code -ne 0 ]]; then
        echo "" >&2
        echo "==== ❌ 脚本异常退出（code=$code）====" >&2
        echo "工作目录：$WORK_DIR" >&2
        for f in "$WORK_DIR"/*.stderr; do
            [[ -f "$f" ]] || continue
            echo "---- $(basename $f) ----" >&2
            cat "$f" >&2
            echo "-------------------------" >&2
        done
        echo "==== 诊断信息结束 ====" >&2
    else
        echo "[i] 工作目录保留：$WORK_DIR" >&2
    fi
}
trap on_exit EXIT

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

    # 关键：stderr 单独存文件，stdout 拿干净的 JSON
    SOURCE_ADD_JSON=$($NOTEBOOKLM source add "$NAMED_MD" --json 2>"$WORK_DIR/source-add.stderr")
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

# ===== Step 4: 生成 audio（task_id 直接关联策略，2026-05-06 重写）=====
#
# 重大发现：NotebookLM CLI 返回的 task_id 就等于 artifact_id！
# 这意味着可以彻底消除并行竞态：
#   1. generate audio --json → 拿 task_id（= artifact_id）
#   2. artifact wait <task_id> --timeout N → 阻塞等 completed
#   3. download audio -a <task_id> → 下载
#
# 之前的 snapshot before/after 策略在并行场景有 bug：两个进程同时
# snapshot 时 BEFORE 集相同，会都把对方的新 artifact 当成自己的。
# task_id 是确定性的强关联，不存在这个问题。

echo "" >&2
echo "[4/6] 启动 generate audio（deep-dive long zh）..." >&2

# Step 4a: PROMPT（Jason 2026-05-06 拍板的铁律）
PROMPT="这期播客介绍《${SOURCE_TITLE}》。中文双主持人对谈，深度阐释原文。

严格要求：
1. 本期节目标题必须是《${SOURCE_TITLE}》。不要重写、不要改名、不要起别的名字。
2. 所有论点、数据、例子、引言、背景信息都必须严格出自原文。不准编原文未讲过的内容。
3. 可以重述、阐释、讨论原文观点，但不准联想、不准类比到原文未提的例子、不准「补充背景」。
4. 如果原文某个点介绍不够详细，说「作者未详述」即可，不准填补。
风格：严谨专业、信息密集、面向专业人士，不要闲聊化。"

# Step 4b: 启动 generate audio --json，提取 task_id
set +e
$NOTEBOOKLM generate audio \
    -s "$SOURCE_ID" \
    --format deep-dive \
    --length long \
    --language zh_Hans \
    --json \
    "$PROMPT" \
    > "$WORK_DIR/generate-audio.stdout" 2>"$WORK_DIR/generate-audio.stderr"
GEN_RC=$?
set -e

if [[ $GEN_RC -ne 0 ]]; then
    echo "  ❌ generate audio 调用失败 rc=$GEN_RC" >&2
    cat "$WORK_DIR/generate-audio.stderr" >&2 || true
    exit 2
fi

TASK_ID=$(python3 -c "
import json, sys
try:
    with open('$WORK_DIR/generate-audio.stdout') as f:
        data = json.load(f)
    print(data.get('task_id', ''))
except Exception as e:
    print('', end='')
")

if [[ -z "$TASK_ID" ]]; then
    echo "  ❌ 从 generate audio 输出提不出 task_id" >&2
    echo "  --- stdout ---" >&2
    cat "$WORK_DIR/generate-audio.stdout" >&2
    exit 2
fi

# task_id == artifact_id（NotebookLM CLI 设计如此）
ARTIFACT_ID="$TASK_ID"
echo "  ✅ task_id (= artifact_id): $ARTIFACT_ID" >&2

# Step 4c: 阻塞等 artifact completed（最多 35 min）
echo "  ⏳ 等 artifact 生成完成（最多 35 min）..." >&2
set +e
$NOTEBOOKLM artifact wait "$ARTIFACT_ID" -n "$NOTEBOOK_ID" --timeout 2100 --interval 15 \
    > "$WORK_DIR/artifact-wait.stdout" 2>"$WORK_DIR/artifact-wait.stderr"
WAIT_RC=$?
set -e

if [[ $WAIT_RC -ne 0 ]]; then
    echo "  ❌ artifact wait 失败 rc=$WAIT_RC" >&2
    echo "  --- wait stderr ---" >&2
    cat "$WORK_DIR/artifact-wait.stderr" >&2 || true
    echo "  --- wait stdout ---" >&2
    cat "$WORK_DIR/artifact-wait.stdout" >&2 || true
    exit 2
fi

echo "  ✅ artifact completed: $ARTIFACT_ID" >&2


# ===== Step 5: 下载 m4a =====
# ⚠️ CLI 语义：`download audio -a <artifact-id> [OUTPUT_PATH]`。不是 -o。
echo "" >&2
echo "[5/6] 下载 m4a..." >&2
$NOTEBOOKLM download audio -a "$ARTIFACT_ID" "$AUDIO_FILE" 2>"$WORK_DIR/download.stderr" | tail -3 >&2 || {
    echo "  ❌ 下载失败，stderr:" >&2
    cat "$WORK_DIR/download.stderr" >&2
    exit 2
}

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
