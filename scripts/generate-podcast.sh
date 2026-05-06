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

# ===== Step 4: 幂等检测 + 生成 audio（关键：-s <source-id> 锁定单篇）=====
# 注：artifact 没有 source 关联字段。幂等检测用「同一 notebook + title 包含本篇关键词 + 最近1小时」。
echo "" >&2
echo "[4/6] 检查是否已有 completed artifact（幂等）..." >&2

# 取 source title 前4个字作为模糊匹配锯（避先误匹配同 notebook 其他篇）
TITLE_PREFIX=$(echo "$SOURCE_TITLE" | head -c 12)

EXISTING_ARTIFACT_ID=$($NOTEBOOKLM artifact list -n "$NOTEBOOK_ID" --type audio --json 2>"$WORK_DIR/artifact-list.stderr" | python3 -c "
import sys, json, time
from datetime import datetime, timedelta
try:
    data = json.load(sys.stdin)
    items = data.get('artifacts', []) if isinstance(data, dict) else data
    title_kw = '${TITLE_PREFIX}'.strip()
    cutoff = datetime.now() - timedelta(hours=24)
    for a in items:
        if a.get('status') != 'completed': continue
        title = a.get('title', '')
        # title 包含本篇关键词（模糊匹配，容忍 NotebookLM 自动变名）
        if not title or not any(w in title for w in title_kw.replace('《','').replace('》','').replace('：','').split()[:1]):
            continue
        # 仅看最近 24h 创建的
        try:
            ct = datetime.fromisoformat(a.get('created_at', '').split('+')[0])
            if ct > cutoff:
                print(a['id']); break
        except Exception:
            continue
except Exception:
    pass
" 2>/dev/null || echo "")

if [[ -n "$EXISTING_ARTIFACT_ID" ]]; then
    ARTIFACT_ID="$EXISTING_ARTIFACT_ID"
    echo "  ♻️  发现近期 completed artifact，复用：$ARTIFACT_ID" >&2
else
    echo "  → 无现成 artifact，开始生成（deep-dive long zh，-s 锁定本篇 source）" >&2

    # 记录生成启动时间，后面轮询只看这之后创建的 artifact
    GEN_START_EPOCH=$(date +%s)
    GEN_START_ISO=$(TZ=UTC date -u -d "@$GEN_START_EPOCH" '+%Y-%m-%dT%H:%M:%S')
    echo "  ⏰ 启动时间（UTC）：$GEN_START_ISO" >&2

    # ⚠️ 铁律：不依赖 --wait（1 个脚本设计必须是幂等、可重试、可诊断的）
    # generate audio --wait 会提前退出（5-6 分钟而不是 15-25）。改用我们自己的轮询。
    #
    # PROMPT 铁律（Jason 2026-05-06 拍板）：
    # 1. 沿用原标题，不要重写
    # 2. 严格仅限原文内容，不准编原文未讲过的东西
    PROMPT="这期播客介绍《${SOURCE_TITLE}》。中文双主持人对谈，深度阐释原文。

严格要求：
1. 本期节目标题必须是《${SOURCE_TITLE}》。不要重写、不要改名、不要起别的名字。
2. 所有论点、数据、例子、引言、背景信息都必须严格出自原文。不准编原文未讲过的内容。
3. 可以重述、阐释、讨论原文观点，但不准联想、不准类比到原文未提的例子、不准「补充背景」。
4. 如果原文某个点介绍不够详细，说「作者未详述」即可，不准填补。
风格：严谨专业、信息密集、面向专业人士，不要闲聊化。"

    # 启动生成（不 --wait）——发起请求后就退出
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
    echo "  → 生成请求已发起（rc=$GEN_RC）" >&2

    # 轮询 artifact list，取本次启动后创建的 audio artifact
    # 轮询策略：最多等 35 分钟（避免 long deep-dive 超期），每 30s 查一次
    echo "  ⏳ 轮询生成状态（最多等 35 分钟）..." >&2
    ARTIFACT_ID=""
    POLL_INTERVAL=30
    POLL_MAX_TRIES=70  # 70 * 30s = 35 分钟

    for i in $(seq 1 $POLL_MAX_TRIES); do
        sleep $POLL_INTERVAL
        ELAPSED=$(( $(date +%s) - GEN_START_EPOCH ))

        # 查 artifact list，取「启动之后创建的 + completed + audio」
        FOUND_ID=$($NOTEBOOKLM artifact list -n "$NOTEBOOK_ID" --type audio --json 2>"$WORK_DIR/poll-${i}.stderr" | python3 -c "
import sys, json
from datetime import datetime
try:
    data = json.load(sys.stdin)
    items = data.get('artifacts', []) if isinstance(data, dict) else data
    cutoff = datetime.fromisoformat('${GEN_START_ISO}')
    for a in items:
        if a.get('status') != 'completed': continue
        try:
            ct = datetime.fromisoformat(a.get('created_at', '').split('+')[0])
            if ct >= cutoff:
                print(a['id']); break
        except Exception:
            continue
except Exception as e:
    pass
" 2>/dev/null || echo "")

        if [[ -n "$FOUND_ID" ]]; then
            ARTIFACT_ID="$FOUND_ID"
            echo "  ✅ 生成完成（耗时 ${ELAPSED}s，轮询 #${i}）：$ARTIFACT_ID" >&2
            break
        fi

        if (( i % 4 == 0 )); then
            echo "  …还在生成中（已等 ${ELAPSED}s / 轮询 #${i}）..." >&2
        fi
    done

    if [[ -z "$ARTIFACT_ID" ]]; then
        echo "  ❌ 轮询 35 分钟后仍未看到 completed artifact" >&2
        echo "  generate-audio.stdout:" >&2
        cat "$WORK_DIR/generate-audio.stdout" >&2
        echo "  generate-audio.stderr:" >&2
        cat "$WORK_DIR/generate-audio.stderr" >&2
        exit 2
    fi
fi
echo "  ✅ artifact-id: $ARTIFACT_ID" >&2

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
