#!/bin/bash
# batch-podcast.sh — 并行 2 路批量生成精读播客
#
# 用法：
#   bash batch-podcast.sh slug1 slug2 slug3 slug4 ...
#
# 输出：
#   - 主日志：$BATCH_LOG_DIR/batch.log
#   - 每篇日志：$BATCH_LOG_DIR/<slug>.log
#   - 完成清单：$BATCH_LOG_DIR/done.txt（成功列表）
#   - 失败清单：$BATCH_LOG_DIR/failed.txt

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GEN_SCRIPT="$SCRIPT_DIR/generate-podcast.sh"
PARALLEL=2

if [[ $# -eq 0 ]]; then
    echo "用法：$0 slug1 slug2 ..." >&2
    exit 1
fi

SLUGS=("$@")
TOTAL=${#SLUGS[@]}

BATCH_LOG_DIR="/tmp/podcast-batch-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BATCH_LOG_DIR"
BATCH_LOG="$BATCH_LOG_DIR/batch.log"
DONE_FILE="$BATCH_LOG_DIR/done.txt"
FAILED_FILE="$BATCH_LOG_DIR/failed.txt"
GIT_LOCK="$BATCH_LOG_DIR/.git.lock"  # 串行化 git commit/push
touch "$DONE_FILE" "$FAILED_FILE"

# 为避免并行同一秒启动被 NotebookLM 后端合并请求，后启动的进程会错开 N 秒。
STAGGER_DELAY=10  # 鬟错启动间隔秒数

log() {
    echo "$@" | tee -a "$BATCH_LOG"
}

log ""
log "==================================================================="
log "📦 批量任务：$TOTAL 篇 / 并行 $PARALLEL 路"
log "📁 日志目录：$BATCH_LOG_DIR"
log "🕐 启动时间：$(date '+%F %T %Z')"
log "==================================================================="
log ""

# 单篇任务：生成 + 上传 + 写回 + commit/push
run_one() {
    local slug="$1"
    local idx="$2"
    local log_file="$BATCH_LOG_DIR/$slug.log"
    local start_ts=$(date '+%F %T')
    local start_epoch=$(date +%s)

    echo "[$start_ts] ▶️  [$idx/$TOTAL] START $slug" >> "$BATCH_LOG"

    # 馔等鬟错启动（除了第 1 口）避免后端可能合并请求
    if [[ $idx -gt 1 && $idx -le $PARALLEL ]]; then
        local stagger=$(( (idx - 1) * STAGGER_DELAY ))
        echo "  [stagger] 鬟错启动 ${stagger}s" >> "$log_file"
        sleep $stagger
    fi

    bash "$GEN_SCRIPT" "$slug" > "$log_file" 2>&1
    local rc=$?

    local end_ts=$(date '+%F %T')
    local elapsed=$(( $(date +%s) - start_epoch ))
    local mm=$((elapsed / 60))
    local ss=$((elapsed % 60))

    if [[ $rc -eq 0 ]]; then
        # commit + push（用 flock 串行化，避免并行 git 冲突）
        (
            flock -x 200
            cd /root/.openclaw/workspace/projects/ai-daily
            local json_file=$(ls src/data/reads/ | grep -E -- "-${slug}\.json$" | head -1)
            if [[ -n "$json_file" ]]; then
                git add "src/data/reads/$json_file" >> "$log_file" 2>&1
                git commit -m "feat(reads): 加 $slug 精读播客" >> "$log_file" 2>&1 || true
                # push 重试 5 次，隔 10s 递增
                local pushed=0
                for try in 1 2 3 4 5; do
                    if git pull --rebase >> "$log_file" 2>&1 && git push >> "$log_file" 2>&1; then
                        pushed=1
                        break
                    fi
                    echo "[try=$try] push 失败，等 $((try*10))s 重试" >> "$log_file"
                    sleep $((try*10))
                done
                if [[ $pushed -eq 1 ]]; then
                    echo "[$end_ts] ✅ [$idx/$TOTAL] DONE $slug (${mm}m${ss}s, pushed)" >> "$BATCH_LOG"
                else
                    echo "[$end_ts] ⚠️  [$idx/$TOTAL] DONE $slug (${mm}m${ss}s, push 失败 5次，已 commit)" >> "$BATCH_LOG"
                fi
                echo "$slug" >> "$DONE_FILE"
            else
                echo "[$end_ts] ⚠️  [$idx/$TOTAL] DONE $slug (${mm}m${ss}s, 但找不到 reads JSON)" >> "$BATCH_LOG"
                echo "$slug" >> "$DONE_FILE"
            fi
        ) 200>"$GIT_LOCK"
    else
        echo "[$end_ts] ❌ [$idx/$TOTAL] FAIL $slug rc=$rc (${mm}m${ss}s)" >> "$BATCH_LOG"
        echo "$slug" >> "$FAILED_FILE"
    fi

    return $rc
}

# 并行调度：用 wait -n 等任意子进程完成
slug_idx=0
running=0

while [[ $slug_idx -lt $TOTAL || $running -gt 0 ]]; do
    # 启动新进程，直到达到并行数
    while [[ $running -lt $PARALLEL && $slug_idx -lt $TOTAL ]]; do
        local_idx=$((slug_idx + 1))
        local_slug="${SLUGS[$slug_idx]}"
        echo "  → [$local_idx/$TOTAL] launching $local_slug" >> "$BATCH_LOG"
        run_one "$local_slug" "$local_idx" &
        slug_idx=$((slug_idx + 1))
        running=$((running + 1))
    done

    # 等任意一个完成
    if [[ $running -gt 0 ]]; then
        wait -n 2>/dev/null
        running=$((running - 1))
    fi
done

# 全部跑完
log ""
log "==================================================================="
log "🎉 批量任务全部完成"
log "  - 成功：$(wc -l < $DONE_FILE) 篇"
log "  - 失败：$(wc -l < $FAILED_FILE) 篇"
log "🕐 结束时间：$(date '+%F %T %Z')"
log "==================================================================="
