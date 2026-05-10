#!/usr/bin/env bash
# Run all signal collectors. Each is failure-tolerant; missing data → empty file.
# Total budget ~ 90 seconds.

set -u
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
mkdir -p /tmp/ai-signals

echo "===== Signal collection started: $(date '+%F %T %Z') ====="

# 并行跑，每个 60 秒 timeout
timeout 60 python3 "$SCRIPT_DIR/fetch-hn-ai.py"        > /tmp/ai-signals/hn-ai.log 2>&1 &
timeout 60 python3 "$SCRIPT_DIR/fetch-smol-ai.py"      > /tmp/ai-signals/smol-ai.log 2>&1 &
timeout 60 python3 "$SCRIPT_DIR/fetch-editorial-en.py" > /tmp/ai-signals/editorial-en.log 2>&1 &
timeout 60 python3 "$SCRIPT_DIR/fetch-editorial-cn.py" > /tmp/ai-signals/editorial-cn.log 2>&1 &

wait

# 串行跑：基于已收集的信号构建「过去 7 天已发布黑名单」
# 失败不阻塞（输出空文件占位）
set +e
timeout 30 python3 "$SCRIPT_DIR/build-recent-published.py" > /tmp/ai-signals/recent-published.log 2>&1
set -e

echo ""
echo "===== Output files ====="
ls -la /tmp/ai-signals/ 2>/dev/null

echo ""
echo "===== Logs (last 3 lines each) ====="
for log in /tmp/ai-signals/*.log; do
    echo "--- $log ---"
    tail -3 "$log"
done

echo ""
echo "===== Done: $(date '+%F %T %Z') ====="
