#!/bin/bash
# publish-audio.sh — 上传音频到 COS + 写回对应 JSON（日报或精读）
#
# 用法：
#   # 精读模式（推荐主路径）
#   ./publish-audio.sh reads <音频路径> <slug>
#   ./publish-audio.sh reads /tmp/karpathy.m4a karpathy-agi-decade-away
#
#   # 日报模式（向后兼容，备用）
#   ./publish-audio.sh daily <音频路径> [日期 YYYY-MM-DD]
#   ./publish-audio.sh daily /tmp/daily.mp3 2026-05-06
#
# 流程：
#   1. 加载 COS 凭据
#   2. upload-audio.py 上传 → 拿元数据 JSON
#   3. write-audio-meta.py 写回对应 JSON
#
# 返回码：0 成功 / 1 失败

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CREDS_FILE="/root/.config/cos/credentials.env"

# ===== 参数检查 =====
if [[ $# -lt 2 ]]; then
    cat >&2 <<EOF
用法：
  $0 reads <音频路径> <slug>            # 精读模式
  $0 daily <音频路径> [日期 YYYY-MM-DD]  # 日报模式

例子：
  $0 reads /tmp/karpathy.m4a karpathy-agi-decade-away
  $0 daily /tmp/daily.mp3
  $0 daily /tmp/daily.mp3 2026-05-06
EOF
    exit 1
fi

MODE="$1"
AUDIO_PATH="$2"

if [[ "$MODE" != "reads" && "$MODE" != "daily" ]]; then
    echo "ERROR: mode 必须是 reads 或 daily（收到：$MODE）" >&2
    exit 1
fi

if [[ ! -f "$AUDIO_PATH" ]]; then
    echo "ERROR: 音频文件不存在：$AUDIO_PATH" >&2
    exit 1
fi

# 模式相关参数
UPLOAD_ARGS=("--mode" "$MODE")
WRITE_ARGS=("--mode" "$MODE")

if [[ "$MODE" == "reads" ]]; then
    SLUG="${3:-}"
    if [[ -z "$SLUG" ]]; then
        echo "ERROR: reads 模式需要 slug 作为第三个参数" >&2
        exit 1
    fi
    UPLOAD_ARGS+=("--slug" "$SLUG")
    WRITE_ARGS+=("--slug" "$SLUG")
    LABEL="精读 [$SLUG]"
else
    DATE="${3:-$(TZ=Asia/Shanghai date +%Y-%m-%d)}"
    if ! [[ "$DATE" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
        echo "ERROR: 日期格式不对（要 YYYY-MM-DD）：$DATE" >&2
        exit 1
    fi
    UPLOAD_ARGS+=("--date" "$DATE")
    WRITE_ARGS+=("--date" "$DATE")
    LABEL="日报 [$DATE]"
fi

# ===== 加载凭据 =====
if [[ ! -f "$CREDS_FILE" ]]; then
    echo "ERROR: COS 凭据文件不存在：$CREDS_FILE" >&2
    exit 1
fi

set -a
# shellcheck disable=SC1090
. "$CREDS_FILE"
set +a

if [[ -z "${SECRET_ID:-}" || -z "${SECRET_KEY:-}" ]]; then
    echo "ERROR: SECRET_ID / SECRET_KEY 加载失败" >&2
    exit 1
fi

# ===== Step 1: 上传 =====
echo "[1/2] 上传音频到 COS（$LABEL）..." >&2
META_JSON=$(python3 "$SCRIPT_DIR/upload-audio.py" "$AUDIO_PATH" "${UPLOAD_ARGS[@]}" --quiet)

if [[ -z "$META_JSON" ]]; then
    echo "ERROR: upload-audio.py 没有输出" >&2
    exit 1
fi

# ===== Step 2: 写回 JSON =====
echo "[2/2] 写回 JSON ..." >&2
echo "$META_JSON" | python3 "$SCRIPT_DIR/write-audio-meta.py" "${WRITE_ARGS[@]}"

echo "" >&2
echo "🎉 完成！$LABEL 的音频已发布。" >&2
