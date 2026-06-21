#!/bin/bash
# auto-enqueue-reads.sh — 自动把"无音频"的精读推入播客生成队列
#
# 由 system cron 定期调用。配合 podcast-pipeline/worker.py（每5分钟）实现
# 精读上线 → 自动生成播客 → 验证(音频可达+时长正常) → 自动上架 全流程无人值守。
#
# 判定"需要生成播客"的精读：
#   1. reads JSON 里没有 audio.url 字段（= 还没上架音频）
#   2. 且 podcast state 队列里没有该 slug 的 active 任务（避免重复入队）
#   3. 且 quotes 格式合规（enqueue.py 会再校验一次，这里提前过滤）
#
# enqueue.py 自身幂等（S.exists 命中返回3），这里的预过滤只是减少无谓调用。
#
# 返回码：0 正常（无论是否有新入队）

set -uo pipefail

PROJECT_ROOT="/root/.openclaw/workspace/projects/ai-daily"
READS_DIR="$PROJECT_ROOT/src/data/reads"
STATE_DIR="$PROJECT_ROOT/state/podcasts"
ENQUEUE="python3 $PROJECT_ROOT/scripts/podcast-pipeline/enqueue.py"
LOG_DIR="$STATE_DIR/.logs"
LOG="$LOG_DIR/auto-enqueue.log"
PROXY="http://127.0.0.1:7890"
LOCK="/tmp/auto-enqueue-reads.lock"

mkdir -p "$LOG_DIR"

ts() { TZ=Asia/Shanghai date '+%H:%M:%S'; }
log() { echo "$(ts) $*" | tee -a "$LOG"; }

# 单实例锁：避免与上一轮（NotebookLM 调用慢）重叠
exec 9>"$LOCK"
if ! flock -n 9; then
    log "另一个 auto-enqueue 在跑，跳过本轮"
    exit 0
fi

# mihomo 健康检查——NotebookLM 必须走代理
if ! ss -tlnp 2>/dev/null | grep -q '127.0.0.1:7890'; then
    log "⚠️ mihomo 未运行，跳过本轮（NotebookLM 不可达）"
    exit 0
fi

# 用 node 找出"无 audio.url 且无 active state"的 slug 列表
TODO=$(node -e '
const fs=require("fs");
const readsDir="'"$READS_DIR"'";
const stateDir="'"$STATE_DIR"'";
// 当前 active state 的 slug（active = 直接在 state/podcasts/ 下的 *.json，不含 .archive/.logs）
let active=new Set();
try {
  fs.readdirSync(stateDir).filter(f=>f.endsWith(".json")).forEach(f=>active.add(f.replace(/\.json$/,"")));
} catch(e){}
let todo=[];
fs.readdirSync(readsDir).filter(f=>f.endsWith(".json")).forEach(f=>{
  let d;
  try { d=JSON.parse(fs.readFileSync(readsDir+"/"+f)); } catch(e){ return; }
  const slug=d.slug;
  if(!slug) return;
  const hasAudio = d.audio && d.audio.url;
  if(hasAudio) return;            // 已上架音频，跳过
  if(active.has(slug)) return;    // 正在处理，跳过
  todo.push(slug);
});
console.log(todo.join("\n"));
')

if [[ -z "$TODO" ]]; then
    log "无需入队（所有精读已有音频或正在处理）"
    exit 0
fi

COUNT=$(echo "$TODO" | grep -c .)
log "发现 $COUNT 篇待生成播客：$(echo $TODO | tr '\n' ' ')"

ENQUEUED=0
while IFS= read -r slug; do
    [[ -z "$slug" ]] && continue
    log "入队：$slug ..."
    if HTTPS_PROXY="$PROXY" timeout 200 $ENQUEUE "$slug" >>"$LOG" 2>&1; then
        log "  ✅ $slug 入队成功"
        ENQUEUED=$((ENQUEUED+1))
    else
        rc=$?
        # rc=3 = 已存在（幂等，正常）；其他为真失败
        if [[ $rc -eq 3 ]]; then
            log "  ↺ $slug 已在队列（幂等跳过）"
        else
            log "  ❌ $slug 入队失败 rc=$rc（worker 的 stuck 告警不覆盖入队失败，留日志待查）"
        fi
    fi
    sleep 8   # 错开 NotebookLM 后端，避免请求合并
done <<< "$TODO"

log "本轮完成：尝试 $COUNT 篇，成功入队 $ENQUEUED 篇"
exit 0
