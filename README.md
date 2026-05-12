# AI Daily Digest

AI 行业信息聚合站——自动 + 人工混合更新，覆盖每日新闻、深度精读、GitHub 热门、大模型榜单、Demo 项目和学习资源。

🌐 网站：https://aidigest.club

---

## 📚 站点结构

由 **6 个独立栏目** + **每日新闻 4 板块** 组成，不同栏目有不同的更新节奏。

### 🗞️ 每日新闻（首页 + 归档）

每日清晨自动同步过去 24 小时全球 AI 行业重要动态，按 4 个板块组织：

- 🔥 **AI 热点新闻** — 重大融资、产品发布、监管动态、突发事件
- 🏢 **企业级 AI 实践** — 落地案例、Agent 编排、企业架构演进
- 💻 **AI Coding 动态** — 编码模型、IDE 集成、开发者工具
- 📊 **深度报告与论文** — 行业研究、学术论文、白皮书

### 🐙 GitHub 热门

每月/每周自动同步 GitHub Trending 上 AI 相关仓库的热度变化、Star 增长、新晋黑马项目。聚焦开源生态。

### 🏆 LMArena

基于 [lmarena.ai](https://lmarena.ai/leaderboard) 真实人类盲测对战数据的全球大模型 Top 50 排行榜。每月 1 日 10:30 自动抓取、解析、生成优势赛道标签，与上月快照对比生成排名变化（↑/↓/🆕/⛔）。

### 📖 精读

精挑细选的 AI 时代深度长文，配中文解读、核心观点、金句精选，部分配有中文双主持人播客版本。每周一 09:00 自动生成候选清单（3-5 篇），人工拍板后写正式精读卡片。**宁缺勿滥**——某周无合适候选则跳过，不为凑数硬塞。

### 🎬 Demo

手工挑选的「值得亲手玩一下」的项目——AI 应用、行业 Dashboard、Agent 工具、可视化作品。每张卡片附 Live Demo 直达链接 + GitHub 源码，从 README 提炼简介、Purpose、Key Features。

### 🎓 学习

AI 相关的学习计划、课程笔记、技术资料汇总。独立于每日资讯主题，更聚焦于深度学习和长期价值。手工维护，按需更新。

### 📋 关于

站点说明、内容范围、信息源清单、更新机制、免责声明。

---

## 🌐 信息源

### 🌍 国际媒体
Reuters · Bloomberg · FT · WSJ · NYT · The Guardian · The Information · Wired · TechCrunch · The Verge · VentureBeat · Ars Technica

### 🏢 厂商一手源
OpenAI · Anthropic · Google DeepMind · Microsoft · Meta · NVIDIA · arXiv · GitHub Trending

### 🇨🇳 中文科技媒体
36氪 · 机器之心 · 量子位 · 虎嗅 · 晚点 LatePost · 极客公园 · InfoQ 中国 · 雷峰网 · PingWest 品玩 · 钛媒体 · IT 之家 · 智东西 · 36氪出海 · 华尔街见闻

### 📊 咨询与研究机构
Accenture · McKinsey · BCG · Gartner · IDC · Deloitte · PwC · Stanford HAI · MIT Technology Review · OECD.AI · Brookings AIET · 中国信通院 CAICT

### 💰 投融资专源
Crunchbase News · Sifted（欧洲） · 投中网（国内）

---

## 🛠 技术栈

- **Astro** — 静态站点生成器
- **Tailwind CSS** — 样式
- **TypeScript** — 类型安全
- **GitHub Actions** — 自动构建与部署到 GitHub Pages
- **Cloudflare** — CDN 与自定义域名（aidigest.club）

## 本地开发

```bash
pnpm install
pnpm dev          # 启动开发服务器
pnpm build        # 构建静态站点
pnpm sync         # 从飞书同步最新内容（需配 .env）
```

---

## 📋 免责声明

Personal project. Not affiliated with Accenture or any other organization mentioned.

内容由 AI 辅助整理，仅供参考，不构成投资或决策建议。所有引用来源均保留原始链接，版权归原作者所有。

## License

MIT
