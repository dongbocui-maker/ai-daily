---
slug: obsidian-skills
title: "Obsidian Skills：CEO 亲自给 AI 写的官方教材"
subtitle: "kepano 开源的 6 个 Agent Skills 全文整理 —— 教会任何 AI 编程助手正确读写 Obsidian 的开放格式，八个多月 48K Star 的「厂商自写说明书」新范式"
sourceUrl: "https://github.com/kepano/obsidian-skills"
sourceLabel: "GitHub · kepano/obsidian-skills（MIT）"
updated: "2026-09-20"
---

<div class="not-prose my-6 flex flex-wrap gap-3">
<a href="https://github.com/kepano/obsidian-skills" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-2 px-4 py-2.5 bg-accent-ink text-white text-sm font-semibold rounded hover:bg-accent-purple transition">⭐ GitHub 仓库（48.6K Star）</a>
<a href="https://agentskills.io/specification" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-2 px-4 py-2.5 border border-accent-gray-300 text-sm font-semibold rounded hover:border-accent-purple hover:text-accent-purple transition">📐 Agent Skills 规范</a>
<a href="https://help.obsidian.md/cli" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-2 px-4 py-2.5 border border-accent-gray-300 text-sm font-semibold rounded hover:border-accent-purple hover:text-accent-purple transition">📄 Obsidian CLI 官方文档</a>
<a href="https://jsoncanvas.org/" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-2 px-4 py-2.5 border border-accent-gray-300 text-sm font-semibold rounded hover:border-accent-purple hover:text-accent-purple transition">🗺 JSON Canvas 开放规范</a>
</div>

<aside class="not-prose my-8 px-6 py-6 bg-gradient-to-br from-accent-purple/10 to-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-base font-bold text-accent-purple tracking-wide uppercase mb-3">🎯 核心观点汇总（给忙人看的精华）</h3>
<ul class="space-y-2 text-[15px] text-accent-gray-800 leading-relaxed list-disc pl-5">
<li><strong>这是软件厂商「亲自给 AI 写说明书」的标杆案例</strong>：Obsidian CEO Steph Ango（kepano）本人维护，不建服务、不写运行时代码，只用 6 个纯文本 SKILL.md 教会所有兼容 agent（Claude Code / Codex / OpenCode……）正确使用自家产品。</li>
<li><strong>数据实证需求侧热度</strong>：2026 年 1 月 2 日创建，9 月 15 日仍在更新，八个多月拿下 48,600+ Star（GitHub API 实测，2026-09-20）。</li>
<li><strong>6 个 skill 各管一个开放格式</strong>：Obsidian 方言 Markdown、Bases 数据库、JSON Canvas 白板、Obsidian CLI、Defuddle 网页抽取、Knap 模板渲染——组合起来是一条「网页 → 干净 Markdown → 模板化笔记 → 数据库视图」的完整流水线。</li>
<li><strong>Skills 比 MCP 更轻</strong>：纯文本、零运行时、可 git 管理、跨 agent 通用。「教 AI 用某个工具」这件事，正在从「建服务」退化（进化）成「写文档」。</li>
</ul>
</aside>

## 背景：为什么一个「文档仓库」能拿 48K Star

**Steph Ango（网名 kepano）是 Obsidian 的 CEO**，也是 Obsidian「文件优先于应用」（*File over app*）哲学的提出者。2026 年 1 月 2 日，他在个人 GitHub 上开源了 `obsidian-skills`——一套遵循 [Agent Skills 规范](https://agentskills.io/specification)的技能包，让任何兼容的 AI 编程助手（Claude Code、Codex、OpenCode 等）学会正确读写 Obsidian 的全部开放格式。

仓库原文对自己的定义只有一句话：

> Agent skills for Obsidian. Teach your agent to use Obsidian CLI and open formats including Markdown, Bases, JSON Canvas.

**这个仓库值得管理者注意的地方，不在代码——它几乎没有代码**。6 个 skill 全部是 Markdown 文档：语法说明、工作流步骤、常见陷阱、验证清单。它证明了一件事：当 AI agent 已经具备通用读写能力时，「教会它用你的产品」最高杠杆的方式未必是新建一个服务，而可以是**把产品文档重写成 AI 能按步骤执行的操作手册**。八个多月 48,600+ star、9 月 15 日还在持续更新（数据来自 GitHub API，2026-09-20 实测），说明需求侧的热度是真实的。

**安装极简**（任选其一）：

```bash
# 通用（任何兼容 skills 的 agent）
npx skills add https://github.com/kepano/obsidian-skills

# Claude Code marketplace
/plugin marketplace add kepano/obsidian-skills
/plugin install obsidian@obsidian-skills
```

---

## 六个 Skill 逐个导读

<nav class="not-prose my-8 px-6 py-5 bg-white border border-accent-gray-200 rounded" aria-label="skill 导航">
<div class="text-[12px] font-semibold tracking-widest uppercase text-accent-purple mb-3">🧭 快速导航</div>
<div class="flex flex-wrap gap-2">
<a href="#1-obsidian-markdown写出地道的-obsidian-方言" class="px-3 py-1 text-[13px] bg-accent-gray-50 border border-accent-gray-200 rounded hover:border-accent-purple hover:text-accent-purple transition">1 obsidian-markdown</a>
<a href="#2-obsidian-bases把一堆笔记变成数据库" class="px-3 py-1 text-[13px] bg-accent-gray-50 border border-accent-gray-200 rounded hover:border-accent-purple hover:text-accent-purple transition">2 obsidian-bases</a>
<a href="#3-json-canvas让-ai-画白板和流程图" class="px-3 py-1 text-[13px] bg-accent-gray-50 border border-accent-gray-200 rounded hover:border-accent-purple hover:text-accent-purple transition">3 json-canvas</a>
<a href="#4-obsidian-cli用命令行遥控正在运行的-obsidian" class="px-3 py-1 text-[13px] bg-accent-gray-50 border border-accent-gray-200 rounded hover:border-accent-purple hover:text-accent-purple transition">4 obsidian-cli</a>
<a href="#5-defuddle把网页洗成干净的-markdown" class="px-3 py-1 text-[13px] bg-accent-gray-50 border border-accent-gray-200 rounded hover:border-accent-purple hover:text-accent-purple transition">5 defuddle</a>
<a href="#6-knap用模板批量生产笔记" class="px-3 py-1 text-[13px] bg-accent-gray-50 border border-accent-gray-200 rounded hover:border-accent-purple hover:text-accent-purple transition">6 knap</a>
</div>
</nav>

## 1. obsidian-markdown：写出地道的 Obsidian 方言

> **官方用途描述**：Create and edit Obsidian Flavored Markdown with wikilinks, embeds, callouts, properties, and other Obsidian-specific syntax. Use when working with .md files in Obsidian, or when the user mentions wikilinks, callouts, frontmatter, tags, embeds, or Obsidian notes.

**中文导读**：这是六个 skill 里最基础、也最常用的一个。Obsidian 的 Markdown 在 CommonMark/GFM 之上扩展了一批私有语法——双链 wikilink、嵌入 embed、标注块 callout、frontmatter 属性、隐藏注释等。通用 AI 不学这套方言，写出来的笔记在 Obsidian 里就是「能看但不对」：链接不会跟随重命名、标注块渲染不出来、属性写错位置。这个 skill 的价值在于把「地道」教给 AI，并且给了一条明确的判断规则——**库内笔记一律用 `[[wikilink]]`（Obsidian 自动跟踪重命名），只有外部 URL 才用标准 Markdown 链接**。

skill 定义的标准工作流五步：加 frontmatter 属性 → 标准 Markdown 写正文 → wikilink 连接相关笔记 → `![[...]]` 嵌入内容 → callout 高亮关键信息，最后在阅读视图验证渲染。核心语法速览（汇编自原文各节示例，中文注释为编者添加）：

```markdown
[[Note Name]]                 链接笔记
[[Note Name|Display Text]]    自定义显示文本
[[Note Name#Heading]]         链接到小节
[[Note Name#^block-id]]       链接到段落块
![[Note Name]]                嵌入整篇笔记
![[image.png|300]]            嵌入图片并限宽
![[document.pdf#page=3]]      嵌入 PDF 第 3 页

> [!warning] Custom Title     标注块（callout）
> [!faq]- 默认折叠            可折叠标注块

==高亮文本==                  Obsidian 专属高亮
%%隐藏注释%%                  阅读视图不可见
```

常用 callout 类型：`note` / `tip` / `warning` / `info` / `example` / `quote` / `bug` / `danger` / `success` / `question` / `todo` 等。此外还覆盖 LaTeX 数学、Mermaid 图表（节点可挂 `internal-link` class 链回笔记）、脚注、嵌套标签。

## 2. obsidian-bases：把一堆笔记变成数据库

> **官方用途描述**：Create and edit Obsidian Bases (.base files) with views, filters, formulas, and summaries. Use when working with .base files, creating database-like views of notes, or when the user mentions Bases, table views, card views, filters, or formulas in Obsidian.

**中文导读**：Bases 是 Obsidian 2025 年推出的「无数据库的数据库」（推出时间为编者补充的外部事实，非仓库内容）——一个 `.base` 文件本质是一段 YAML，声明筛选条件（按标签/文件夹/属性/日期）、计算公式和视图（表格/卡片/列表/地图），Obsidian 就把散落的 Markdown 笔记实时聚合成 Notion 式的数据库视图，**而底层数据仍然是一个个纯文本文件**。这是「File over app」哲学的具体落地。这个 skill 的主文档是六个中最长的，因为 YAML 引号规则和公式表达式是 AI 最容易翻车的地方——skill 里专门列了验证步骤：先验 YAML 合法性，再查所有引用的属性和公式是否已定义，最后在 Obsidian 里打开确认渲染。

一个典型 `.base` 文件的骨架（原文示例节选）：

```yaml
filters:
  and:
    - 'status == "active"'
    - not:
        - 'file.hasTag("archived")'
formulas:
  formula_name: 'expression'
summaries:
  custom_summary_name: 'values.mean().round(3)'
views:
  - type: table          # table | cards | list | map
    name: "View Name"
    groupBy:
      property: property_name
      direction: ASC
    order:
      - file.name
```

对企业用户的联想：这套「筛选 + 公式 + 视图都是声明式纯文本」的设计，天然对 AI 友好——agent 改一行 YAML 就等于重构了一个数据库视图，且全程可 git diff、可回滚。

## 3. json-canvas：让 AI 画白板和流程图

> **官方用途描述**：Create and edit JSON Canvas files (.canvas) with nodes, edges, groups, and connections. Use when working with .canvas files, creating visual canvases, mind maps, flowcharts, or when the user mentions Canvas files in Obsidian.

**中文导读**：JSON Canvas 是 Obsidian 主导的**开放白板格式**（[jsoncanvas.org](https://jsoncanvas.org/)，Spec 1.0）——一个 `.canvas` 文件就是 `{"nodes": [], "edges": []}` 两个数组，节点带坐标和尺寸，边连接节点。有了这个 skill，你可以直接让 AI「把这篇会议纪要画成决策流程图」「给这个项目做张思维导图」，产出的是可以在 Obsidian 里继续手动编辑的白板，而不是一张死图片。

skill 把三个高频工作流写成了可执行清单——新建画布、往现有画布加节点、连接两个节点——每条都以「Validate」收尾：ID 必须是唯一 16 位 hex、所有 `fromNode`/`toNode` 必须能解析到真实节点、新节点坐标要避开现有节点（留 50–100px 间距）。这些恰是 AI 徒手生成 JSON 时最常犯的错。四种节点类型：`text`（Markdown 文本）、`file`（引用库内文件）、`link`（外部 URL）、`group`（分组容器）。

## 4. obsidian-cli：用命令行遥控正在运行的 Obsidian

> **官方用途描述**：Interact with Obsidian vaults using the Obsidian CLI to read, create, search, and manage notes, tasks, properties, and more. Also supports plugin and theme development with commands to reload plugins, run JavaScript, capture errors, take screenshots, and inspect the DOM. Use when the user asks to interact with their Obsidian vault, manage notes, search vault content, perform vault operations from the command line, or develop and debug Obsidian plugins and themes.

**中文导读**：前三个 skill 教 AI「写对文件格式」，这个 skill 教 AI「操作正在运行的 Obsidian 应用」（要求 Obsidian 处于打开状态）。两类能力：**日常笔记操作**——读写、搜索、追加日记、管理任务和属性、查反链；**插件/主题开发调试**——这部分最惊喜，AI 可以改完插件代码后自己 reload、抓错误、截图、查 DOM、跑 JavaScript，形成完整的「改码 → 重载 → 验证」闭环，等于把 Obsidian 变成了 AI 可测试的开发环境。

```bash
# 日常操作
obsidian read file="My Note"
obsidian create name="New Note" content="# Hello" silent
obsidian search query="search term" limit=10
obsidian daily:append content="- [ ] New task"
obsidian property:set name="status" value="done" file="My Note"
obsidian backlinks file="My Note"

# 插件开发闭环（原文工作流）
obsidian plugin:reload id=my-plugin   # 1. 重载插件
obsidian dev:errors                   # 2. 查错误，有错修完回到 1
obsidian dev:screenshot path=s.png    # 3. 截图目检
obsidian dev:console level=error      # 4. 查控制台
```

文件定位规则值得记：`file=` 按 wikilink 方式解析（只要名字），`path=` 用库根精确路径，都不传则作用于当前活跃文件。

## 5. defuddle：把网页洗成干净的 Markdown

> **官方用途描述**：Extract clean Markdown from HTML pages with Defuddle CLI.

**中文导读**：六个 skill 里最短的一个（不到 1KB），但定位精准。[Defuddle](https://github.com/kepano/defuddle) 是 kepano 自己写的正文抽取器（Obsidian Web Clipper 的底层引擎，Readability 的替代品），把网页的导航、广告、杂物全部剥掉，只留正文 Markdown。skill 里明确指示 agent：**处理标准网页时优先用 Defuddle 而不是内置的 WebFetch——因为洗干净的正文能显著省 token**。这是很务实的成本视角（编者注：原文仅称 reducing token usage、未给量级；以本站实践经验，同一篇文章原始 HTML 常达几十万字符，抽完正文往往只剩几千）。

```bash
defuddle parse <url> --md              # 输出 Markdown
defuddle parse <url> --md -o note.md   # 存文件
defuddle parse <url> -p title          # 只取标题等元数据
```

## 6. knap：用模板批量生产笔记

> **官方用途描述**：Render Markdown from templates and structured data using Knap CLI. Use when the user asks to apply a Knap template, turn JSON or CSV data into notes, batch-generate Markdown files, or format Defuddle output into a note.

**中文导读**：[Knap](https://github.com/obsidianmd/knap) 是 Obsidian 官方的模板渲染 CLI（`{{ variable }}` 变量 + `|` 过滤器 + `{% if %}` 逻辑，Web Clipper 同款模板语言）。它解决的是「结构化数据 → 批量笔记」的最后一公里：一份 CSV 或 JSON 数组，一个模板文件，一条命令生成一批规范一致的 Markdown。skill 里最有价值的是**与 defuddle 的管道组合**——抓网页和格式化笔记从两步并成一步：

```bash
# 网页 → JSON（含正文 Markdown）→ 按模板渲染成笔记，一条管道
defuddle parse https://example.com/article --md --json \
  | knap render template.md --data - -o note.md

# CSV 批量生成，每行一个文件
knap batch template.md --data articles.csv --output-dir notes \
  --filename '{{ title | safe_name }}.md'
```

细节设计很周到：`--dry-run` 先验证再落盘、已有文件必须 `--overwrite`、`safe_name` 过滤器处理文件名非法字符、`knap validate` 渲染前先查模板语法。**defuddle（抓取）→ knap（模板化）→ obsidian-markdown（方言规范）→ obsidian-bases（数据库视图）四件套连起来，就是一条 AI 可全自动执行的「网页到知识库」流水线**——这大概也是 kepano 把它们放进同一个仓库的原因。

---

## 编辑判断：这个仓库真正的启示

**（以下为编辑观点，非原文内容）**

1. **「厂商自写 AI 说明书」正在成为新范式**。对比两条路线：做一个 MCP server 需要开发、部署、维护运行时；写一套 skills 只需要把文档重写成操作手册。kepano 选了后者，八个多月 48K star。对任何有开放格式/CLI 的产品团队，这是值得抄的作业——你的产品文档如果 AI 读不懂、不会照着做，等于在 AI 时代没有文档。

2. **Skills 的本质是「把专家经验写成检查清单」**。细看这 6 个文件，最值钱的不是语法表（模型多半见过），而是工作流步骤、验证清单和陷阱提示——「YAML 特殊字符要引号」「块 ID 在列表后要另起一行」「节点间距留 50–100px」。这与我们在 [Agentic Design Patterns 精读](/learn/agentic-design-patterns/)里看到的结论一致：AI 的可靠性来自把隐性知识显性化。

3. **开放格式是 AI 时代的护城河，也是入场券**。Obsidian 敢这么做，因为它的所有格式（Markdown/YAML/JSON Canvas）都是纯文本开放规范——AI 天然能读写。封闭二进制格式的竞品想跟进，得先补「格式开放」这一课。*File over app* 在 AI agent 时代获得了第二层含义：**文件不仅属于用户，也属于用户的 AI**。
