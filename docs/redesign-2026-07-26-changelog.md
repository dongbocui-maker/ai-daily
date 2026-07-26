# aidigest.club 全站改版归档 · 2026-07-26

> 一天内完成的全站 UI 重设计（首页 + 5 栏目页 + 关于页 + 2 详情页 + 栏目重命名 + 字号/交互优化）。
> 本文档为正式归档，回滚指引见文末。旧版式备份文件**永久保留，不得删除**（Jason 2026-07-26 明确要求）。

## 一、设计体系定稿（sections-v1）

- **基调**：白底为主，Accenture Purple `#A100FF`/`#7500C0` 为主站重音色；无埃森哲「>」logo 元素（侵权红线）
- **组件语言**：胶囊徽章 Hero（badge + 大标题重音词着色 + hero-sub + stat 条）、双层板块头 sec-head（英文眉题 + 中文标题 + 渐隐细线 + 计数）、统一卡片 card（tag pill + 来源 + 标题 + 正文 + 底部动作行）、排行条 rank-row（GitHub/LMArena 用）
- **栏目 accent 色**：每栏目一个专属色，页面级 CSS 变量 `--acc/--acc-deep/--acc-ghost/--acc-band` 切换
  - 精读室 靛蓝 #4F46E5 · 开源榜 翠绿 #10B981 · 竞技场 琥珀 #F59E0B · 档案库 青 #06B6D4 · 研修院 玫红 #EC4899 · 首页/关于/日报详情 主站紫 #A100FF
- **图标**：线性 SVG（Feather 风格 2px），UI chrome 全站无 emoji
- **核心文件**：`src/styles/sections.css`（共享样式）+ `src/components/SectionSprite.astro`（SVG symbol 库）
- **设计稿**：`docs/redesign-mockup-v14.html`（首页终稿）、`docs/redesign-mockup-sections-v1.html`（栏目页终稿）；过程稿 v1-v13 均保留

## 二、栏目命名体系（Jason 拍板）

| 路径 | 中文名（导航） | EN badge | H1 |
|---|---|---|---|
| `/` | 情报流 | FEED | AI 情报局（v14 定稿） |
| `/archive/` | 档案库 | VAULT | 档案库 |
| `/github/` | 开源榜 | GH TRENDS | 开源榜 |
| `/lmarena/` | 竞技场 | ARENA | 模型竞技场 |
| `/reads/` | 精读室 | READS | 精读室 |
| `/learn/` | 研修院 | ACADEMY | 研修院 |
| `/about/` | 关于 | ABOUT | 关于本站 |
| `/x/` | （导航隐身） | — | 保留页面，入口=首页 Signals 区「查看全部」 |

## 三、commit 时间线（全部已上线，GHA 部署 success）

| commit | 内容 |
|---|---|
| `2551029` | 首页 v13：hero brief、交替淡底色、X section、卡片动作行 |
| `f111b9d` | 首页 v14：「AI 情报局」标题、statement 观点卡、双层板块头 |
| `9adbd71` | **5 栏目页统一风格**（reads/github/lmarena/archive/learn），各自 accent |
| `57d8395` | **栏目重命名** + 关于页 sections-v1 改版（黑底 Hero + emoji 全清） |
| `6e5763e` | 档案库月份折叠：`<details>` 默认只开当月，零 JS |
| `c758835` | 全站卡片字号 +1px |
| `deec5d7` | 再 +1px（终值：卡片标题 17.5px / 正文 15-15.5px / insight 14.5px） |
| `2f62768` | 精读详情页字号同步（.reads-content 基准 17.5px） |
| `92dc2d2` | **两个详情页统一**：/d/[date]（紫 FEED Hero + 四板块 sec-head）+ /reads/[slug]（靛蓝 READS Hero + 6 区块 emoji 标题换眉题板块头） |
| `ed3aab9` | AudioPlayer 白底适配（原暗色玻璃拟态在白底上隐形） |

## 四、关键决策与教训

1. **数据层零改动**：全程只动渲染层，`src/data/` 与数据 lib 未碰；stat 数字全部动态实算，禁止 hardcode 设计稿假数字
2. **LMArena 数据无 ELO 分数**（只有 rank）：排行条右侧值槽改显示月度 delta，bar 按 `(51-rank)/50` 渲染
3. **换背景色系要连带查嵌入组件**：AudioPlayer 原注释「和 Hero 暗色风格融合」，详情页改白底后整个隐形——重构容器时必须清查子组件配色假设
4. **QC 流程**：每次渲染层 commit 过 MK46 审（verdict 记录：9adbd71 与 57d8395 = APPROVE_WITH_WARNINGS 均已修复告警项后上线；92dc2d2 = APPROVE 零问题）
5. 旧组件 `Hero/SectionBlock/Brief/DateNav` 详情页重写后已全部无引用（待清理，确认无其他页面引用后可归档删除——删除前需再确认）

## 五、回滚指引

- **git 层**：任意 commit 可 `git revert <hash>`；整体回到改版前 = revert 至 `03f4fcf`（改版前最后一个功能 commit）
- **文件层备份**（`docs/` 下，git 已追踪，**永久保留**）：
  - `index.astro.bak-v-old` — 改版前首页
  - `reads-index / github / lmarena-index / archive / learn-index / about .astro.bak-pre-sections-v1` — 六个页面旧版
  - `d-date.astro.bak-pre-sections-v1`、`reads-slug.astro.bak-pre-sections-v1` — 两个详情页旧版
- **设计过程稿**：`docs/redesign-mockup-v1~v14.html`、`docs/redesign-mockup-sections-v1.html`、调研报告 `docs/redesign-research-2026-07.md`、过程截图 `docs/shots/`

## 六、遗留待办

- [ ] xSource 空串 fallback（low，QC 提出）
- [ ] 旧组件 Footer/Hero/SectionBlock/Brief/DateNav 引用清查后归档（删除前先向 Jason 确认）
- [ ] reads「配播客」stat 全覆盖时的表述优化（low）
- [ ] 未来扩展 SectionKey 枚举时同步 `d/[date].astro` 的 sectionMeta 硬编码
