# Arena 月更：抓取候选 → 独立 QC → 发布

更新：2026-10-11。实现以 `scripts/fetch-lmarena.sh` / `scripts/parse-lmarena.py` 为准。

## 根因与永久约束

- 系统 crontab 实际是 **每月 1 日 10:30（Asia/Shanghai）**，不是旧脚本注释中的 OpenClaw cron / 09:00。此次没有改调度。
- 10/1 的保留日志证明：HTTP 200、783,961 bytes，命中 `<1MB` 门槛，exit 5，尚未进入解析；旧 EXIT trap 又删除了原文。因此不能声称已经复原 10/1 原文。
- 10/11 取证：官方 `/leaderboard` 已是多赛道概览（820,685 bytes），不再含旧版扁平 `name/organization/overall` 矩阵。官方概览明确链接 `/leaderboard/chat/text`。新页 RSC 中为 `leaderboard.entries`，而非旧 regex 对象。
- **永久约束**：HTTP 200/字节数不是榜单完整性证据。必须解码结构、验证榜单口径、唯一模型数与源声明一致、必需字段、rank/rating/CI/votes 合法性；失败保留原文，不能写成功快照。
- **代理是共享依赖**，脚本只能使用已存在的 `127.0.0.1:7890`，缺失明确失败。不得启动、停止、pkill、改配置。此次没有动代理服务。
- 发布不得自动 pull/rebase/autostash；3 次 push 全失败必须非零，保留已提交数据以便人工重试。

## 新口径与日期

唯一接受来源：`https://arena.ai/leaderboard/chat/text`；HTTPS、默认 TLS 证书校验，非预期有效 URL 拒绝。

- `arenaSlug=text`、`leaderboardSlug=overall`、`params={category:overall,styleControl:true}`；精确 leaderboard ID 校验。
- 展示 **文本总榜（风格控制）Top 50**。`scores.overall` 仍表示名次；`rating` 是独立源字段，不再把两者混为一谈。
- 不捏造新页面没有的旧版 27 维分项/优势赛道；`highlight=[]`。
- `rankingBasis=arena-text-overall-style-control-v1`。无同口径前期快照时，页面显示基线、不算升降或退出 Top 50。旧快照没有明确口径，不强行拼接时间序列。
- `snapshotDate` 是 **抓取日期**，从带时区 `fetchedAt` 派生；不是用户随意传入的发布日期。
- `sourceUpdatedAt` 实际语义是官方 `voteCutoffISOString`（投票截止），不是页面渲染时刻。缺失时为 null、明确标注未知；已知源时间超过 45 天或晚于抓取时刻 5 分钟以上均拒绝。
- 唯一模型数须 100–5000 且等于 `totalModels`；排名必须完整 1..N，rating 与排名单调一致；精确重复去重，冲突 ID/显示名拒绝。若官方未来改为并列名次，须人工适配，不能默默补排。
- 源的 `modelOrganization` 字段缺失拒绝；源明确空字符串的旧模型标为“未披露”，不猜厂商。当前 414 个源模型有 50 个空厂商，Top 50 均非空。

## 安全模式

```bash
# 默认模式也是 fetch；不写 src/data，不 build，不 git commit，不 push
scripts/fetch-lmarena.sh fetch

# 离线重解析保留样本；日期仍取原始 fetch.json，不改日期
scripts/fetch-lmarena.sh parse .cron-logs/lmarena/<run>
```

每次抓取目录 `.cron-logs/lmarena/<真实时间>-<随机串>/` 保留：

- `source.html`：原始响应正文（解析失败也保留）
- `response.headers`、`transport.txt`：原始传输证据（仅本地，不发布可能的 cookie）
- `fetch.json`：UTC+8 抓取时间、原始/有效 URL、HTTP/传输退出码、字节数、SHA-256
- `candidate.json`：仅通过语义验证才原子落盘；失败不会覆盖已有候选
- `status.json`；同时更新 `.cron-logs/lmarena/latest-status.json`

`parse` 是无网络的回放验证，不意味着今天重新抓取。SHA-256/bytes/HTTP/curl 返回码均须与样本对应。

## QC 与发布（需主会话人工收口）

1. MK46 独立核对原文、模型数据、日期和口径、测试与页面证据。
2. QC **APPROVE** 后，由主会话取得**被批准候选文件**的 SHA-256。hash 参数是明确批准动作的绑定，不代表密码学签名，也不会自动产生批准。
3. 项目必须处于 `main`、干净工作树（含未跟踪文件），再执行：

```bash
scripts/fetch-lmarena.sh publish .cron-logs/lmarena/<run> \
  --approved-sha256 <QC批准候选的SHA256>
```

发布模式会重新验证原文并逐字比对候选 → 取得既有 `ai-daily-publish.lock` → 新增真实日期快照 → `pnpm exec astro build` → 只提交该快照 → push（最多 3 次、不 rebase）。`pnpm exec` 刻意绕过与 Arena 无关、会改 agent-chains 的 package prebuild。build 失败撤掉本次新建快照；不同内容同日快照拒绝覆盖；已成功提交但 push 失败保留本地 commit，重试不重复提交。

**当前主工作树含他人修改和未跟踪文件，不满足自动发布前置条件。** 不得为了过 gate 擅自 stash/clean/提交它们。主会话可在梳理自己的变更后正常发布，或用干净独立 checkout 集成审核后的代码和候选。此次工程交付只把候选放进 `state/lmarena-candidates/2026-10-11.json`，没有写生产 `src/data/lmarena/snapshots/`，也没有 push。

`published` 仅指 git push 成功，不表示 GH Pages 已上线；主会话仍须检查 CI 和线上 `/lmarena/` 实际日期。

## 告警接入状态：尚未接通通知

旧脚本“非零会由 cron 捕获给 heartbeat”的注释不成立：系统 crontab 只是将 stdout/stderr 重定向 `/tmp/lmarena-cron.log`。没有证据表明此日志被送进飞书。

源码核验的既有 `scripts/daily-watchdog.sh` 只检查 Daily JSON/首页日期，会补 push/触发日报重跑，**不是 Arena 看门狗**。现有启用的 OpenClaw `ai-daily-watchdog`（`4450901e-d8fb-4feb-b75f-0bcb1ad548b0`）有 announce 渠道，但其 payload 尚未引用 Arena。

当前仅提供本地机器可读状态，`notificationDelivered=false`：

- `candidate_ready`：抓取/解析成功，等待 QC，**不是已发布**。
- `failed`：含 phase、exitCode、runDir，原文可追溯。
- `published`：push 成功，线上部署另验。

**建议的最小后续方案（未实施）**：由主会话审批后，在既有 watchdog 的 prompt/检查步骤追加只读检查 `latest-status.json`（不复用其自动补 push 分支），用现成 announce 报“抓取失败 / 本月无候选 / 候选等待 QC / 已 push 但站点仍旧”。将告警去重键设为 `runDir + status`；7:10 看门狗对 10:30 月更的检查最多滞后一日，需明确接受这个延迟或另行审批更合适的既有时段。此任务不新增 cron、不改任何通知权限、不外发消息。

## 可复现验证

```bash
python3 -m unittest discover -s tests -p 'test_lmarena.py' -v
bash -n scripts/fetch-lmarena.sh
```

测试用固定真实原文 gzip fixture，同时使用合成边界数据。shell 测试在临时 git 仓库中 mock 网络、代理检查、build 与 push，既不动共享代理，也不发网络请求。fixture SHA 在 `tests/fixtures/lmarena/text-2026-10-11.fetch.json`，不把页面响应头/cookie 入库。

页面验证：在**独立构建副本**安装候选到 `src/data/lmarena/snapshots/2026-10-11.json`，跑 `pnpm build`，再执行：

```bash
# 可用 PLAYWRIGHT_CHROMIUM_EXECUTABLE 指定已安装 Chromium，测试不会下载浏览器
node tests/check-lmarena-page.mjs <独立副本>/dist \
  state/lmarena-candidates/2026-10-11.json <证据目录>
```

脚本只访问本地临时 HTTP server，阻止外部请求；检查桌面/移动端 50 行、模型名完整相符、时间/口径、无虚假升降、无 JS 错误/横向溢出，并保存截图。它不会修改真实快照目录。

## 2026-10-11 候选证据

- 抓取：`2026-10-11T23:41:46+08:00`；官方投票截止：`2026-10-08T14:00:00.000Z`（北京时间 10/8 22:00）。不是 10/1 补日期，也未复用 9 月数据。
- 原文：2,741,589 bytes；SHA-256 `42362a73ed654c18204719d256319d624c0ec41bc1053e79f19a24157d8ed5b4`。
- 源声明/解析均为 **414** 个模型，Top **50**；第一名 `gemini-4-argon-high`，rating `1525.3956435571818`。
- 候选 SHA-256：`9e45d98e55b7ad093103df29e0f64273a1f871edf0a4a5efb67e8fe0bb8e4dca`。
- 本机抓取目录：`.cron-logs/lmarena/2026-10-11T234146-TI0nFv/`。
- 本机补充证据：`/root/.openclaw/workspace-mk2/arena-repair-evidence/`（overview/text 原文及解码摘录、测试/build/page 日志、1440/390px 截图）。
- 完整 `pnpm build` 在独立副本通过：272 pages；真实项目中的他人脏文件没有被构建 prehook 修改。

## 回滚

尚未 push/安装候选时：无需回滚生产数据。若需要撤回本次代码，用本次专属 commit 的 `git revert <commit>`（先处理自己的工作树，勿触碰他人文件）。若新快照已发布，另作经审核的 revert 删除该新增日期快照，重新 build/push 恢复前期展示。**不要直接恢复旧的危险 fetch 脚本到计划任务入口**；撤回代码前应由主会话另行决定暂停抓取或保留安全版入口，避免重新引入 pkill 共享代理。没有任何代理/全局配置需要恢复。
