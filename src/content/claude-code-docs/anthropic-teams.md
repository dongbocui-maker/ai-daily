---
slug: anthropic-teams-claude-code
title: "How Anthropic Teams Use Claude Code"
subtitle: "Anthropic 官方 PDF · 10 个内部团队的实战案例"
sourceUrl: "https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf"
sourceLabel: "anthropic.com · PDF"
updated: "2026-05-17"
---

<aside class="not-prose my-8 px-6 py-6 bg-gradient-to-br from-accent-purple/10 to-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-base font-bold text-accent-purple tracking-wide uppercase mb-3">🎯 核心观点汇总（给忙人看的精华）</h3>
<ul class="space-y-2 text-[15px] text-accent-gray-800 leading-relaxed list-disc pl-5">
<li><strong>Claude Code 不只是给工程师用的</strong>。10 个团队里 4 个是非技术或半技术职能（增长营销、产品设计、法务、数据基础设施的财务子场景），他们都在用 Claude Code 完成传统上需要 dev 资源才能做的事——这是分水岭式的能力下放。</li>
<li><strong>CLAUDE.md 是杠杆最高的单点投入</strong>。数据基础设施和 RL 工程都把它列为头号建议——把团队特有的工具、命令偏好、踩坑模式写进去，Claude 在重复性任务上的表现立刻拉满。</li>
<li><strong>"非同步 + checkpoint-heavy" 是高产范式</strong>。产品研发用 auto-accept 模式让 Claude 跑 30 分钟再回来 review；数据科学叫它「老虎机」（commit 后放手让它跑，不行就重开）；RL 工程的 try-and-rollback 是同一招——核心是 git 提供的廉价回滚让"放手让它干"变成 dominant strategy。</li>
<li><strong>原型加速跨越职能边界</strong>。产品设计师直接改前端状态管理代码、法务团队 1 小时做出 family accessibility app、增长营销自建 Figma 插件+MCP server——共同点是从「写规格交给工程师」变成「自己直接做出可演示原型」，沟通成本从周降到小时。</li>
<li><strong>自定义 slash command + MCP server 是高级用法的两大支柱</strong>。安全工程团队贡献了 monorepo 一半的自定义 slash command；增长营销建了 Meta Ads MCP server；数据基础设施用 MCP 取代 BigQuery CLI 做敏感数据访问。这两类自定义能力是 power user 与普通用户的分野。</li>
<li><strong>对不熟悉的代码库 / 语言，Claude Code 是 onboarding 加速器</strong>。Inference、API、安全工程、产品研发都强调"用 Claude 探索陌生 codebase 比问同事或读 GitHub 快得多"——新人贡献周期从「周」降到「天」。</li>
<li><strong>测试生成几乎是每个工程团队的标配用法</strong>。Inference、产品研发、RL 工程、安全工程都把"先让 Claude 写测试再写实现"作为 TDD 的低成本启动方式——测试既是质量保障也是 Claude 的自检回路。</li>
<li><strong>Claude.ai 做规划、Claude Code 做实施，是非技术团队的通用模式</strong>。法务和增长营销都明确把这个两步走列为关键经验——先用 Claude.ai 把想法聊清楚、生成详细 prompt，再交给 Claude Code 一步步执行。</li>
</ul>
</aside>

---

<aside class="not-prose my-8 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-sm font-bold text-accent-purple tracking-wide uppercase mb-2">📌 章节导读 · 1. 数据基础设施团队</h3>
<p class="text-[15px] text-accent-gray-800 leading-relaxed">负责为全公司团队组织业务数据的中枢团队。痛点是日常重复性的数据工程任务、跨网络/Kubernetes 的复杂排障、以及如何让非技术同事（如财务团队）也能自助跑数据流程。Claude Code 让他们既能在 K8s 故障时绕开"必须拉系统 / 网络团队"的瓶颈，也能把"用自然语言描述工作流"开放给零代码经验的同事——同时大幅压缩新数据科学家的 onboarding 时间。</p>
</aside>

## Claude Code for Data Infrastructure

The Data Infrastructure team organizes all business data for teams across the company. They use Claude Code for automating routine data engineering tasks, troubleshooting complex infrastructure issues, and creating documented workflows for technical and non-technical team members to access and manipulate data independently.

### Main Claude Code use cases

**Kubernetes debugging with screenshots**
When Kubernetes clusters went down and weren't scheduling new pods, the team used Claude Code to diagnose the issue. They fed screenshots of dashboards into Claude Code, which guided them through Google Cloud's UI menu by menu until they found a warning indicating pod IP address exhaustion. Claude Code then provided the exact commands to create a new IP pool and add it to the cluster, bypassing the need to involve networking specialists.

**Plain text workflows for finance team**
The team showed finance team members how to write plain text files describing their data workflows, then load them into Claude Code to get fully automated execution. Employees with no coding experience could describe steps like "query this dashboard, get information, run these queries, produce Excel output," and Claude Code would execute the entire workflow, including asking for required inputs like dates.

**Codebase navigation for new hires**
When new data scientists join the team, they're directed to use Claude Code to navigate their massive codebase. Claude Code reads their Claude.md files (documentation), identifies relevant files for specific tasks, explains data pipeline dependencies, and helps newcomers understand which upstream sources feed into dashboards. This replaces traditional data catalogs and discoverability tools.

**End-of-session documentation updates**
The team asks Claude Code to summarize completed work sessions and suggest improvements at the end of each task. This creates a continuous improvement loop where Claude Code helps refine the Claude.md documentation and workflow instructions based on actual usage, making subsequent iterations more effective.

**Parallel task management across multiple instances**
When working on long-running data tasks, they open multiple instances of Claude Code in different repositories for different projects. Each instance maintains full context, so when they switch back after hours or days, Claude Code remembers exactly what they were doing and where they left off, enabling true parallel workflow management without context loss.

### Team impact

**Resolved infrastructure problems without specialized expertise**
Resolved Kubernetes cluster issues that would normally require pulling in systems or networking team members, using Claude Code to diagnose problems and provide exact fixes.

**Accelerated onboarding**
New data analysts and team members can quickly understand complex systems and contribute meaningfully without extensive guidance.

**Enhanced support workflow**
Can process much larger data volumes and identify anomalies (like monitoring 200 dashboards) that would be impossible for humans to review manually.

**Enabled cross-team self-service**
Finance teams with no coding experience can now execute complex data workflows independently.

### Top tips from the Data Infrastructure team

**Write detailed Claude.md files**
The better you document your workflows, tools, and expectations in Claude.md files, the better Claude Code performs. This made Claude Code excel at routine tasks like setting up new data pipelines when you have existing patterns.

**Use MCP servers instead of CLI for sensitive data**
They recommend using MCP servers rather than the BigQuery CLI to maintain better security control over what Claude Code can access, especially for handling sensitive data that requires logging or has potential privacy concerns.

**Share team usage sessions**
The team held sessions where members demonstrated their Claude Code workflows to each other. This helped spread best practices and showed different ways to use the tool they might not have discovered on their own.

---

<aside class="not-prose my-8 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-sm font-bold text-accent-purple tracking-wide uppercase mb-2">📌 章节导读 · 2. 产品研发团队（即 Claude Code 团队本身）</h3>
<p class="text-[15px] text-accent-gray-800 leading-relaxed">用自己产品迭代自己产品的"dogfooding"团队。他们的关键洞察是任务分层——边缘性 / 原型性的活塞进 auto-accept 模式让 Claude 跑自动循环（Vim 模式 70% 由 Claude 自主完成），而触碰核心业务逻辑的部分则保持 synchronous 监督。git 干净状态 + 频繁 commit checkpoint 是他们让"放手让它干"风险可控的前提。</p>
</aside>

## Claude Code for Product Development

The Claude Code team uses their own product to build updates to Claude Code, expanding the product's enterprise capabilities and agentic loop functionalities.

### Main Claude Code use cases

**Fast prototyping with auto-accept mode**
Engineers use Claude Code for rapid prototyping by enabling "auto-accept mode" (shift+tab) and setting up autonomous loops where Claude writes code, runs tests, and iterates continuously. They give Claude abstract problems they're unfamiliar with, let it work autonomously, then review the 80% complete solution before taking over for final refinements. Teams emphasize starting from a clean git state and committing checkpoints regularly so they can easily revert any incorrect changes if Claude goes off track.

**Synchronous coding for core features**
For more critical features touching the application's business logic, the team works synchronously with Claude Code, giving detailed prompts with specific implementation instructions. They monitor the process in real-time to ensure code quality, style guide compliance, and proper architecture while letting Claude handle the repetitive coding work.

**Building Vim mode**
One of their most successful async projects was implementing Vim key bindings for Claude Code. They asked Claude to build the entire feature (despite it not being a priority), and roughly 70% of the final implementation came from Claude's autonomous work, requiring only a few iterations to complete.

**Test generation and bug fixes**
They use Claude Code to write comprehensive tests after implementing features and handle simple bug fixes identified in pull request reviews. They also leverage GitHub Actions integration to have Claude automatically address Pull Request comments like formatting issues or function renaming.

**Codebase exploration**
When working with unfamiliar codebases (like the monorepo or API side), the team uses Claude Code to quickly understand how systems work. Instead of waiting for Slack responses, they ask Claude directly for explanations and code references, saving significant time in context switching.

### Team impact

**Faster feature implementation**
Successfully implemented complex features like Vim mode with 70% of code written autonomously by Claude.

**Improved development velocity**
Can rapidly prototype features and iterate on ideas without getting bogged down in implementation details.

**Enhanced code quality through automated testing**
Claude generates comprehensive tests and handles routine bug fixes, maintaining high standards while reducing manual effort.

**Better codebase exploration**
Team members can quickly understand unfamiliar parts of the monorepo without waiting for colleague responses.

### Top tips from the Claude Code team

**Create self-sufficient loops**
Set up Claude to verify its own work by running builds, tests, and lints automatically. This allows Claude to work longer autonomously and catch its own mistakes, especially effective when you ask Claude to generate tests before writing code.

**Develop task classification intuition**
Learn to distinguish between tasks that work well asynchronously (peripheral features, prototyping) versus those needing synchronous supervision (core business logic, critical fixes). Abstract tasks on the product's edges can be handled with "auto-accept mode," while core functionality requires closer oversight.

**Form clear, detailed prompts**
When components have similar names or functions, be extremely specific in your requests. The better and more detailed your prompt, the more you can trust Claude to work independently without unexpected changes to the wrong parts of the codebase.

---

<aside class="not-prose my-8 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-sm font-bold text-accent-purple tracking-wide uppercase mb-2">📌 章节导读 · 3. 安全工程团队</h3>
<p class="text-[15px] text-accent-gray-800 leading-relaxed">聚焦 SDLC 安全、供应链安全、开发环境安全。痛点是事故响应时间和 Terraform 审批形成的瓶颈。最具标志性的数据是——这支团队贡献了整个 monorepo 50% 的自定义 slash command 实现，是 power user 的范本。除了写代码和审 Terraform，他们也大量用 Claude Code 把多个文档源合成成 markdown runbook，再把这些精简文档当作排障时的上下文。</p>
</aside>

## Claude Code for Security Engineering

The Security Engineering team focuses on securing the software development lifecycle, supply chain security, and development environment security. They use Claude Code extensively for writing and debugging code.

### Main Claude Code use cases

**Complex infrastructure debugging**
When working on incidents, they feed Claude Code stack traces and documentation, asking it to trace control flow through the codebase. This significantly reduces time-to-resolution for production issues, allowing them to understand problems that would normally take 10-15 minutes of manual code scanning in about 5 minutes.

**Terraform code review and analysis**
For infrastructure changes requiring security approval, they copy Terraform plans into Claude Code to ask "what's this going to do? Am I going to regret this?" This creates tighter feedback loops and makes it easier for the security team to quickly review and approve infrastructure changes, reducing bottlenecks in the development process.

**Documentation synthesis and runbooks**
They have Claude Code ingest multiple documentation sources and create markdown runbooks, troubleshooting guides, and overviews. They use these condensed documents as context for debugging real issues, creating a more efficient workflow than searching through full knowledge bases.

**Test-driven development workflow**
Instead of their previous "design doc → janky code → refactor → give up on tests" pattern, they now ask Claude Code for pseudocode, guide it through test-driven development, and periodically check in to steer it when stuck, resulting in more reliable and testable code.

**Context switching and project onboarding**
When contributing to existing projects like "dependant" (a web application for security approval workflows), they use Claude Code to write, review, and execute specifications written in markdown and stored in the codebase, enabling meaningful contributions within days instead of weeks.

### Team impact

**Reduced incident resolution time**
Infrastructure debugging that normally takes 10-15 minutes of manual code scanning now takes about 5 minutes.

**Improved security review cycle**
Terraform code reviews for security approval happen much faster, eliminating developer blocks while waiting for security team approval.

**Enhanced cross-functional contribution**
Team members can meaningfully contribute to projects within days instead of weeks of context building.

**Better documentation workflow**
Synthesized troubleshooting guides and runbooks from multiple sources create more efficient debugging processes.

### Top tips from the Security Engineering team

**Use custom slash commands extensively**
Security engineering uses 50% of all custom slash command implementations in the entire monorepo. These custom commands streamline specific workflows and speed up repeated tasks.

**Let Claude talk first**
Instead of asking targeted questions for code snippets, they now tell Claude Code to "commit your work as you go" and let it work autonomously with periodic check-ins, resulting in more comprehensive solutions.

**Leverage it for documentation**
Beyond coding, Claude Code excels at synthesizing documentation and creating structured outputs. They provide writing samples and formatting preferences to get documents they can immediately use in Slack, Google Docs, and other tools to avoid interface switching fatigue.

---

<aside class="not-prose my-8 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-sm font-bold text-accent-purple tracking-wide uppercase mb-2">📌 章节导读 · 4. 推理团队（Inference）</h3>
<p class="text-[15px] text-accent-gray-800 leading-relaxed">负责 Claude 推理过程中读取 prompt 与生成响应时的内存系统。团队里有大量 ML 背景较弱的成员，Claude Code 对他们而言最大的价值是"知识弥合"——查模型函数定义、跨语言写测试、解释陌生概念，把 1 小时 Google 缩短到 10-20 分钟（80% 时间节省）。"先用代码生成建立信任，再扩展到测试和复杂任务"是他们的渐进采纳路径。</p>
</aside>

## Claude Code for Inference

The Inference team manages the memory system that stores information while Claude reads your prompt and generates its response. Team members, especially those who are new to machine learning, can use Claude Code extensively to bridge that knowledge gap and accelerate their work.

### Main Claude Code use cases

**Codebase comprehension and onboarding**
The team relies heavily on Claude Code to quickly understand the architecture when joining a complex codebase. Instead of manually searching GitHub repos, they ask Claude to find which files call specific functionalities, getting results in seconds rather than asking colleagues or searching manually.

**Unit test generation with edge case coverage**
After writing core functionality, they ask Claude to write comprehensive unit tests. Claude automatically includes missed edge cases, completing what would normally take significant mental energy in minutes, acting like a coding assistant they can review.

**Machine learning concept explanation**
Without a machine learning background, team members depend on Claude to explain model-specific functions and settings. What would require an hour of Google searching and reading documentation now takes 10-20 minutes, reducing research time by 80%.

**Cross-language code translation**
When testing functionality in different programming languages, they explain what they want to test and Claude writes the logic in the required language (like Rust), eliminating the need to learn new languages just for testing purposes.

**Command recall and Kubernetes management**
Instead of remembering complex Kubernetes commands, they ask Claude for the correct syntax, like "how to get all pods or deployment status," and receive the exact commands needed for their infrastructure work.

### Team impact

**Accelerated ML concept learning**
Research time reduced by 80% — what took an hour of Google searching now takes 10-20 minutes.

**Faster codebase navigation**
Can find relevant files and understand system architecture in seconds instead of asking colleagues.

**Comprehensive test coverage**
Claude automatically generates unit tests with edge cases, relieving mental burden while maintaining code quality.

**Language barrier elimination**
Can implement functionality in unfamiliar languages like Rust without needing to learn it.

### Top tips from the Inference team

**Test knowledge base functionality first**
Try asking various questions to see if Claude can answer faster than Google search. If it's faster and more accurate, it's a valuable time-saving tool for your workflow.

**Start with code generation**
Give Claude specific instructions and ask it to write logic, then verify correctness. This helps build trust in the tool's capabilities before using it for more complex tasks.

**Use it for test writing**
Having Claude write unit tests relieves significant pressure from daily development work. Leverage this feature to maintain code quality without spending time thinking through all test cases manually.

---

<aside class="not-prose my-8 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-sm font-bold text-accent-purple tracking-wide uppercase mb-2">📌 章节导读 · 5. 数据科学与可视化团队</h3>
<p class="text-[15px] text-accent-gray-800 leading-relaxed">他们的核心需求是"理解模型在训练 / 评估时究竟在做什么"，但搭这种可视化工具传统上需要 full-stack 能力。他们"几乎不会 JS/TS"，却用 Claude Code 写出了 5000 行的 React TypeScript app。两个最值得记住的隐喻：把 Claude 当"老虎机"（commit、放手让它跑 30 分钟、不行就重开），以及"被监督时打断它叫它简化"（默认会过度复杂化，但响应"simpler"指令很好）。</p>
</aside>

## Claude Code for Data Science and Visualization

Data Science and ML Engineering teams need sophisticated visualization tools to understand model performance, but building these tools often requires expertise in unfamiliar languages and frameworks. Claude Code enables these teams to build production-quality analytics dashboards without becoming full-stack developers.

### Main Claude Code use cases

**Building JavaScript/TypeScript dashboard apps**
Despite knowing "very little JavaScript and TypeScript," the team uses Claude Code to build entire React applications for visualizing RL model performance and training data. They give Claude control to write full applications from scratch, like a 5,000-line TypeScript app, without needing to understand the code themselves. This is critical because visualization apps are relatively low context and don't require understanding the entire monorepo, allowing rapid prototyping of tools to understand model performance during training and evaluations.

**Handling repetitive refactoring tasks**
When faced with merge conflicts or semi-complicated file refactoring that's too complex for editor macros but not large enough for major development effort, they use Claude Code like a "slot machine" — commit their state, let Claude work autonomously for 30 minutes, and either accept the solution or restart fresh if it doesn't work.

**Creating persistent analytics tools instead of throwaway notebooks**
Instead of building one-off Jupyter notebooks that get discarded, the team now has Claude build permanent React dashboards that can be reused across future model evaluations. This is important because understanding Claude's performance is "one of the most important things for the team" — they need to understand how models perform during training and evaluations, which "is actually non-trivial and simple tools can't get too much signal from looking at a single number go up."

**Zero-dependency task delegation**
For tasks in completely unfamiliar codebases or languages, they delegate entire implementation to Claude Code, leveraging its ability to gather context from the monorepo and execute tasks without their involvement in the actual coding process. This allows productivity in areas outside their expertise instead of spending time learning new technologies.

### Team impact

**Achieved 2-4x time savings**
Routine refactoring tasks that were tedious but manageable manually are now completed much faster.

**Built complex applications in unfamiliar languages**
Created 5,000-line TypeScript applications despite having minimal JavaScript/TypeScript experience.

**Shifted from throwaway to persistent tools**
Instead of disposable Jupyter notebooks, now building reusable React dashboards for model analysis.

**Direct model improvement insights**
Firsthand Claude Code experience informs development of better memory systems and UX improvements for future model iterations.

**Enabled visualization-driven decision making**
Better understanding of Claude's performance during training and evaluations through advanced data visualization tools.

### Top tips from the Data Science and ML Engineering teams

**Treat it like a slot machine**
Save your state before letting Claude work, let it run for 30 minutes, then either accept the result or start fresh rather than trying to wrestle with corrections. Starting over often has a higher success rate than trying to fix Claude's mistakes.

**Interrupt for simplicity when needed**
While supervising, don't hesitate to stop Claude and ask "why are you doing this? Try something simpler." The model tends toward more complex solutions by default but responds well to requests for simpler approaches.

---

<aside class="not-prose my-8 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-sm font-bold text-accent-purple tracking-wide uppercase mb-2">📌 章节导读 · 6. API 团队（API Knowledge）</h3>
<p class="text-[15px] text-accent-gray-800 leading-relaxed">负责 PDF 支持、citations、web search 等把额外知识带进 Claude context window 的功能。痛点是必须在大型复杂 codebase 上工作——总在遇到陌生模块、花大量时间收集上下文。Claude Code 成了他们的 "first stop"：先问它哪些文件相关，再开始干活。意外收益是 model dogfooding——Claude Code 自动用最新的研究模型快照，让他们提前感知模型行为变化。</p>
</aside>

## Claude Code for API

The API Knowledge team works on features like PDF support, citations, and web search that bring additional knowledge into Claude's context window. Working across large, complex codebases means constantly encountering unfamiliar code sections, spending significant time understanding which files to examine for any given task, and building context before making changes. Claude Code improves this experience by serving as a guide that can help them understand system architecture, identify relevant files, and explain complex interactions.

### Main Claude Code use cases

**First-step workflow planning**
The team uses Claude Code as their "first stop" for any task, asking it to identify which files to examine for bug fixes, feature development, or analysis. This replaces the traditional time-consuming process of manually navigating the codebase and gathering context before starting work.

**Independent debugging across codebases**
The team now has the confidence to tackle bugs in unfamiliar parts of the codebase instead of asking others for help. They can ask Claude "Do you think you can fix this bug? This is the behavior I'm seeing" and often get immediate progress, which wasn't feasible before given the time investment required.

**Model iteration testing through dogfooding**
Claude Code automatically uses the latest research model snapshots, making it their primary way of experiencing model changes. This gives them direct feedback on model behavior changes during development cycles, which they hadn't experienced during previous launches.

**Eliminating context-switching overhead**
Instead of copying code snippets and dragging files into Claude.ai while explaining problems extensively, they can ask questions directly in Claude Code without additional context gathering, significantly reducing mental overhead.

### Team impact

**Increased confidence in tackling unfamiliar areas**
Team members can independently debug bugs and investigate incidents in unfamiliar codebases.

**Significant time savings in context gathering**
Eliminated the overhead of copying code snippets and dragging files into Claude.ai, reducing mental context-switching burden.

**Faster rotation onboarding**
Engineers rotating to new teams can quickly navigate unfamiliar codebases and contribute meaningfully without extensive colleague consultation.

**Enhanced developer happiness**
Team reports feeling happier and more productive with reduced friction in daily workflows.

### Top tips from the API Knowledge team

**Treat it as an iterative partner, not a one-shot solution**
Rather than expecting Claude to solve problems immediately, approach it as a collaborator you iterate with. This works better than trying to get perfect solutions on the first try.

**Use it for building confidence in unfamiliar areas**
Don't hesitate to tackle bugs or investigate incidents outside your expertise — Claude Code makes it feasible to work independently in areas that would normally require extensive context building.

**Start with minimal information**
Begin with just the bare minimum of what you need and let Claude guide you through the process, rather than front-loading extensive explanations.

---

<aside class="not-prose my-8 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-sm font-bold text-accent-purple tracking-wide uppercase mb-2">📌 章节导读 · 7. 增长营销团队（Growth Marketing）</h3>
<p class="text-[15px] text-accent-gray-800 leading-relaxed">这是全文最具示范性的"非技术职能用 Claude Code"案例——一个人的非技术团队，覆盖 paid search/social、app store、email、SEO。他们用 Claude Code 干了传统上要"专门工程资源"才能做的事：建 agentic 工作流自动生成 Google Ads 文案（hundreds 在分钟级）、写 Figma 插件批量出广告创意（10x 创意产能）、自建 Meta Ads MCP server、做 prompt 记忆系统。文案生产 2 小时降到 15 分钟——这种压缩比让他们"像一个更大的团队在运作"。</p>
</aside>

## Claude Code for Growth Marketing

The Growth Marketing team focuses on building out performance marketing channels across paid search, paid social, mobile app stores, email marketing, and SEO. As a non-technical team of one, they use Claude Code to automate repetitive marketing tasks and create agentic workflows that would traditionally require significant engineering resources.

### Main Claude Code use cases

**Automated Google Ads creative generation**
The team built an agentic workflow that processes CSV files containing hundreds of existing ads with performance metrics, identifies underperforming ads for iteration, and generates new variations that meet strict character limits (30 characters for headlines, 90 for descriptions). Using two specialized sub-agents (one for headlines, one for descriptions), the system can generate hundreds of new ads in minutes instead of requiring manual creation across multiple campaigns. This has enabled them to test and iterate at scale, something that would have taken a significant amount of time to achieve previously.

**Figma plugin for mass creative production**
Instead of manually duplicating and editing static images for paid social ads, they developed a Figma plugin that identifies frames and programmatically generates up to 100 ad variations by swapping headlines and descriptions, reducing what would take hours of copy-pasting to half a second per batch. This enables 10x creative output, allowing the team to test vastly more creative variations across key social channels.

**Meta Ads MCP server for campaign analytics**
They created an MCP server integrated with Meta Ads API to query campaign performance, spending data, and ad effectiveness directly within the Claude Desktop app, eliminating the need to switch between platforms for performance analysis, saving critical time where every efficiency gain translates to better ROI.

**Advanced prompt engineering with memory systems**
They implemented a rudimentary memory system that logs hypotheses and experiments across ad iterations, allowing the system to pull previous test results into context when generating new variations, creating a self-improving testing framework. This enables systematic experimentation that would be impossible to track manually.

### Team impact

**Dramatic time savings on repetitive tasks**
Ad copy creation reduced from 2 hours to 15 minutes, freeing up time for strategic work.

**10x increase in creative output**
The team can now test vastly more ad variations across channels with automated generation and Figma integration.

**Operating like a larger team**
The team can handle tasks that traditionally required dedicated engineering resources.

**Strategic focus shift**
The team can spend more time on overall strategy and building agentic automation rather than manual execution.

### Top tips from the Growth Marketing team

**Identify API-enabled repetitive tasks**
Look for workflows involving repetitive actions with tools that have APIs (like ad platforms, design tools, analytics platforms). These are prime candidates for automation and where Claude Code provides the most value.

**Break complex workflows into specialized sub-agents**
Instead of trying to handle everything in one prompt or workflow, create separate agents for specific tasks (like their headline agent vs. description agent). This makes debugging easier and improves output quality when dealing with complex requirements.

**Thoroughly brainstorm and prompt plan before coding**
Spend significant time upfront using Claude.ai to think through your entire workflow, then have Claude.ai create a comprehensive prompt and code structure for Claude Code to reference. Also, work step-by-step rather than asking for one-shot solutions to avoid Claude getting overwhelmed by complex tasks.

---

<aside class="not-prose my-8 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-sm font-bold text-accent-purple tracking-wide uppercase mb-2">📌 章节导读 · 8. 产品设计团队</h3>
<p class="text-[15px] text-accent-gray-800 leading-relaxed">服务 Claude Code、Claude.ai、Anthropic API 三条产品线。最让工程师惊讶的是——他们开始做"传统设计师不该做的事"，比如直接改前端状态管理代码。日常 80% 时间 Figma 和 Claude Code 并开。一个标杆案例：GA 发布前要在全 codebase 移除 "research preview" 字样并与法务实时协调——传统要一周来回，他们用两次 30 分钟会议完成。这是"周变小时"级的协作模式变革。</p>
</aside>

## Claude Code for Product Design

The Product Design team supports Claude Code, Claude.ai and the Anthropic API, specializing in building AI products. Even non-developers can use Claude Code to bridge the traditional gap between design and engineering, enabling direct implementation of their design vision without extensive back-and-forth with engineers.

### Main Claude Code use cases

**Front-end polish and state management changes**
Instead of creating extensive design documentation and going through multiple rounds of feedback with engineers for visual tweaks (typefaces, colors, spacing), they now directly implement these changes using Claude Code. Engineers noted they're making "large state management changes that you typically wouldn't see a designer making," enabling them to achieve the exact quality they envision.

**GitHub Actions automated ticketing**
Using Claude Code's GitHub integration, they can simply file issues/tickets describing needed changes, and Claude automatically proposes code solutions without having to open Claude Code, creating a seamless bug-fixing and feature refinement workflow for their persistent backlog of polish tasks.

**Rapid interactive prototyping**
By pasting mockup images into Claude Code, they generate fully functional prototypes that engineers can immediately understand and iterate on, replacing the traditional cycle of static Figma designs that required extensive explanation and translation to working code.

**Edge case discovery and system architecture understanding**
They use Claude Code to map out error states, logic flows, and different system statuses, allowing them to identify edge cases during design rather than discovering them later in development, fundamentally improving the quality of their initial designs.

**Complex copy changes and legal compliance**
For tasks like removing "research preview" messaging across the entire codebase, they used Claude Code to find all instances, review surrounding copy, coordinate changes with legal in real-time, and implement updates — a process that took two 30-minute calls instead of a week of back-and-forth coordination.

### Team impact

**Transformed core workflow**
Claude Code becomes a primary design tool, with Figma and Claude Code open 80% of the time.

**2-3x faster execution**
Visual and state management changes that previously required extensive back-and-forth with engineers now implemented directly.

**Weeks to hours cycle time**
Complex projects like GA launch messaging that would take a week of coordination now completed in two 30-minute calls.

**Two distinct user experiences**
Developers get "augmented workflow" (faster execution), while non-technical users get "holy crap, I'm a developer workflow" (entirely new capabilities previously impossible).

**Improved design-engineering collaboration**
Better communication and faster problem-solving because designers understand system constraints and possibilities upfront.

### Top tips from the Product Design team

**Get proper setup help from engineers**
Have engineering teammates help with initial repository setup and permissions — the technical onboarding is challenging for non-developers, but once configured, it becomes transformative for daily workflow.

**Use custom memory files to guide Claude's behavior**
Create specific instructions telling Claude you're a designer with little coding experience who needs detailed explanations and smaller, incremental changes, dramatically improving the quality of Claude's responses and making it less intimidating.

**Leverage image pasting for prototyping**
Use Command+V to paste screenshots directly into Claude Code — it excels at reading designs and generating functional code, making it invaluable for turning static mockups into interactive prototypes that engineers can immediately understand and build upon.

---

<aside class="not-prose my-8 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-sm font-bold text-accent-purple tracking-wide uppercase mb-2">📌 章节导读 · 9. RL 工程团队</h3>
<p class="text-[15px] text-accent-gray-800 leading-relaxed">负责 RL 中的高效采样和跨集群权重传输。诚实度最高的一章——他们明确说 Claude Code 在 first attempt 上成功率只有 1/3，所以工作流必须搭配 checkpoint-heavy 的 try-and-rollback 范式。值得记住的具体工程实践：把"run pytest not run / don't cd unnecessarily"这种重复踩的坑写进 Claude.md，能显著降低重复犯错。"先 one-shot，不行再切换协作"是他们的成本最优解。</p>
</aside>

## Claude Code for RL Engineering

The RL Engineering team focuses on efficient sampling in RL and weight transfers across the cluster. They use Claude Code primarily for writing small to medium features, debugging, and understanding complex codebases, with an iterative approach that includes frequent checkpointing and rollbacks.

### Main Claude Code use cases

**Feature development with supervised autonomy**
The team lets Claude Code write most of the code for small to medium features while providing oversight, such as implementing authentication mechanisms for weight transfer components. They work interactively, allowing Claude to take the lead but steering it when it goes off track.

**Test generation and code review**
After implementing changes themselves, they ask Claude Code to add tests or review their code. This automated testing workflow saves significant time on routine but important quality assurance tasks.

**Debugging and error investigation**
They use Claude Code to debug errors with mixed results — sometimes it identifies issues immediately and adds relevant tests, while other times it struggles to understand the problem, but overall provides value when it works.

**Codebase comprehension and call stack analysis**
One of the biggest changes in their workflow is using Claude Code to get quick summaries of relevant components and call stacks, replacing manual code reading or extensive debugging output generation.

**Kubernetes operations guidance**
They frequently ask Claude Code about Kubernetes operations that would otherwise require extensive Googling, getting immediate answers for configuration and deployment questions.

### Development workflow impact

**Experimental approach enabled**
They now use a "try and rollback" methodology, frequently committing checkpoints so they can test Claude's autonomous implementation attempts and revert if needed, enabling more experimental.

**Documentation acceleration**
Claude Code automatically adds helpful comments that save significant time on documentation, though they note it sometimes adds comments in odd places or uses questionable code organization.

**Speed-up with limitations**
While Claude Code can implement small-to-medium PRs with "relatively little time" from them, they acknowledge it only works on first attempt about one-third of the time, requiring either additional guidance or manual intervention.

### Top tips from the RL Engineering team

**Customize your Claude.md file for specific patterns**
Add instructions to your Claude.md file to prevent Claude from making repeated tool-calling mistakes, such as telling it to "run pytest not run and don't cd unnecessarily — just use the right path." This significantly improved consistency.

**Use a checkpoint-heavy workflow**
Regularly commit your work as Claude makes changes so you can easily roll back when experiments don't work out. This enables a more experimental approach to development without risk.

**Try one-shot first, then collaborate**
Give Claude a quick prompt and let it attempt the full implementation first. If it works (about one-third of the time), you've saved significant time. If not, then switch to a more collaborative, guided approach.

---

<aside class="not-prose my-8 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-sm font-bold text-accent-purple tracking-wide uppercase mb-2">📌 章节导读 · 10. 法务团队（Legal）</h3>
<p class="text-[15px] text-accent-gray-800 leading-relaxed">最具个人色彩的一章——出发点是好奇心和"想了解 Anthropic 自家产品"。最打动人的案例是给有说话障碍的家庭成员造的辅助沟通 app（1 小时做出来）。其他用例聚焦法务的"phone tree"工单分派、G Suite 周报、跨产品法律审查追踪。他们也作为产品律师，最早识别出 deep MCP 集成的安全合规问题。两步走："Claude.ai 头脑风暴 + 出 prompt → Claude Code 一步步实施"。还有一条值得所有非技术团队听的话："克服分享 silly/toy 原型的羞耻感，正是这些演示才能让别人看到可能性"。</p>
</aside>

## Claude Code for Legal

The Legal team discovered Claude Code's potential through experimentation, and a desire to learn about Anthropic's product offerings. Additionally, one team member had a personal use case related to creating accessibility tools for family and work prototypes that demonstrate the technology's power for non-developers.

### Main Claude Code use cases

**Custom accessibility solution for family members**
Team members have built communication assistants for family members with speaking difficulties due to medical diagnoses. In just one hour, they created a predictive text app using native speech-to-text that suggests responses and speaks them using voice banks, solving gaps in existing accessibility tools recommended by speech therapists.

**Legal department workflow automation**
They created prototype "phone tree" systems to help team members connect with the right lawyer at Anthropic, demonstrating how legal departments can build custom tools for common tasks without traditional development resources.

**Team coordination tools**
Managers have built G Suite applications that automate weekly team updates and track legal review status across products, allowing lawyers to quickly flag items needing review through simple button clicks rather than spreadsheet management.

**Rapid prototyping for solution validation**
They use Claude Code to quickly build functional prototypes they can show to domain experts (like showing accessibility tools to UCSF specialists) to validate ideas and identify existing solutions before investing more time.

### Work style and impact

**Planning in Claude.ai, building in Claude Code**
They use a two-step process where they brainstorm and plan with Claude.ai first, then move to Claude Code for implementation, asking it to slow down and work step-by-step rather than outputting everything at once.

**Visual-first approach**
They frequently use screenshots to show Claude Code what they want interfaces to look like, then iterate based on visual feedback rather than describing features in text.

**Prototype-driven innovation**
They emphasize overcoming the fear of sharing "silly" or "toy" prototypes, as these demonstrations inspire others to see possibilities they hadn't considered.

### Security and compliance awareness

**MCP integration concerns**
As product lawyers, they immediately identify security implications of deep MCP integrations, noting how conservative security postures will create barriers as AI tools access more sensitive systems.

**Compliance tooling priorities**
They advocate for building compliance tools quickly as AI capabilities expand, recognizing the balance between innovation and risk management.

### Top tips from the Legal Department

**Plan extensively in Claude.ai first**
Use Claude's conversational interface to flesh out your entire idea before moving to Claude Code. Then ask Claude to summarize everything into a step-by-step prompt for implementation.

**Work incrementally and visually**
Ask Claude Code to slow down and implement one step at a time so you can copy-paste without getting overwhelmed. Use screenshots liberally to show what you want interfaces to look like.

**Share prototypes despite imperfection**
Overcome the urge to hide "toy" projects or unfinished work — sharing prototypes helps others see possibilities and sparks innovation across departments that don't typically interact.

---

## 阅读建议

这 10 个案例放在一起看，最值得 takeaway 的不是某个单点技巧，而是 Anthropic 内部呈现的"能力下放"模式——传统上要"专门工程资源"才能做的事，正在被设计师、营销、法务、数据分析师等"半技术 / 非技术"角色直接完成。

**对个人开发者**：盯三个杠杆——CLAUDE.md 的精度、自定义 slash command 的复利效应、checkpoint-heavy 工作流。这三个都是低成本起步、回报随时间累积的投入。

**对团队 leader**：从 dogfooding 的产品研发团队和 50% slash command 贡献的安全工程团队身上看模式——power user 的产生不是天赋，是"内部分享 session + 让团队互相演示工作流"的产物。增长营销团队的 sub-agent 拆分思路也值得搬到任何复杂业务流程。

**对高管 / 决策者**：注意产品设计团队那条"两种用户体验"——developer 得到 augmented workflow，非技术员工得到"holy crap I'm a developer"的全新能力。后者带来的协作模式变革（周变小时、跨职能边界扩展）才是 ROI 的真正来源，不是单纯的代码生成速度。

**对采纳路径**：Inference 团队"先做知识问答试水，再扩展到代码生成，最后到测试"的渐进信任建立法，是任何团队从 0 到 1 引入 Claude Code 的最稳妥起点。

