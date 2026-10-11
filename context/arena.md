# Arena 数据管线（2026-10-11 修复候选，待独立 QC）

详见 [运行手册与证据](../docs/arena-pipeline.md)。该文件是本任务新建；未修改同日由主会话新建的其他 Context Pack 文件。

- 实际调度：系统 crontab 每月 1 日 **10:30 Asia/Shanghai**。任务入口仍是 `scripts/fetch-lmarena.sh`；未改 cron。
- 默认入口现在只抓取 **QC 候选**，不直接写入生产快照、不自动提交发布。`parse RUN_DIR` 离线回放；`publish RUN_DIR --approved-sha256 SHA` 必须在主会话取得 MK46 APPROVE 后使用。
- 官方来源已适配为 `https://arena.ai/leaderboard/chat/text`，Next.js Flight `leaderboard.entries`，文本总榜/风格控制。概览页不再提供旧 rank 矩阵，不能只降低 HTML 大小阈值。
- `fetchedAt/snapshotDate` 与官方 `voteCutoffISOString` 分离；分项缺失不得伪造，口径变化不得硬算月度升降。
- 现存代理只使用、不启停。失败留样本和非零状态；不自动 rebase/autostash；push 全失败不能宣称成功。
- 原文、元数据、候选及状态在 `.cron-logs/lmarena/<run>/`；候选首次交付在 `state/lmarena-candidates/2026-10-11.json`，**尚未安装进 `src/data/lmarena/snapshots/`**。
- 测试：`python3 -m unittest discover -s tests -p 'test_lmarena.py' -v`；真实 fixture 随库；页面测试在独立副本 build，不污染他人工作树。
- **告警未接通**：只有 `latest-status.json`/stderr；不能声称 cron stderr 自动到飞书。建议经主会话审批后接入既有 ai-daily-watchdog announce，只读检查、不调用其 Daily 自动代推分支。

主会话收口时请在 INDEX 的 Arena 触发索引链接本文件，并把此处永久约束合并进 conventions；本任务不擅自修改他人尚未提交的 Pack。
