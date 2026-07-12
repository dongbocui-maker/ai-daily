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

# 1b. 从 openclaw.json 重新生成 agent 模型链路（single source of truth）
# GitHub Actions build 环境读不到 openclaw.json，故必须在本机（VM）生成并提交，
# Actions 的 prebuild hook 会 fail-soft 保留这份已提交的 JSON。
python3 scripts/gen-agent-chains.py || echo "[$(date '+%F %T')] gen-agent-chains skipped (keeping existing)"

# 2. 仅当 fallback 快照 或 模型链路 有变化才提交（避免空 commit）
# 注：live 数据走 Cloudflare Tunnel 实时服务，git 只跟踪低频 fallback 快照（AUDIT-2026-06-11 M2）
if git diff --quiet public/agents/data/dashboard-fallback.json src/data/agent-chains.json 2>/dev/null; then
  echo "[$(date '+%F %T')] no fallback / chain change, skip commit"
  exit 0
fi

git add public/agents/data/dashboard-fallback.json src/data/agent-chains.json
git commit -m "chore(agents): refresh dashboard fallback + agent chains $(date '+%F %H:%M')" >/dev/null
git push origin main >/dev/null 2>&1
echo "[$(date '+%F %T')] pushed — Pages will rebuild in ~1-2min"
