#!/usr/bin/env bash
# S.H.R.I.M.P. OS Dashboard — 每小时数据刷新 + 部署
# 由 cron 调用：聚合最新 token 数据 → 提交到 ai-daily 仓库 → 触发 GitHub Pages 重建
# GitHub push 走 mihomo 代理（~/.gitconfig 已全局配 GitHub-only proxy）
set -euo pipefail

REPO=/root/.openclaw/workspace/projects/ai-daily
cd "$REPO"

echo "[$(date '+%F %T')] S.H.R.I.M.P. dashboard refresh start"

# 1. 聚合最新 token / 成本数据
python3 scripts/agents-dashboard-aggregate.py

# 2. 仅当数据有变化才提交（避免空 commit）
if git diff --quiet public/agents/data/dashboard-data.json 2>/dev/null; then
  echo "[$(date '+%F %T')] no data change, skip commit"
  exit 0
fi

git add public/agents/data/dashboard-data.json
git commit -m "chore(agents): refresh dashboard telemetry $(date '+%F %H:%M')" >/dev/null
git push origin main >/dev/null 2>&1
echo "[$(date '+%F %T')] pushed — Pages will rebuild in ~1-2min"
