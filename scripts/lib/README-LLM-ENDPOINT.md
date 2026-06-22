# LLM Endpoint 单一可信源（B 方案）

## 设计

ai-daily 所有需要 LLM 的脚本（github-trending 翻译、sync 翻译），其 endpoint
配置**统一来自 `openclaw.json` 的 provider**，不再散落在各处 `.env`。

- **可信源**：`/root/.openclaw/openclaw.json` → `models.providers.aigw-claude-48-main`
- **解析器**：`scripts/lib/llm-endpoint.sh`（从 openclaw.json 读 base/key/model/protocol，export LLM_*）
- **消费方**：cron-github.sh / cron-sync.sh / cron-sync-event.sh 启动时 `source` 该 helper

## 🔧 以后换 endpoint 怎么做（只改一处！）

编辑 `/root/.openclaw/openclaw.json`，改 `aigw-claude-48-main` provider 的：
- `baseUrl` —— 新 endpoint 地址
- `apiKey` —— 新 key
- `models[0].id` —— 新模型名（helper 默认取第一个 model）

改完**无需重启任何东西**，下次 cron 跑时自动生效（ai-daily 脚本 + 各 OpenClaw agent 同时切换）。

### 想让 ai-daily 用不同于 agent 的 provider/model？

设环境变量覆盖（一般不需要）：
- `AI_DAILY_LLM_PROVIDER=其它provider名`
- `AI_DAILY_LLM_MODEL=其它model名`

## 🩺 健康检查

- 手动：`bash scripts/check-endpoints.sh`
- 自动：每天 06:05 cron（`check-endpoints-cron.sh`）探活，挂了发飞书告警给 Jason
- 这是为了避免「endpoint 静默关停 → 数据停更数周才发现」（2026-06-22 GitHub 榜单事故）

## ⚠️ 改动注意

`cron-github.sh` 含 `git reset --hard origin/main`，会冲掉未提交的本地源码改动。
**改这些脚本必须先 commit+push 到 origin** 才能生效，否则一跑 cron 就被还原。
