---
slug: agentic-design-patterns
title: "Agentic Design Patterns · 21 个 Agent 设计模式精读"
subtitle: "Google Cloud CTO 办公室 Antonio Gulli · 482 页原著中英对照 · 管理者视角提炼：模式定义 / 适用场景 / 架构取舍 · 附两本原版 PDF"
sourceUrl: "https://link.springer.com/book/10.1007/978-3-032-01402-3"
sourceLabel: "Springer（2025-10-30 正式出版）"
updated: "2026-09-20"
---

<aside class="not-prose my-8 px-6 py-6 bg-gradient-to-br from-accent-purple/10 to-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-base font-bold text-accent-purple tracking-wide uppercase mb-3">🎯 为什么值得读这本书</h3>
<ul class="space-y-2 text-[15px] text-accent-gray-800 leading-relaxed list-disc pl-5">
<li><strong>它在做 GoF《设计模式》对 Agent 工程做过的事</strong>：把散落在各家框架、各种博客里的 Agent 构建手法，收敛成 21 个有名字、有边界、有适用条件的模式。价值不在代码，在于给团队建立<strong>共同语汇</strong>——当架构师说"这里用 Reflection 而不是 Multi-Agent"，全组知道在讨论什么。</li>
<li><strong>作者身份决定了视角高度</strong>：Antonio Gulli 是 Google Cloud CTO 办公室的工程总监，30 年从业经历，书里的判断来自大规模生产系统而非 demo。前言由 Google Cloud 的 Richard Seroter 撰写。</li>
<li><strong>每章结构统一到可以横向对比</strong>：Pattern Overview（模式定义）→ Practical Applications（适用场景）→ Hands-On Code（代码，本文跳过）→ At a Glance（What / Why / <strong>Rule of thumb</strong>）→ Key Takeaways。其中 Rule of thumb 是全书最高密度的部分——一句话讲清"什么时候该用这个模式"。</li>
<li><strong>本文的取舍</strong>：作为管理者你不需要逐行跑代码。我把每个模式的<strong>定义、适用场景、架构取舍（成本 / 复杂度 / 可靠性的权衡）</strong>提炼出来，英文原文关键段落对照保留，代码实现全部剥离。</li>
<li><strong>额外加了两层原书没有的东西</strong>：① 🆕 <strong>2026 视角补充</strong>——从作者 2026 年新书《AI Design》里抽取对应的增量内容 ② 📍 <strong>2026 现状对照</strong>——书写于 2025 年，其中哪些当年的前瞻判断已经成为事实标准，哪些还没兑现。</li>
</ul>
</aside>

<aside class="not-prose my-8 px-6 py-6 bg-accent-gray-50 border border-accent-gray-200 rounded">
<h3 class="text-sm font-bold text-accent-ink tracking-wide uppercase mb-4">📎 原版 PDF 下载（两本全文，永久存档）</h3>
<div class="grid md:grid-cols-2 gap-4">
<a href="/learn/agentic-design-patterns/agentic-design-patterns-gulli-2025.pdf" target="_blank" rel="noopener" class="block px-5 py-4 bg-white border-2 border-accent-purple rounded hover:bg-accent-purple hover:text-white transition group">
<div class="text-[11px] font-semibold tracking-widest uppercase text-accent-purple group-hover:text-white mb-1">主干书 · 2025</div>
<div class="text-[15px] font-bold mb-1">Agentic Design Patterns</div>
<div class="text-[13px] text-accent-gray-600 group-hover:text-white/90">A Hands-On Guide to Building Intelligent Systems<br/>482 页 · 21 个模式 · 7.5 MB PDF</div>
</a>
<a href="/learn/agentic-design-patterns/ai-design-gulli-2026.pdf" target="_blank" rel="noopener" class="block px-5 py-4 bg-white border-2 border-accent-gray-300 rounded hover:border-accent-purple hover:bg-accent-purple hover:text-white transition group">
<div class="text-[11px] font-semibold tracking-widest uppercase text-accent-gray-500 group-hover:text-white mb-1">补充书 · 2026</div>
<div class="text-[15px] font-bold mb-1">AI Design</div>
<div class="text-[13px] text-accent-gray-600 group-hover:text-white/90">A Beginner's Guide to Building Intelligence Through Patterns<br/>398 页 · Springer 版 2026-11-16 出版 · 5.2 MB PDF</div>
</a>
</div>
<p class="text-[13px] text-accent-gray-600 mt-4 leading-relaxed">两份均为作者本人公开发布的免费完整版。2025 版由 Springer 于 2025-10-30 正式出版（ISBN 978-3-032-01401-6），2026 版的 Springer 正式版（ISBN 978-3-032-15973-1）尚未上市，目前流通的是作者公开的完整原稿。</p>
</aside>

## 读前必读：这 21 个模式怎么分组

原书分为四个 Part，但章节顺序更接近写作顺序而非认知顺序。按「解决什么层面的问题」重新归组，更适合从架构视角理解：

| 组别 | 模式 | 本质上在解决什么 |
|---|---|---|
| **A. 基础编排** | 1 Prompt Chaining · 2 Routing · 3 Parallelization · 4 Reflection · 5 Tool Use · 6 Planning · 7 Multi-Agent | 控制流问题：任务怎么拆、怎么走、怎么并行、怎么自查、怎么接外部世界 |
| **B. 认知与状态** | 8 Memory · 9 Learning & Adaptation · 10 MCP · 11 Goal Setting · 12 Exception Handling · 13 Human-in-the-Loop · 14 RAG | 状态问题：Agent 记什么、学什么、怎么接知识、出错怎么办、人在哪里介入 |
| **C. 协同与治理** | 15 A2A · 16 Resource-Aware · 17 Reasoning · 18 Guardrails · 19 Evaluation · 20 Prioritization · 21 Exploration | 系统问题：多 Agent 怎么通信、成本怎么控、怎么推理、怎么防护、怎么评估 |

> **一句话判断该不该往下读**：如果你正在或即将主导 Agent 类项目的架构评审，A 组的七个模式是评审时的最小词汇表——不掌握这七个，很难判断团队给出的方案是过度设计还是能力不足。

---

<nav class="not-prose my-8 px-6 py-6 bg-white border border-accent-gray-200 rounded" aria-label="模式导航">
<h3 class="text-sm font-bold text-accent-ink tracking-wide uppercase mb-4">🧭 快速导航 · 21 个模式直达</h3>
<div class="mb-4">
<div class="text-[12px] font-semibold tracking-widest uppercase text-accent-purple mb-2"><a href="#第一组--基础编排模式pattern-1-7" class="hover:underline">A · 基础编排（1-7）</a></div>
<div class="flex flex-wrap gap-2">
<a href="#pattern-1--prompt-chaining提示链--管道模式" class="px-3 py-1 text-[13px] bg-accent-gray-50 border border-accent-gray-200 rounded hover:border-accent-purple hover:text-accent-purple transition">1 提示链</a>
<a href="#pattern-2--routing路由--条件分流" class="px-3 py-1 text-[13px] bg-accent-gray-50 border border-accent-gray-200 rounded hover:border-accent-purple hover:text-accent-purple transition">2 路由</a>
<a href="#pattern-3--parallelization并行化" class="px-3 py-1 text-[13px] bg-accent-gray-50 border border-accent-gray-200 rounded hover:border-accent-purple hover:text-accent-purple transition">3 并行化</a>
<a href="#pattern-4--reflection反思--自我批判" class="px-3 py-1 text-[13px] bg-accent-gray-50 border border-accent-gray-200 rounded hover:border-accent-purple hover:text-accent-purple transition">4 反思</a>
<a href="#pattern-5--tool-use--function-calling工具使用--函数调用" class="px-3 py-1 text-[13px] bg-accent-gray-50 border border-accent-gray-200 rounded hover:border-accent-purple hover:text-accent-purple transition">5 工具使用</a>
<a href="#pattern-6--planning规划" class="px-3 py-1 text-[13px] bg-accent-gray-50 border border-accent-gray-200 rounded hover:border-accent-purple hover:text-accent-purple transition">6 规划</a>
<a href="#pattern-7--multi-agent-collaboration多智能体协作" class="px-3 py-1 text-[13px] bg-accent-gray-50 border border-accent-gray-200 rounded hover:border-accent-purple hover:text-accent-purple transition">7 多智能体</a>
</div>
</div>
<div class="mb-4">
<div class="text-[12px] font-semibold tracking-widest uppercase text-accent-purple mb-2"><a href="#第二组--认知与状态模式pattern-8-14" class="hover:underline">B · 认知与状态（8-14）</a></div>
<div class="flex flex-wrap gap-2">
<a href="#pattern-8--memory-management记忆管理" class="px-3 py-1 text-[13px] bg-accent-gray-50 border border-accent-gray-200 rounded hover:border-accent-purple hover:text-accent-purple transition">8 记忆管理</a>
<a href="#pattern-9--learning-and-adaptation学习与适应" class="px-3 py-1 text-[13px] bg-accent-gray-50 border border-accent-gray-200 rounded hover:border-accent-purple hover:text-accent-purple transition">9 学习适应</a>
<a href="#pattern-10--model-context-protocolmcp--模型上下文协议" class="px-3 py-1 text-[13px] bg-accent-gray-50 border border-accent-gray-200 rounded hover:border-accent-purple hover:text-accent-purple transition">10 MCP</a>
<a href="#pattern-11--goal-setting-and-monitoring目标设定与监控" class="px-3 py-1 text-[13px] bg-accent-gray-50 border border-accent-gray-200 rounded hover:border-accent-purple hover:text-accent-purple transition">11 目标监控</a>
<a href="#pattern-12--exception-handling-and-recovery异常处理与恢复" class="px-3 py-1 text-[13px] bg-accent-gray-50 border border-accent-gray-200 rounded hover:border-accent-purple hover:text-accent-purple transition">12 异常恢复</a>
<a href="#pattern-13--human-in-the-loop人在回路" class="px-3 py-1 text-[13px] bg-accent-gray-50 border border-accent-gray-200 rounded hover:border-accent-purple hover:text-accent-purple transition">13 人在回路</a>
<a href="#pattern-14--knowledge-retrieval--rag知识检索" class="px-3 py-1 text-[13px] bg-accent-gray-50 border border-accent-gray-200 rounded hover:border-accent-purple hover:text-accent-purple transition">14 RAG</a>
</div>
</div>
<div>
<div class="text-[12px] font-semibold tracking-widest uppercase text-accent-purple mb-2"><a href="#第三组--协同与治理模式pattern-15-21" class="hover:underline">C · 协同与治理（15-21）</a></div>
<div class="flex flex-wrap gap-2">
<a href="#pattern-15--inter-agent-communicationa2a--跨框架智能体通信" class="px-3 py-1 text-[13px] bg-accent-gray-50 border border-accent-gray-200 rounded hover:border-accent-purple hover:text-accent-purple transition">15 A2A 通信</a>
<a href="#pattern-16--resource-aware-optimization资源感知优化" class="px-3 py-1 text-[13px] bg-accent-gray-50 border border-accent-gray-200 rounded hover:border-accent-purple hover:text-accent-purple transition">16 资源优化</a>
<a href="#pattern-17--reasoning-techniques推理技术" class="px-3 py-1 text-[13px] bg-accent-gray-50 border border-accent-gray-200 rounded hover:border-accent-purple hover:text-accent-purple transition">17 推理技术</a>
<a href="#pattern-18--guardrails--safety-patterns护栏--安全模式" class="px-3 py-1 text-[13px] bg-accent-gray-50 border border-accent-gray-200 rounded hover:border-accent-purple hover:text-accent-purple transition">18 护栏安全</a>
<a href="#pattern-19--evaluation-and-monitoring评估与监控" class="px-3 py-1 text-[13px] bg-accent-gray-50 border border-accent-gray-200 rounded hover:border-accent-purple hover:text-accent-purple transition">19 评估监控</a>
<a href="#pattern-20--prioritization优先级排序" class="px-3 py-1 text-[13px] bg-accent-gray-50 border border-accent-gray-200 rounded hover:border-accent-purple hover:text-accent-purple transition">20 优先级</a>
<a href="#pattern-21--exploration-and-discovery探索与发现" class="px-3 py-1 text-[13px] bg-accent-gray-50 border border-accent-gray-200 rounded hover:border-accent-purple hover:text-accent-purple transition">21 探索发现</a>
</div>
</div>
</nav>

# 第一组 · 基础编排模式（Pattern 1-7）

## Pattern 1 · Prompt Chaining（提示链 / 管道模式）

<aside class="not-prose my-6 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-sm font-bold text-accent-purple tracking-wide uppercase mb-3">📌 管理者速读</h3>
<p class="text-[15px] text-accent-gray-800 leading-relaxed mb-2"><strong>解决什么问题：</strong>复杂任务塞进一个大 prompt 会让模型"认知过载"，产生四类可预测的失败——指令遗漏（instruction neglect）、上下文漂移（contextual drift）、错误放大（error propagation）、幻觉概率上升。原书给的典型例子：让模型一次完成"分析市场调研报告 + 总结发现 + 识别趋势并给数据支撑 + 起草邮件"，结果往往是总结做得不错，但数据提取和邮件起草失败。</p>
<p class="text-[15px] text-accent-gray-800 leading-relaxed mb-2"><strong>何时用：</strong>任务对单个 prompt 而言过于复杂 / 有多个明显不同的处理阶段 / 步骤之间需要调用外部工具 / 需要维持状态的多步推理。</p>
<p class="text-[15px] text-accent-gray-800 leading-relaxed"><strong>架构取舍：</strong>这是全书门槛最低、收益最直接的模式——拆步骤几乎必然提升可靠性，代价只是多几次模型调用（延迟和 token 成本线性增加）。<strong>真正的工程要点在步骤之间的数据契约</strong>：原书强调若步骤间传递的输出格式模糊，下游会因为输入损坏而失败，因此必须指定 JSON / XML 等结构化输出格式。这一点在企业落地时是最常被忽略、也最容易造成线上事故的地方。</p>
</aside>

### 模式定义 · Pattern Overview

> Prompt chaining, sometimes referred to as Pipeline pattern, represents a powerful paradigm for handling intricate tasks when leveraging large language models (LLMs). Rather than expecting an LLM to solve a complex problem in a single, monolithic step, prompt chaining advocates for a divide-and-conquer strategy. The core idea is to break down the original, daunting problem into a sequence of smaller, more manageable sub-problems. Each sub-problem is addressed individually through a specifically designed prompt, and the output generated from one prompt is strategically fed as input into the subsequent prompt in the chain.

**中文提炼**：提示链（有时也叫管道模式）的核心是分而治之——不指望 LLM 在一个庞大步骤里解决复杂问题，而是把问题拆成一串更小、更可控的子问题，每个子问题配一个专门设计的 prompt，前一步的输出作为后一步的输入。

> This sequential processing technique inherently introduces modularity and clarity into the interaction with LLMs. By decomposing a complex task, it becomes easier to understand and debug each individual step, making the overall process more robust and interpretable.

**中文提炼**：这种顺序处理天然带来模块化和清晰度。拆解之后，每一步都更容易理解和调试，整体流程因此更健壮、更可解释。**这是管理者最该记住的收益点——不是"效果更好"，而是"出问题时你知道是哪一步坏了"。**

> Furthermore, prompt chaining is not just about breaking down problems; it also enables the integration of external knowledge and tools. At each step, the LLM can be instructed to interact with external systems, APIs, or databases... This capability dramatically expands the potential of LLMs, allowing them to function not just as isolated models but as integral components of broader, more intelligent systems.

**中文提炼**：提示链不只是拆问题，它还是接入外部知识和工具的载体。每一步都可以让 LLM 与外部系统、API、数据库交互——这让 LLM 从孤立的模型变成更大智能系统中的一个组件。

### 关键工程细节 · The Role of Structured Output

> The reliability of a prompt chain is highly dependent on the integrity of the data passed between steps. If the output of one prompt is ambiguous or poorly formatted, the subsequent prompt may fail due to faulty input. To mitigate this, specifying a structured output format, such as JSON or XML, is crucial.

**中文提炼**：提示链的可靠性高度依赖步骤间传递数据的完整性。上一步输出若含糊或格式混乱，下一步会因输入有误而失败。缓解办法是强制指定 JSON / XML 等结构化输出格式。

原书还提到一个实用技巧：**给每一步分配明确的角色**。同样是上面那个市场报告的例子，第一步设为"Market Analyst"，第二步"Trade Analyst"，第三步"Expert Documentation Writer"——角色约束会进一步收窄模型在该步骤的行为空间。

### 何时使用 · Rule of Thumb（原文）

> Use this pattern when a task is too complex for a single prompt, involves multiple distinct processing stages, requires interaction with external tools between steps, or when building Agentic systems that need to perform multi-step reasoning and maintain state.

### 📍 2026 现状对照

Prompt Chaining 在 2026 年已经不太会被单独拿出来讨论了——因为它已经内化成所有主流 Agent 框架的默认结构（LangGraph 的 graph、ADK 的 SequentialAgent、各家 workflow 引擎）。它的"消失"恰恰说明它赢了。**但书里强调的结构化数据契约问题依然是线上事故高发区**：当团队把 chain 越拉越长，中间某一步的 schema 悄悄变更导致下游静默失败，是企业 Agent 项目最典型的运维痛点之一。评审时该问的问题是：每一步之间的契约是否有 schema 校验？失败时是抛错还是静默传递脏数据？

---

## Pattern 2 · Routing（路由 / 条件分流）

<aside class="not-prose my-6 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-sm font-bold text-accent-purple tracking-wide uppercase mb-3">📌 管理者速读</h3>
<p class="text-[15px] text-accent-gray-800 leading-relaxed mb-2"><strong>解决什么问题：</strong>Prompt Chaining 解决的是"确定性线性流程"，但真实系统必须根据环境状态、用户输入、上一步结果在多个可能动作之间仲裁。Routing 就是往 Agent 里引入条件逻辑——从固定执行路径变成动态选路。</p>
<p class="text-[15px] text-accent-gray-800 leading-relaxed mb-2"><strong>何时用：</strong>Agent 需要在多个不同的 workflow / 工具 / 子 Agent 之间做选择时。原书点名的典型场景是分诊类应用——客服机器人区分销售咨询、技术支持、账户管理。</p>
<p class="text-[15px] text-accent-gray-800 leading-relaxed"><strong>架构取舍：</strong>关键决策不是"要不要路由"，而是<strong>路由器用什么实现</strong>。原书给了三条路线：LLM 路由（灵活但有延迟和成本，且分类可能不稳定）、规则路由（快、可预测、零成本，但不适应新情况）、嵌入相似度路由（介于两者之间，适合语义分类）。企业场景的实践经验是：<strong>高频、意图明确的分流用规则或嵌入，低频、语义复杂的兜底交给 LLM</strong>——不要所有分流都上 LLM，那是在用最贵的方式解决最简单的问题。</p>
</aside>

### 模式定义 · Pattern Overview

> While sequential processing via prompt chaining is a foundational technique for executing deterministic, linear workflows with language models, its applicability is limited in scenarios requiring adaptive responses. Real-world agentic systems must often arbitrate between multiple potential actions based on contingent factors, such as the state of the environment, user input, or the outcome of a preceding operation. This capacity for dynamic decision-making, which governs the flow of control to different specialized functions, tools, or sub-processes, is achieved through a mechanism known as routing.

**中文提炼**：提示链擅长确定性的线性流程，但面对需要自适应响应的场景就力不从心。真实的 Agent 系统必须基于环境状态、用户输入或前一步结果，在多个潜在动作之间做仲裁。这种把控制流导向不同专门函数、工具或子流程的动态决策能力，就是路由。

> Routing introduces conditional logic into an agent's operational framework, enabling a shift from a fixed execution path to a model where the agent dynamically evaluates specific criteria to select from a set of possible subsequent actions.

**中文提炼**：路由把条件逻辑引入 Agent 的运行框架，使其从固定执行路径转变为——动态评估特定标准，从一组可能的后续动作中做选择。

### 三种路由实现 · Routing Mechanisms

原书列出的实现路径（管理者需要知道的是它们的成本 / 能力曲线不同）：

> **LLM-based Routing**: The language model itself can be prompted to analyze the input and output a specific identifier or instruction that indicates the next step or destination.

**① LLM 路由**：直接让模型分析输入并输出类别标识（如"只输出以下类别之一：Order Status / Product Info / Technical Support / Other"）。最灵活，能处理模糊语义，但每次路由都是一次模型调用——延迟、成本、以及分类本身的不确定性都要计入。

**② 规则路由**：基于关键词、正则、预定义条件的传统条件判断。快、便宜、完全可预测，代价是无法应对没枚举到的情况。

**③ 嵌入相似度路由**：把输入向量化后与各路由目标的向量比对，取最相近者。适合语义分类且比 LLM 便宜，但需要维护 embedding 索引。

### 何时使用 · Rule of Thumb（原文）

> Use the Routing pattern when an agent must decide between multiple distinct workflows, tools, or sub-agents based on the user's input or the current state. It is essential for applications that need to triage or classify incoming requests to handle different types of tasks, such as a customer support bot distinguishing between sales inquiries, technical support, and account management questions.

### 📍 2026 现状对照

Routing 在 2026 年演化出了书里没有展开的一个重要变体：**模型路由（model routing）**——不是在业务分支之间选，而是在不同能力 / 价格档位的模型之间选（简单请求走小模型，复杂请求升级到旗舰模型）。这已经成为企业控成本的标准手段，OpenRouter、各家网关产品都把它做成了基础设施。**如果你的团队在做 Agent 平台，这一层应该在平台侧统一实现，而不是让每个业务 Agent 自己写**——这是本书成书时还不明显、现在已经很清楚的架构分层。

---

## Pattern 3 · Parallelization（并行化）

<aside class="not-prose my-6 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-sm font-bold text-accent-purple tracking-wide uppercase mb-3">📌 管理者速读</h3>
<p class="text-[15px] text-accent-gray-800 leading-relaxed mb-2"><strong>解决什么问题：</strong>纯顺序执行时总耗时 = 所有子任务耗时之和。当子任务大量依赖外部 I/O（调 API、查库）时，这个累加会变成严重瓶颈。并行化让相互独立的子任务同时跑。</p>
<p class="text-[15px] text-accent-gray-800 leading-relaxed mb-2"><strong>何时用：</strong>workflow 中存在多个互不依赖的操作——从多个 API 取数、处理不同数据块、生成多份内容后再综合。</p>
<p class="text-[15px] text-accent-gray-800 leading-relaxed"><strong>架构取舍（本章最该记住的一句）：</strong>原书在 Key Takeaways 里罕见地给出了明确的负面警告——<em>"The adoption of a concurrent or parallel architecture introduces substantial complexity and cost, impacting key development phases such as design, debugging, and system logging."</em> 并行不是免费午餐：设计、调试、日志三个环节的复杂度都会显著上升。分布式系统里所有关于并发的老问题（竞态、部分失败、日志交错难追踪）在 Agent 里一个都不会少，而且因为 LLM 调用本身有不确定性，复现问题更难。<strong>建议的判据：只有当延迟是真实的产品瓶颈、且并行收益能量化时才上；为了"看起来更先进"而并行是负收益。</strong></p>
</aside>

### 模式定义 · Pattern Overview

> Parallelization involves executing multiple components, such as LLM calls, tool usages, or even entire sub-agents, concurrently. Instead of waiting for one step to complete before starting the next, parallel execution allows independent tasks to run at the same time, significantly reducing the overall execution time for tasks that can be broken down into independent parts.

**中文提炼**：并行化指同时执行多个组件——LLM 调用、工具使用，甚至整个子 Agent。不必等一步完成再启动下一步，独立任务同时运行，对可拆分为独立部分的任务能大幅缩短总执行时间。

> The core idea is to identify parts of the workflow that do not depend on the output of other parts and execute them in parallel. This is particularly effective when dealing with external services (like APIs or databases) that have latency, as you can issue multiple requests concurrently.

**中文提炼**：核心是识别出 workflow 中不依赖其他部分输出的环节并让它们并行。当涉及有延迟的外部服务（API、数据库）时尤其有效——可以并发发出多个请求。

原书给的对照例子很直观：研究并总结某个主题，顺序做法是「搜索源 A → 总结 A → 搜索源 B → 总结 B → 综合」；并行做法是「A、B 同时搜索 → A、B 同时总结 → 综合」。**注意最后的综合步骤天然是顺序的**——这是并行模式的固有结构：扇出（fan-out）之后必有扇入（fan-in）。

### 何时使用 · Rule of Thumb（原文）

> Use this pattern when a workflow contains multiple independent operations that can run simultaneously, such as fetching data from several APIs, processing different chunks of data, or generating multiple pieces of content for later synthesis.

### 📍 2026 现状对照

并行化在 2026 年最主流的落地形态，是 Anthropic、OpenAI 等厂商反复强调的 **subagent 并行研究模式**——主 Agent 扇出多个子 Agent 各自独立检索/分析，再由主 Agent 综合。这恰好是书里 Parallelization + Multi-Agent 两个模式的叠加。同时，书里的成本警告在这个形态下被放大了：并行 N 个子 Agent 意味着 token 消耗接近 N 倍，**在企业场景中这是最容易失控的成本项**。评审并行方案时该问：并发上限是多少？有没有熔断？单次任务的 token 预算上限在哪？

---

## Pattern 4 · Reflection（反思 / 自我批判）

<aside class="not-prose my-6 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-sm font-bold text-accent-purple tracking-wide uppercase mb-3">📌 管理者速读</h3>
<p class="text-[15px] text-accent-gray-800 leading-relaxed mb-2"><strong>解决什么问题：</strong>前三个模式让流程更高效更灵活，但 Agent 的初次输出未必最优、准确或完整。Reflection 引入反馈回路——让 Agent 评估自己的产出并据此改进。</p>
<p class="text-[15px] text-accent-gray-800 leading-relaxed mb-2"><strong>何时用：</strong>对输出质量、准确性、细腻程度要求高的任务。<strong>最有价值的实现是 Producer-Critic（生产者-批评者）分离</strong>：用独立的第二个 Agent（或明确不同系统提示的第二次调用）来批判第一个 Agent 的产出，而不是让同一个 Agent 自我反思——原书明确指出职责分离能提升客观性并产出更结构化的反馈。</p>
<p class="text-[15px] text-accent-gray-800 leading-relaxed"><strong>架构取舍：</strong>原书给的代价清单非常具体——<em>增加延迟、增加计算开销、更高的上下文窗口溢出风险、更容易被 API 限流</em>。反思本质是用成倍的调用次数换质量。<strong>实践判据：质量缺陷的业务代价 &gt; 多轮调用的成本时才值得。</strong>对内部草稿类任务通常不值，对对外交付物、代码合并、合规文本则往往值得。另外要注意"反思次数"必须设上限——无限自我批判会陷入无收敛的打磨循环。</p>
</aside>

### 模式定义 · Pattern Overview

> The Reflection pattern involves an agent evaluating its own work, output, or internal state and using that evaluation to improve its performance or refine its response. It's a form of self-correction or self-improvement, allowing the agent to iteratively refine its output or adjust its approach based on feedback, internal critique, or comparison against desired criteria. Reflection can occasionally be facilitated by a separate agent whose specific role is to analyze the output of an initial agent.

**中文提炼**：反思模式指 Agent 评估自身的工作、输出或内部状态，并用该评估改进表现或优化响应。这是一种自我纠错 / 自我提升机制，让 Agent 基于反馈、内部批判或与既定标准的比对，迭代地打磨输出或调整方法。反思也可以由一个专门分析初始 Agent 输出的独立 Agent 来完成。

> Unlike a simple sequential chain where output is passed directly to the next step, or routing which chooses a path, reflection introduces a feedback loop.

**中文提炼**：与顺序链（输出直接传给下一步）和路由（选择路径）不同，反思引入的是**反馈回路**——这是它在控制流上的本质区别。

### 四步循环 · The Process

> 1. **Execution**: The agent performs a task or generates an initial output.
> 2. **Evaluation/Critique**: The agent (often using another LLM call or a set of rules) analyzes the result from the previous step. This evaluation might check for factual accuracy, coherence, style, completeness, adherence to instructions, or other relevant criteria.
> 3. **Reflection/Refinement**: Based on the critique, the agent determines how to improve...
> 4. **Iteration (Optional but common)**: The refined output or adjusted approach can then be executed, and the reflection process can repeat until a satisfactory result is achieved or a stopping condition is met.

**中文提炼**：① 执行——产出初始结果 ② 评估/批判——用另一次 LLM 调用或规则集分析上一步结果，检查事实准确性、连贯性、风格、完整性、指令遵循度 ③ 反思/优化——基于批判决定如何改进 ④ 迭代（可选但常见）——重复该过程直到满意或触发停止条件。**第 4 步的"停止条件"在工程上必须显式设计，否则就是死循环。**

### Producer-Critic 模型

> A key and highly effective implementation of the Reflection pattern separates the process into two distinct logical roles: a Producer and a Critic. This is often called the "Generator-Critic" or "Producer-Reviewer" model. While a single agent can perform self-reflection, using two specialized agents (or two separate LLM calls with distinct system prompts)...

**中文提炼**：反思模式最有效的实现方式，是把过程拆成两个独立逻辑角色——生产者与批评者（也叫"生成器-批评者"或"生产者-评审者"模型）。单个 Agent 虽然也能自我反思，但用两个专门化的 Agent（或两次带不同系统提示的独立调用）效果更好。

> **Key Takeaway 原文**：A powerful implementation is the Producer-Critic model, where a separate agent (or prompted role) evaluates the initial output. This separation of concerns enhances objectivity and allows for more specialized, structured feedback.
>
> However, these benefits come at the cost of increased latency and computational expense, along with a higher risk of exceeding the model's context window or being throttled by API services.

### 📍 2026 现状对照

这是 2026 年落地最广、也最被低估的一个模式。多 Agent 系统里的「QC Agent」「Reviewer Agent」本质都是 Producer-Critic 的工程化。一个书里没写、但实践中非常关键的经验：**批评者应该使用与生产者不同的模型**——同模型自我批判会系统性地遗漏同类盲点（相同训练偏差导致相同误判），换模型能显著提升发现率。如果团队在做质量门禁类 Agent，这是一条值得直接写进架构规范的经验。

---

## Pattern 5 · Tool Use / Function Calling（工具使用 / 函数调用）

<aside class="not-prose my-6 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-sm font-bold text-accent-purple tracking-wide uppercase mb-3">📌 管理者速读</h3>
<p class="text-[15px] text-accent-gray-800 leading-relaxed mb-2"><strong>解决什么问题：</strong>LLM 的知识是静态的、截止于训练数据的，且本身无法执行动作或获取实时信息。Tool Use 是让模型突破这道墙的唯一机制——没有它，LLM 对真实业务问题的价值严重受限。</p>
<p class="text-[15px] text-accent-gray-800 leading-relaxed mb-2"><strong>何时用：</strong>凡是需要跳出模型内部知识、与外部世界交互的场景——实时数据（天气、股价）、私有数据（查企业数据库）、精确计算、执行代码、触发真实动作（发邮件、控制设备）。</p>
<p class="text-[15px] text-accent-gray-800 leading-relaxed"><strong>架构取舍：</strong>这个模式本身没有"要不要用"的问题（不用就没有 Agent），真正的取舍在<strong>工具的粒度与数量</strong>。工具定义即 prompt 的一部分——工具越多，模型选错的概率越高、上下文占用越大。业界经验是单个 Agent 的工具数超过十几个后选择准确率开始明显下降，此时应该考虑的是拆分 Agent（Pattern 7）或引入路由（Pattern 2），而不是继续堆工具。另一个管理者必须关注的维度是<strong>权限与风险分级</strong>：读类工具和写类工具（尤其是不可逆操作）必须分开治理，这一点在 Pattern 13 Human-in-the-Loop 里会展开。</p>
</aside>

### 模式定义 · Pattern Overview

> The Tool Use pattern, often implemented through a mechanism called Function Calling, enables an agent to interact with external APIs, databases, services, or even execute code. It allows the LLM at the core of the agent to decide when and how to use a specific external function based on the user's request or the current state of the task.

**中文提炼**：工具使用模式（通常通过函数调用机制实现）让 Agent 能与外部 API、数据库、服务交互，甚至执行代码。它让 Agent 核心的 LLM 自行判断——基于用户请求或任务当前状态，**何时**以及**如何**使用某个外部函数。

### 六步流程 · The Process

> 1. **Tool Definition**: External functions or capabilities are defined and described to the LLM. This description includes the function's purpose, its name, and the parameters it accepts, along with their types and descriptions.
> 2. **LLM Decision**: The LLM receives the user's request and the available tool definitions. Based on its understanding of the request and the tools, the LLM decides if calling one or more tools is necessary.
> 3. **Function Call Generation**: If the LLM decides to use a tool, it generates a structured output (often a JSON object) that specifies the name of the tool to call and the arguments to pass to it.
> 4. **Tool Execution**: The agentic framework or orchestration layer intercepts this structured output... and executes the actual external function with the provided arguments.
> 5. **Observation/Result**: The output or result from the tool execution is returned to the agent.
> 6. **LLM Processing (Optional but common)**: The LLM receives the tool's output as context and uses it to formulate a final response.

**中文提炼**：① **工具定义**——把外部函数的用途、名称、参数及其类型与说明描述给 LLM ② **LLM 决策**——模型基于请求与工具定义判断是否需要调用 ③ **生成调用**——输出结构化对象（通常是 JSON），指明调用哪个工具、传什么参数 ④ **工具执行**——编排层拦截该输出并真正执行函数 ⑤ **观察结果**——执行结果返回给 Agent ⑥ **LLM 处理**——模型把结果作为上下文，形成最终响应或决定下一步。

**管理者视角的关键认知**：第 ①③ 步是模型侧，第 ④ 步是你的系统侧。**模型只是"请求"调用某个函数，真正执行的是你的编排层**——所有的权限校验、参数白名单、风险拦截都应该发生在第 ④ 步，而不是指望模型自觉。这是 Agent 安全架构的基本盘。

> This pattern is fundamental because it breaks the limitations of the LLM's training data and allows it to access up-to-date information, perform calculations it can't do internally, interact with user-specific data, or trigger real-world actions. Function calling is the technical mechanism that bridges the gap between the LLM's reasoning capabilities and the vast array of external functionalities available.

**中文提炼**：这个模式之所以是根本性的，因为它打破了 LLM 训练数据的限制——获取最新信息、执行模型内部做不了的计算、访问用户特定数据、触发真实世界动作。函数调用是连接 LLM 推理能力与海量外部功能的技术桥梁。

### 何时使用 · Rule of Thumb（原文）

> Use the Tool Use pattern whenever an agent needs to break out of the LLM's internal knowledge and interact with the outside world. This is essential for tasks requiring real-time data (e.g., checking weather, stock prices), accessing private or proprietary information (e.g., querying a company's database), performing precise calculations, executing code, or triggering actions in other systems (e.g., sending an email, controlling smart devices).

### 📍 2026 现状对照

Tool Use 在 2026 年的最大变化，是**工具的供给方式从"每个 Agent 自己写"转向"标准协议接入"**——也就是 MCP（Pattern 10 会详述）。这个转变对企业的意义是：工具从散落在各个 Agent 代码库里的函数，变成可以集中治理、统一鉴权、统一审计的服务目录。如果你的组织有多个团队在做 Agent，**工具层应该被当作平台资产而非项目资产来管理**——这是 2025 年写书时尚在萌芽、2026 年已经是主流判断的架构决策。

---

## Pattern 6 · Planning（规划）

<aside class="not-prose my-6 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-sm font-bold text-accent-purple tracking-wide uppercase mb-3">📌 管理者速读</h3>
<p class="text-[15px] text-accent-gray-800 leading-relaxed mb-2"><strong>解决什么问题：</strong>智能行为不只是对输入做反应，还需要前瞻性——把复杂任务拆成可管理的步骤，并策划如何达成目标。Planning 就是 Agent 从初始状态走向目标状态的动作序列生成能力。</p>
<p class="text-[15px] text-accent-gray-800 leading-relaxed mb-2"><strong>何时用：</strong>用户请求复杂到无法用单个动作或工具完成时——生成详细研究报告、新员工入职流程、竞品分析这类需要一串相互依赖操作的任务。</p>
<p class="text-[15px] text-accent-gray-800 leading-relaxed"><strong>架构取舍（全书最锋利的一段判断）：</strong>原书在这一章给出了一条我认为应该贴在所有 Agent 项目评审室墙上的判据——<strong>"决定用规划型 Agent 还是简单执行型 Agent，取决于一个问题：<em>how</em> 需要被发现，还是已经是已知的？"</strong> 如果解法已知且可重复，把 Agent 约束在预定的固定 workflow 里更有效——这是在牺牲自主性换取确定性。动态规划是一种特定工具，不是万能解。<strong>这条判据直接对应了 Anthropic "workflow first, agent only when needed" 的原则，但表述得更可操作。</strong></p>
</aside>

### 模式定义 · Pattern Overview

> In the context of AI, it's helpful to think of a planning agent as a specialist to whom you delegate a complex goal. When you ask it to "organize a team offsite," you are defining the **what**—the objective and its constraints—but not the **how**. The agent's core task is to autonomously chart a course to that goal. It must first understand the initial state (e.g., budget, number of participants, desired dates) and the goal state (a successfully booked offsite), and then discover the optimal sequence of actions to connect them. The plan is not known in advance; it is created in response to the request.

**中文提炼**：可以把规划型 Agent 理解为一个你委派复杂目标的专家。当你要求它"组织一次团队 offsite"时，你定义的是 **what**（目标与约束），而非 **how**。Agent 的核心任务是自主地规划出通往目标的路径——先理解初始状态（预算、人数、期望日期）与目标状态（成功预订的 offsite），再找出连接两者的最优动作序列。**计划不是事先已知的，而是针对请求现场生成的。**

> A hallmark of this process is adaptability. An initial plan is merely a starting point, not a rigid script. The agent's real power is its ability to incorporate new information and steer the project around obstacles. For instance, if the preferred venue becomes unavailable or a chosen caterer is fully booked, a capable agent doesn't simply fail. It adapts.

**中文提炼**：这个过程的标志是**适应性**。初始计划只是起点，不是僵硬的剧本。Agent 的真正威力在于吸收新信息并绕过障碍——首选场地不可用、选定的餐饮商约满了，有能力的 Agent 不会直接失败，而是记录新约束、重新评估选项、形成新计划。

### 核心取舍 · Flexibility vs Predictability（本章最重要的一段）

> However, it is crucial to recognize the trade-off between flexibility and predictability. Dynamic planning is a specific tool, not a universal solution. When a problem's solution is already well-understood and repeatable, constraining the agent to a predetermined, fixed workflow is more effective. This approach limits the agent's autonomy to reduce uncertainty and the risk of unpredictable behavior, guaranteeing a reliable and consistent outcome. Therefore, the decision to use a planning agent versus a simple task-execution agent hinges on a single question: **does the "how" need to be discovered, or is it already known?**

**中文提炼**：必须认清灵活性与可预测性之间的权衡。动态规划是特定工具，不是普适方案。当问题的解法已经充分理解且可重复时，**把 Agent 约束在预定的固定 workflow 里反而更有效**——这样做限制了 Agent 的自主性，以降低不确定性和不可预测行为的风险，换取可靠一致的结果。因此，用规划型 Agent 还是简单任务执行型 Agent，取决于一个问题：**"怎么做"需要被发现，还是已经是已知的？**

### 何时使用 · Rule of Thumb（原文）

> Use this pattern when a user's request is too complex to be handled by a single action or tool. It is ideal for automating multi-step processes, such as generating a detailed research report, onboarding a new employee, or executing a competitive analysis. Apply the Planning pattern whenever a task requires a sequence of interdependent operations to reach a final, synthesized outcome.

### 🆕 2026 视角补充 · Deep Research 作为规划的产品化

原书在本章 Key Takeaways 里提到 <em>"Google Deep Research is an agent analyzing on our behalf sources obtained using Google Search"</em>，而 2026 年的《AI Design》专门用 Appendix L 展开了 Google Deep Research 的机制。这是 Planning 模式最成熟的消费级产品化形态：用户给出研究目标（what），系统自主生成检索计划、执行多轮搜索、按需调整方向（how 由系统发现）。

对企业的启发是：**Deep Research 类产品验证了"规划 + 并行检索 + 综合"这条链路在通用场景已经可用**，接下来的差异化不在编排本身，而在于能接入什么专有数据源——这恰好是企业相对通用产品的结构性优势所在。

### 📍 2026 现状对照

2026 年 Planning 领域最明显的变化是**显式规划（写出计划文件再执行）成为主流实践**。Anthropic 的 AI-Native SDLC Playbook 里的 `intent.md → spec.md → plan.md` artifact 链、各家 coding agent 的 plan mode，都是把书里的"内部规划"外化成人类可审阅的中间产物。这个变化的意义远超技术本身：**计划一旦可见，人类就获得了在执行前介入的机会**——这是企业采纳 Agent 的关键信任机制，比事后审计有效得多。

---

## Pattern 7 · Multi-Agent Collaboration（多智能体协作）

<aside class="not-prose my-6 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-sm font-bold text-accent-purple tracking-wide uppercase mb-3">📌 管理者速读</h3>
<p class="text-[15px] text-accent-gray-800 leading-relaxed mb-2"><strong>解决什么问题：</strong>单体 Agent 架构在定义明确的问题上有效，但面对跨领域的复杂任务时能力受限——单个 Agent 可能不具备所需的全部专门技能或工具访问权。多 Agent 通过任务分解 + 专业化分工破这个局。</p>
<p class="text-[15px] text-accent-gray-800 leading-relaxed mb-2"><strong>何时用：</strong>任务对单 Agent 过于复杂，且能分解成需要不同专门技能或工具的子任务。典型场景：复杂研究分析、软件开发、创意内容生成。</p>
<p class="text-[15px] text-accent-gray-800 leading-relaxed"><strong>架构取舍：</strong>原书明确指出系统成效<strong>"不仅来自分工，更关键地取决于 Agent 间的通信机制"</strong>——需要标准化通信协议和共享本体（shared ontology）。这句话是多 Agent 项目失败的主要根源：大多数团队把精力放在"设计几个角色"上，却没有认真设计 Agent 之间传什么、怎么传、传错了怎么办。原书列出的六种拓扑各有明确代价，其中 Supervisor 模式的警告最值得记住：<strong>它引入单点故障，且当下属过多或任务过于复杂时，Supervisor 本身会成为瓶颈</strong>。</p>
</aside>

### 模式定义 · Pattern Overview

> The Multi-Agent Collaboration pattern addresses these limitations by structuring a system as a cooperative ensemble of distinct, specialized agents. This approach is predicated on the principle of task decomposition, where a high-level objective is broken down into discrete sub-problems. Each sub-problem is then assigned to an agent possessing the specific tools, data access, or reasoning capabilities best suited for that task.

**中文提炼**：多智能体协作模式把系统构造成一组独立、专门化 Agent 的协作集合。其前提是任务分解——高层目标被拆成离散子问题，每个子问题分配给拥有最适合该任务的工具、数据访问权或推理能力的 Agent。

> The efficacy of such a system is not merely due to the division of labor but is **critically dependent on the mechanisms for inter-agent communication**. This requires a standardized communication protocol and a shared ontology, allowing agents to exchange data, delegate sub-tasks, and coordinate their actions to ensure the final output is coherent.

**中文提炼**：这类系统的成效不仅来自分工，更**关键地取决于 Agent 间的通信机制**——需要标准化的通信协议和共享本体，使 Agent 能交换数据、委派子任务、协调行动，从而保证最终输出的连贯性。

> This distributed architecture offers several advantages, including enhanced modularity, scalability, and robustness, as the failure of a single agent does not necessarily cause a total system failure.

**中文提炼**：这种分布式架构带来模块化、可扩展性和健壮性——单个 Agent 失败不必然导致整个系统失败。

### 六种协作拓扑 · Interaction Models（原书 Fig.2 展开）

原书系统列出了从单 Agent 到完全自定义的六种拓扑，每种都标注了优势与代价。这份清单是评审多 Agent 方案时的对照表：

| 拓扑 | 原书描述 | 代价 / 风险 |
|---|---|---|
| **1. Single Agent** | 自主运行，无与其他实体的直接交互。实现和管理最简单 | 能力被单个 Agent 的范围和资源天然限制 |
| **2. Network（网络 / 对等）** | 多 Agent 去中心化直接交互，点对点通信，共享信息、资源甚至任务。韧性好——单个 Agent 失败不致瘫痪全系统 | 通信开销管理困难；大规模无结构网络中难以保证决策连贯 |
| **3. Supervisor（监督者）** | 专门的 supervisor 统筹协调下属 Agent，作为通信、任务分配、冲突解决的中心枢纽。层级清晰，简化管理与控制 | **引入单点故障**；下属过多或任务复杂时 supervisor 成为瓶颈 |
| **4. Supervisor as a Tool（监督者即工具）** | Supervisor 角色从指挥控制转向提供资源、指导和分析支持 | 弱化中心控制，协调一致性依赖下层自觉 |
| **5. Hierarchical（层级）** | 多层 supervisor，高层监督低层，最底层是操作型 Agent。适合可分解为子问题的复杂问题，在明确边界内实现分布式决策 | 层级深度带来延迟累积与调试复杂度 |
| **6. Custom（自定义）** | 完全按具体问题需求定制关系与通信结构，可混合多种模式 | 灵活性最高，可复用性与可维护性最低 |

### 协作的具体形式 · Collaboration Forms

> - **Sequential Handoffs**: One agent completes a task and passes its output to another agent for the next step in a pipeline (similar to the Planning pattern, but explicitly involving different agents).
> - **Parallel Processing**: Multiple agents work on different parts of a problem simultaneously, and their results are later combined.
> - **Debate and Consensus**: Multi-Agent Collaboration where Agents with varied perspectives and information sources engage in discussions to evaluate options, ultimately reaching a consensus or a more informed decision.
> - **Hierarchical Structures**: A manager agent might delegate tasks to worker agents dynamically based on their tool access or plugin capabilities and synthesize their results.

**中文提炼**：① **顺序移交**——一个 Agent 完成任务后把输出交给流水线下一环（类似规划模式，但显式涉及不同 Agent）② **并行处理**——多 Agent 同时处理问题的不同部分，结果后续合并 ③ **辩论与共识**——持不同视角和信息源的 Agent 通过讨论评估选项，最终达成共识或形成更有依据的决策 ④ **层级结构**——管理者 Agent 基于工具访问权或插件能力动态委派任务给工作 Agent，并综合其结果。

### 何时使用 · Rule of Thumb（原文）

> Use this pattern when a task is too complex for a single agent and can be decomposed into distinct sub-tasks requiring specialized skills or tools. It is ideal for problems that benefit from diverse expertise, parallel processing, or a structured workflow with multiple stages, such as complex research and analysis, software development, or creative content generation.

### 📍 2026 现状对照

多 Agent 是 2025-2026 年被过度营销最严重的模式，也是企业踩坑最多的地方。几条来自实践的补充判断：

- **先榨干单 Agent 再拆**。OpenAI 在其官方 Agent 指南里给出的拆分信号很明确：只有当 prompt 里 if-else 分支泛滥、或工具多到彼此混淆时才拆分。为"架构美观"而拆是负收益——每增加一个 Agent，就增加一组通信失败面和一份 token 成本。
- **通信协议这一层在 2026 年有了标准答案**：A2A（Agent-to-Agent，Pattern 15 详述）。书写作时它还是新提案，现在已是这个领域的主流协议方向。
- **辩论/共识模式的成本极高且收益不稳定**。在企业场景中，比起让 N 个 Agent 辩论，用 Producer-Critic（Pattern 4）做单轮交叉验证的性价比通常高得多。
- **Supervisor 单点问题在生产中真实存在**。当中心 Agent 负责所有调度时，它的上下文会随任务复杂度线性膨胀，最终成为整个系统的上下文瓶颈——这是书里的警告在 LLM 语境下的特殊表现形式。

---

<aside class="not-prose my-10 px-6 py-6 bg-accent-ink text-white rounded">
<h3 class="text-base font-bold tracking-wide uppercase mb-3">📋 第一组小结 · 七个模式的决策关系</h3>
<p class="text-[15px] leading-relaxed mb-3 text-accent-gray-200">这七个基础编排模式不是并列的选项清单，而是有依赖关系的决策序列。实际做架构评审时的判断顺序建议是：</p>
<ol class="space-y-2 text-[15px] leading-relaxed list-decimal pl-5 text-accent-gray-100">
<li><strong>先问"how 是否已知"（Pattern 6 的判据）</strong>——已知就用固定 workflow，别上规划型 Agent。这一问能砍掉大量过度设计。</li>
<li><strong>流程确定后，能拆就拆（Pattern 1）</strong>——单 prompt 干复杂事是最常见的可靠性问题来源。拆完记得定义步骤间的结构化契约。</li>
<li><strong>需要分支就加路由（Pattern 2）</strong>——但优先用规则/嵌入，别默认上 LLM 路由。</li>
<li><strong>延迟是真瓶颈才并行（Pattern 3）</strong>——原书明确警告并行显著抬高设计、调试、日志三方面的复杂度。</li>
<li><strong>质量代价高于调用成本时才反思（Pattern 4）</strong>——用 Producer-Critic 分离，且必须设迭代上限。</li>
<li><strong>接外部世界靠工具（Pattern 5）</strong>——记住执行发生在你的编排层，权限校验放在那里，不要指望模型自觉。</li>
<li><strong>最后才考虑拆多 Agent（Pattern 7）</strong>——先榨干单 Agent；拆了之后，通信协议的设计比角色划分更决定成败。</li>
</ol>
</aside>

---

# 第二组 · 认知与状态模式（Pattern 8-14）

## Pattern 8 · Memory Management（记忆管理）

<aside class="not-prose my-6 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-sm font-bold text-accent-purple tracking-wide uppercase mb-3">📌 管理者速读</h3>
<p class="text-[15px] text-accent-gray-800 leading-relaxed mb-2"><strong>解决什么问题：</strong>没有记忆机制的 Agent 是无状态的——每次交互都从零开始，无法维持对话上下文、无法从经验中学习、无法个性化。原书把 Agent 记忆分成两层：短期记忆（本质就是 LLM 的上下文窗口，会话结束即失）与长期记忆（外部持久存储，通常是向量库 / 知识图谱 / 数据库，靠语义检索取回）。</p>
<p class="text-[15px] text-accent-gray-800 leading-relaxed mb-2"><strong>何时用：</strong>凡是 Agent 需要做的事超出"回答一个孤立问题"——跨轮对话保持上下文、多步任务追踪进度、按用户偏好个性化、从过往成败中学习——就必须显式设计记忆管理。</p>
<p class="text-[15px] text-accent-gray-800 leading-relaxed"><strong>架构取舍：</strong>本章最容易被误读的一点是"长上下文模型让记忆管理过时了"。原书明确反驳：长上下文只是把短期记忆的容器撑大了，<strong>它依然是会话级、临时的，且每次全量处理既贵又低效</strong>。真正的架构决策在三个层面：① 短期记忆放什么（上下文窗口是稀缺资源，要靠摘要压缩、要点强调来管理）② 长期记忆存什么、怎么组织（原书借 LangGraph 给出了语义 / 情景 / 程序性三分法，比"一个向量库存所有"精细得多）③ 状态更新走什么通道（ADK 明确警告：绕过事件机制直接改 state 会导致不可追溯、并发问题、持久化失效——这本质是在说记忆写入必须走受控通道，与业务系统"禁止直接改库"是同一条治理逻辑）。</p>
</aside>

### 模式定义 · Pattern Overview

> In agent systems, memory refers to an agent's ability to retain and utilize information from past interactions, observations, and learning experiences. This capability allows agents to make informed decisions, maintain conversational context, and improve over time.

**中文提炼**：Agent 系统中的记忆，指 Agent 保留并利用来自过往交互、观察与学习经验的信息的能力。它支撑三件事：做出更有依据的决策、维持对话上下文、随时间持续改进。

短期记忆的本质与边界，原书说得很直白：

> However, this context is still ephemeral and is lost once the session concludes, and it can be costly and inefficient to process every time. Consequently, agents require separate memory types to achieve true persistence, recall information from past interactions, and build a lasting knowledge base.

**中文提炼**：即便有了长上下文窗口，这份上下文依然是短暂的——会话一结束就丢失，而且每次全量处理成本高、效率低。因此 Agent 需要独立的记忆类型来实现真正的持久化、跨交互召回和长期知识库积累。**这句话是对"上下文窗口越来越大，还要什么记忆系统"这类论调的直接回应——窗口再大也只是更大的草稿纸，不是档案柜。**

长期记忆的主流实现是向量化 + 语义检索：

> In vector databases, information is converted into numerical vectors and stored, enabling agents to retrieve data based on semantic similarity rather than exact keyword matches, a process known as semantic search.

**中文提炼**：向量数据库把信息转成数值向量存储，让 Agent 能按语义相似度而非关键词精确匹配来检索——即语义搜索。取回的内容被注入短期上下文中使用，实现"既有知识 + 当前交互"的结合。

### 长期记忆的三种类型（LangGraph 视角）

原书借 LangChain / LangGraph 的框架，把长期记忆按人类记忆类比拆成三类——这个三分法对架构设计的价值远超工具本身：

> Semantic Memory: Remembering Facts: This involves retaining specific facts and concepts, such as user preferences or domain knowledge.

**① 语义记忆（记事实）**：用户偏好、领域知识等具体事实与概念。实现上通常是持续更新的用户 profile（JSON 文档）或事实文档集合。

**② 情景记忆（记经历）**：回忆过去的事件或动作序列。工程上最常见的落法是 few-shot 示例——把过往成功的交互序列喂给 Agent 当模板。

> Procedural Memory: Remembering Rules: This is the memory of how to perform tasks—the agent's core instructions and behaviors, often contained in its system prompt.

**③ 程序性记忆（记规则）**：如何执行任务的记忆——Agent 的核心指令与行为准则，通常就在系统提示里。原书指出 Agent 修改自己的提示词来适应与改进是常见做法，典型技术是"Reflection"：把当前指令 + 近期交互喂给模型，让它优化自己的指令。**管理者要意识到这一条的治理含义：允许 Agent 改写自己的系统提示，等于把"流程规范的修订权"交给了执行者本人——收益是自适应，代价是行为漂移风险，必须配审计与回滚。**

### 关键工程细节 · 状态写入必须走受控通道

原书在讲 ADK 的 Session / State / MemoryService 三件套时，给出了一条极具普适性的工程铁律：

> Note that direct modification of the `session.state` dictionary after retrieving a session is strongly discouraged as it bypasses the standard event processing mechanism. Such direct changes will not be recorded in the session's event history, may not be persisted by the selected `SessionService`, could lead to concurrency issues, and will not update essential metadata such as timestamps.

**中文提炼**：强烈不建议取出 session 后直接改 state 字典——这绕过了标准事件处理机制。直接修改不会被记入会话事件历史、可能不被持久化、可能引发并发问题、也不会更新时间戳等关键元数据。**抽象掉 ADK 的具体 API，这条讲的是：Agent 的记忆写入必须事件化、可追溯、走统一通道。评审 Agent 平台方案时可以直接问：状态变更有没有审计日志？能不能回放？两个并发会话同时写用户偏好怎么处理？**

托管化是本章隐含的演进方向。原书介绍的 Vertex Memory Bank 代表"记忆即服务"形态：

> Memory Bank, a managed service in the Vertex AI Agent Engine, provides agents with persistent, long-term memory. The service uses Gemini models to asynchronously analyze conversation histories to extract key facts and user preferences.

**中文提炼**：Memory Bank 是 Vertex AI Agent Engine 中的托管服务，为 Agent 提供持久长期记忆——用 Gemini 模型异步分析对话历史，抽取关键事实与用户偏好，按 user ID 等 scope 组织存储，并智能合并新数据、消解矛盾。**"异步抽取 + 矛盾消解"是自建记忆系统最难做好的两件事，也是托管服务的核心卖点。**

### 何时使用 · Rule of Thumb（原文）

> Use this pattern when an agent needs to do more than answer a single question. It is essential for agents that must maintain context throughout a conversation, track progress in multi-step tasks, or personalize interactions by recalling user preferences and history. Implement memory management whenever the agent is expected to learn or adapt based on past successes, failures, or newly acquired information.

### 🆕 2026 视角补充 · 短期记忆的"RAM"类比

《AI Design》（2026）Appendix G（Developing Agents with Google ADK）用更通俗的方式重述了短期记忆的边界：

> The InMemorySessionService gives the Agent a temporary, short-term memory (like RAM). It remembers what you just asked, but every conversation is wiped clean when the script stops.

**中文提炼**：InMemorySessionService 给 Agent 的是临时短期记忆（像 RAM）——记得你刚问过什么，但脚本一停，对话全部清零。2026 书没有超出 2025 版的记忆架构增量（它面向初学者，只覆盖到 Session 层），但这个 RAM 类比适合向非技术干系人解释"为什么 demo 里的 Agent 看起来有记忆、上生产却什么都不记得"——demo 用的往往就是这种进程内存级的会话存储。

### 📍 2026 现状对照

**（编辑判断，非原书内容）**记忆管理在 2026 年成为 Agent 平台竞争的主战场之一——各主流框架与托管服务都把"跨会话记忆"作为标配能力推进。一个书里没写、但实践中非常关键的经验：企业落地的真实瓶颈不在存储技术，而在**记忆治理**：存什么（用户敏感信息入不入长期记忆？合规边界在哪？）、信什么（Agent 自己写入的"经验"被污染怎么办？）、忘什么（过期偏好、错误结论如何淘汰？）。原书的事件化写入铁律是这套治理的技术地基。此段为编辑判断，具体厂商能力现状建议以当期文档为准。

---

## Pattern 9 · Learning and Adaptation（学习与适应）

<aside class="not-prose my-6 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-sm font-bold text-accent-purple tracking-wide uppercase mb-3">📌 管理者速读</h3>
<p class="text-[15px] text-accent-gray-800 leading-relaxed mb-2"><strong>解决什么问题：</strong>预编程逻辑无法覆盖动态环境中的新情况——Agent 遇到设计时没预料到的场景就性能退化。学习与适应让 Agent 从"按指令执行"进化为"随经验变强"，不需要持续人工重编程。</p>
<p class="text-[15px] text-accent-gray-800 leading-relaxed mb-2"><strong>何时用：</strong>Agent 必须在动态、不确定、持续演变的环境中运行时；需要个性化、持续性能改进、自主处理新情况的场景。</p>
<p class="text-[15px] text-accent-gray-800 leading-relaxed"><strong>架构取舍：</strong>本章内容跨度极大——从经典 ML 范式（强化 / 监督 / 无监督）到 LLM 对齐算法（PPO / DPO），再到自改代码的 SICA 和进化式的 AlphaEvolve。管理者需要的判断框架是把"学习"按<strong>风险与介入深度</strong>分级：① 提示层学习（few-shot、记忆召回）——成本低、可控性最好，绝大多数企业场景到这层就够 ② 权重层学习（微调、DPO 对齐）——需要数据管线和评估基建，改的是模型本身 ③ <strong>代码层自改（SICA 式）——Agent 修改自己的源码，收益上限最高、失控风险也最高</strong>。原书对第 ③ 层的架构描述值得逐字读：SICA 必须配独立的异步 overseer 监控循环 / 停滞并有权中止执行，且强制 Docker 隔离。换句话说：<strong>自改能力与独立监督机制是成对出现的，没有后者就不该有前者。</strong></p>
</aside>

### 模式定义 · The Big Picture

> Agents learn and adapt by changing their thinking, actions, or knowledge based on new experiences and data. This allows agents to evolve from simply following instructions to becoming smarter over time.

**中文提炼**：Agent 通过基于新经验和数据改变其思考方式、行动或知识来学习和适应——从"只会照指令做"进化为"随时间变聪明"。原书列出六条学习路径：强化学习（试错 + 奖惩，适合机器人控制 / 游戏）、监督学习（标注样本，适合分类 / 预测）、无监督学习（无标注数据中发现模式）、**LLM Agent 的 few-shot/zero-shot 学习（少量示例即可适应新任务——这是 LLM 时代成本最低的学习形态）**、在线学习（持续吞新数据，适合实时流场景）、基于记忆的学习（召回过往经验调整当前动作，与 Pattern 8 直接衔接）。

### 对齐算法速览 · PPO 与 DPO

原书用相当篇幅解释了两个 LLM 对齐算法。管理者不需要推公式，但需要知道两者的工程含义：

**PPO（近端策略优化）**：强化学习算法，核心是"小步慢改"——通过 clipping 机制建立信任区域，防止一次策略更新走得太远导致性能崩塌。传统 RLHF 对齐是两步走：先用人类偏好数据训练一个奖励模型，再用 PPO 让 LLM 最大化奖励模型给分。原书点出这条路的风险：流程复杂、不稳定，模型可能找到漏洞去"黑"奖励模型——对坏回答骗高分。

> In essence, DPO simplifies alignment by directly optimizing the language model on human preference data. This avoids the complexity and potential instability of training and using a separate reward model, making the alignment process more efficient and robust.

**中文提炼**：DPO（直接偏好优化）跳过奖励模型，直接用偏好数据更新 LLM 策略——本质是教模型"提高'被偏好回答'的生成概率、降低'被弃回答'的概率"。省掉独立奖励模型的训练与维护，对齐过程更高效也更稳健。**决策含义：如果团队要做偏好对齐微调，DPO 路线的工程门槛和不稳定性都显著低于 RLHF+PPO，这也是它迅速流行的原因。**

### 案例研究 · SICA：会改自己代码的 Agent

原书用 Self-Improving Coding Agent（SICA，Robeyns / Aitchison / Szummer）作为学习模式的深度案例——这是一项公开研究（arXiv:2504.15228），不是商业部署：

> This contrasts with traditional approaches where one agent might train another; SICA acts as both the modifier and the modified entity, iteratively refining its code base to improve performance across various coding challenges.

**中文提炼**：与"一个 Agent 训练另一个"的传统路径不同，SICA 既是修改者也是被修改者——迭代地改写自己的代码库来提升编码任务表现。其循环是：回顾历史版本存档 → 按加权评分（成功率 / 耗时 / 算力成本）选出最强版本 → 由它分析存档、直接改代码 → 跑基准测试 → 结果入档 → 重复。SICA 在这个循环中自主发明了越来越精细的工具链：从简单的文件覆写，进化出 Smart Editor、基于 AST 的符号定位器、diff 最小化优化等。

**但真正该带走的是它的安全架构**：

> An asynchronous overseer, another LLM, monitors SICA's behavior, identifying potential issues such as loops or stagnation. It communicates with SICA and can intervene to halt execution if necessary.

**中文提炼**：一个异步 overseer（另一个 LLM）持续监控 SICA 的行为，识别死循环或停滞等问题，可与其通信、必要时干预中止执行。它接收详细的行动报告（调用图 + 消息与工具日志）来发现低效模式。加上强制 Docker 容器隔离（Agent 能执行 shell 命令，必须与宿主机隔离）和可视化观测界面，SICA 展示了一套"自改 Agent 的最小安全配置"：**独立监督者 + 沙箱隔离 + 全程可观测，三者缺一不可。**

原书也如实记录了局限：让 LLM Agent 在每轮迭代中自主提出真正新颖、可行的改进，仍是当前研究的开放难题——自改不等于无限进步。

### 案例研究 · AlphaEvolve 与 OpenEvolve

学习模式的另一分支是进化式优化。Google 的 AlphaEvolve 用 Gemini 双模型组合（Flash 大量生成候选算法 + Pro 深度分析精炼）配自动评估器和进化框架来发现与优化算法。原书列举的成果均为 Google 官方公布数字：数据中心调度改进带来全球算力资源 0.7% 的节省、Gemini 架构核心 kernel 提速 23%、FlashAttention 底层 GPU 指令优化至多 32.5%，以及 4x4 复数矩阵乘法 48 次标量乘法的新算法。OpenEvolve 则是同思路的开源实现，支持整文件进化、多语言、多目标优化。**管理者视角的意义：进化式方法适用于"有明确自动评估函数"的优化问题——评估器能打分，进化就能跑；没有可靠的自动评分，这条路就不成立。**

### 何时使用 · Rule of Thumb（原文）

> Use this pattern when building agents that must operate in dynamic, uncertain, or evolving environments. It is essential for applications requiring personalization, continuous performance improvement, and the ability to handle novel situations autonomously.

### 🆕 2026 视角补充 · RLAIF：把"人类反馈"换成"带宪法的 AI 反馈"

《AI Design》（2026）第 14 章"AI Teaching AI: The Future with RLAIF"是对本章对齐路线的直接增量——2025 书讲到 RLHF/DPO，2026 书往前推了一步：

> This is the cutting-edge idea behind Reinforcement Learning from AI Feedback (RLAIF). The process is almost identical to RLHF, but we replace the human labeler with a highly capable "instructor" AI model. This instructor AI acts as the teacher, providing the preference data needed to align a smaller "student" AI model.

**中文提炼**：RLAIF（基于 AI 反馈的强化学习）流程与 RLHF 几乎一致，区别在于把人类标注员换成一个高能力的"教师"AI——由它生成偏好数据来对齐更小的"学生"模型。这解决了 RLHF 的规模瓶颈：AI 可以 7×24 生成百万级反馈，比人类标注团队快得多、便宜得多。

> Before the AI even starts its real training, we hand the instructor AI a constitution—a set of human-written principles that it absolutely has to follow when making decisions.

**中文提炼**：那如何保证 AI 教师本身可靠？Constitutional AI——在训练开始前给教师 AI 一部"宪法"（一组人类撰写的原则），它做判断时必须遵循。教师模型对每对候选回答先"出声思考"（对照宪法逐条评审），再给出 chosen/rejected 标签。**对管理者的启发：这正是"用 AI 评审 AI"（LLM-as-a-Judge、第一组 Pattern 4 的 Producer-Critic）在训练层的对应物——而"宪法"机制提示了关键治理原则：可以把评判工作交给 AI 规模化，但评判标准必须由人类书面固化。**（原稿定位：2026 书 Chapter 14，全文 6784 行起。）

### 📍 2026 现状对照

**（编辑判断，非原书内容）**在 2026 年的企业实践里，"Agent 学习"的主流落地形态既不是自改代码也不是微调，而是 Pattern 8 讲的记忆回路——把成功经验、失败教训写入长期记忆，下次任务召回参考。这条路径成本最低、可审计、可回滚。SICA 式的代码级自改在生产环境仍属前沿实验；如果团队提出此类方案，评审时应直接引用原书的安全三件套（独立 overseer / 沙箱隔离 / 全程可观测）作为准入门槛。此段为编辑判断，不构成对当期行业状态的事实断言。

---

## Pattern 10 · Model Context Protocol（MCP · 模型上下文协议）

<aside class="not-prose my-6 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-sm font-bold text-accent-purple tracking-wide uppercase mb-3">📌 管理者速读</h3>
<p class="text-[15px] text-accent-gray-800 leading-relaxed mb-2"><strong>解决什么问题：</strong>没有标准协议时，LLM 与每个外部工具 / 数据源的对接都是一次性定制开发——不可复用、难以扩展。MCP 是一个开放标准，把"LLM 怎么发现、连接、使用外部能力"统一成客户端-服务器协议：MCP Server 暴露工具（可执行动作）、资源（静态数据）、提示模板，任何合规的 MCP Client 都能即插即用。</p>
<p class="text-[15px] text-accent-gray-800 leading-relaxed mb-2"><strong>何时用：</strong>构建复杂、可扩展、企业级的 Agent 系统，工具与数据源集合多样且持续演变；需要跨 LLM 互操作；需要 Agent 不重新部署就能动态发现新能力。反之，功能少而固定的简单应用，直接函数调用就够。</p>
<p class="text-[15px] text-accent-gray-800 leading-relaxed"><strong>架构取舍：</strong>本章最有分量的内容不是协议本身，而是原书给出的两条反直觉警告。<strong>其一：MCP 只是"Agent 接口的契约"，效果取决于底层 API 的设计</strong>——直接把遗留 API 原样包一层 MCP 往往是次优解（例如工单系统只支持逐条取全量详情，Agent 做高优先级工单汇总时又慢又不准；底层 API 必须先补上过滤、排序等确定性能力）。<strong>其二：MCP 不保证数据格式对 Agent 友好</strong>——包一个返回 PDF 的文档库，消费端 Agent 解析不了照样没用，应先做返回 Markdown 的 API。两条合起来是一个管理判断：<strong>上 MCP 之前先做 API 的"Agent 就绪度"改造，协议标准化替代不了接口设计。</strong></p>
</aside>

### 模式定义 · Pattern Overview

> It's an open standard designed to standardize how LLMs like Gemini, OpenAI's GPT models, Mixtral, and Claude communicate with external applications, data sources, and tools. Think of it as a universal connection mechanism that simplifies how LLMs obtain context, execute actions, and interact with various systems.

**中文提炼**：MCP 是一个开放标准，统一 Gemini、GPT、Mixtral、Claude 等各家 LLM 与外部应用、数据源、工具的通信方式——一个通用连接机制，简化 LLM 获取上下文、执行动作、与各类系统交互的过程。原书的比喻是"通用适配器"：任何 LLM 不需要逐一定制集成，就能接入任何外部系统。

### 两条关键警告 · 协议不能替代接口设计

> However, MCP is a contract for an "agentic interface," and its effectiveness depends heavily on the design of the underlying APIs it exposes. There is a risk that developers simply wrap pre-existing, legacy APIs without modification, which can be suboptimal for an agent.

**中文提炼**：MCP 是"Agent 接口"的契约，其效果高度依赖它所暴露的底层 API 的设计。风险在于开发者不加改造地直接包装遗留 API——这对 Agent 往往是次优的。原书举例：工单系统 API 若只支持逐条取完整详情，Agent 汇总高优先级工单时会又慢又不准，底层 API 需要先具备过滤、排序等确定性特性。紧接着是全章最值得引用的一句：

> This highlights that agents do not magically replace deterministic workflows; they often require stronger deterministic support to succeed.

**中文提炼**：**Agent 不会魔法般取代确定性工作流；恰恰相反，它们往往需要更强的确定性支撑才能成功。**这句话值得贴在每个"用 Agent 替代现有系统"的立项书上——非确定性的 Agent 要跑得好，底下的确定性地基（API 能力、数据质量、schema 约束）反而要打得更牢。

> An API is only useful if its data format is agent-friendly, a guarantee that MCP itself does not enforce. For instance, creating an MCP server for a document store that returns files as PDFs is mostly useless if the consuming agent cannot parse PDF content.

**中文提炼**：API 只有在数据格式对 Agent 友好时才有用——而这一点 MCP 本身并不保证。给返回 PDF 的文档库做 MCP server，如果消费端 Agent 解析不了 PDF，基本等于白做；正确做法是先做一个返回文本（如 Markdown）的 API。**连接问题和数据可消费性问题是两件事，MCP 只解决前者。**

### MCP vs. 函数调用 · 什么时候需要升级到协议层

原书用五个维度对比了两者：函数调用是**专有的、厂商特定的**一对一机制，工具在会话里被显式告知、集成与特定应用紧耦合；MCP 是**开放标准协议**，客户端-服务器架构，支持动态发现（client 可查询 server 有什么能力）、工具可复用（一个 MCP server 服务所有合规客户端）。

> In short, function calling provides direct access to a few specific functions, while MCP is the standardized communication framework that lets LLMs discover and use a vast range of external resources. For simple applications, specific tools are enough; for complex, interconnected AI systems that need to adapt, a universal standard like MCP is essential.

**中文提炼**：函数调用是给 AI 一套定制工具（一把特定的扳手和螺丝刀），适合任务固定的工坊；MCP 是建一套通用标准电源插座系统——它本身不提供工具，但让任何厂商的合规工具即插即用。简单应用用前者足矣；需要适应演变的复杂互联 AI 系统，通用标准是刚需。**原书还点出 MCP 联邦模式的企业价值：把分散的遗留服务包上 MCP 合规接口就能纳入现代生态，服务本身继续独立运行，却可被 LLM 编排进新工作流——不需要昂贵的重写。**

### 关键工程细节 · 安全与部署形态

> Security: Exposing tools and data via any protocol requires robust security measures. An MCP implementation must include authentication and authorization to control which clients can access which servers and what specific actions they are permitted to perform.

**中文提炼**：通过任何协议暴露工具和数据都需要健壮的安全措施。MCP 实现必须包含认证与授权——控制哪些客户端能访问哪些 server、被允许执行哪些具体动作。原书同时列出了部署形态的选择维度：本地 server（速度快、敏感数据不出机）vs 远程 server（组织级共享、可扩展）；本地传输用 JSON-RPC over STDIO，远程用 Streamable HTTP / SSE。**管理者的检查清单：工具目录有没有统一鉴权？错误如何回传给 LLM（工具失败、server 不可用时 Agent 能否理解并换路）？敏感域工具是否强制本地部署？**

### 何时使用 · Rule of Thumb（原文）

> Use the Model Context Protocol (MCP) when building complex, scalable, or enterprise-grade agentic systems that need to interact with a diverse and evolving set of external tools, data sources, and APIs. It is ideal when interoperability between different LLMs and tools is a priority, and when agents require the ability to dynamically discover new capabilities without being redeployed. For simpler applications with a fixed and limited number of predefined functions, direct tool function calling may be sufficient.

### 🆕 2026 视角补充 · "USB-C 口"与 MCP/A2A 分工

《AI Design》（2026）Appendix G: Developing Agents with Google ADK 用一组更直白的类比重述了 MCP 的定位，并把它与 A2A 的分工讲透了：

> Now, thanks to MCP (standardized by Anthropic), if a tool is "MCP-ready," any agent can just plug in and use it, no sweat. It's like a standard USB-C port: you can connect a hard drive, a screen, or a microphone to your laptop, and they all just work.

**中文提炼**：MCP（由 Anthropic 标准化）之下，只要工具是"MCP-ready"的，任何 Agent 即插即用——像标准 USB-C 口，硬盘、屏幕、麦克风插上就能工作。2026 书在此明确署名了协议的标准化者是 Anthropic（2025 书未展开这一点），并给出了与 A2A 的一句话分工：

> They can't tackle big jobs without working together: A2A handles the teamwork, and MCP handles the tools.

**中文提炼**：**A2A 管协作，MCP 管工具**——两者不是竞争关系而是互补层：Agent 之间的任务移交走 A2A（第三组 Pattern 15 详述），单个 Agent 接工具走 MCP。2026 书还给出 Manager Agent 通过 Agent Card 找到 Finance Agent（A2A），后者再用 MCP 接股票数据库的完整协作示例。（原稿定位：2026 书 Appendix G: Developing Agents with Google ADK 的 "MCP and A2A" 小节，全文 12385 行起。）

### 📍 2026 现状对照

**（编辑判断，非原书内容）**MCP 是本书 21 个模式中协议化程度最高、生态扩散最快的一个。第一组 Pattern 5 曾指出"工具层应作为平台资产管理"，MCP 正是这一判断的协议载体。但需要提醒：MCP 生态的快速膨胀也把安全问题推到了台前——第三方 MCP server 本质是让外部代码进入你的工具调用链，供应链风险（恶意 server、工具描述注入）成为新攻击面。原书"认证 + 授权"的要求是底线而非全部；企业接入外部 MCP server 时应比照第三方依赖引入流程做安全评审。此段为编辑判断，具体生态现状以当期资料为准。

---

## Pattern 11 · Goal Setting and Monitoring（目标设定与监控）

<aside class="not-prose my-6 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-sm font-bold text-accent-purple tracking-wide uppercase mb-3">📌 管理者速读</h3>
<p class="text-[15px] text-accent-gray-800 leading-relaxed mb-2"><strong>解决什么问题：</strong>没有明确目标的 Agent 只能被动响应，无法判断自己是否在走向成功。此模式做两件事：给 Agent 具体的、可衡量的目标；配套监控机制持续追踪进度与环境状态，形成"评估表现 → 纠偏 → 调整计划"的反馈回路，把被动响应系统变成主动的目标导向系统。</p>
<p class="text-[15px] text-accent-gray-800 leading-relaxed mb-2"><strong>何时用：</strong>Agent 需要在无人持续干预下自主执行多步任务、适应动态条件、可靠达成高层目标时——客服工单闭环、项目里程碑跟踪、内容审核、自动交易等。目标定义建议直接套 SMART 准则（具体 / 可衡量 / 可达成 / 相关 / 有时限）。</p>
<p class="text-[15px] text-accent-gray-800 leading-relaxed"><strong>架构取舍：</strong>本章真正的分量在原书对自己示例代码的"自我拆台"。示例用同一个 LLM 生成代码、评审代码、裁决目标是否达成——原书随即列出这个设计的全部弱点：<strong>模型可能误解目标含义却自评成功；可能幻觉；同一个模型既当运动员又当裁判，很难发现自己方向错了</strong>；且简单的 True/False 监控有永不收敛的死循环风险。给出的修正方向是角色分离的多 Agent 结构（独立的 Code Reviewer 显著改善评估客观性）。<strong>管理判断：目标监控的裁判必须独立于执行者——这与第一组 Pattern 4 的 Producer-Critic 分离是同一条原则在目标层的应用；此外"目标达成判定"这一步能用确定性校验（测试通过、指标阈值）就不要用 LLM 主观裁决。</strong></p>
</aside>

### 模式定义 · Pattern Overview

> It's about giving agents specific objectives to work towards and equipping them with the means to track their progress and determine if those objectives have been met.

**中文提炼**：目标设定与监控 = 给 Agent 明确的努力方向 + 让它有手段追踪进度、判断目标是否达成。原书用旅行规划类比：先定目标状态（去哪）、认清初始状态（从哪出发）、考虑约束（预算、路线），再展开步骤序列——目标是规划（Pattern 6）的前提，监控是自主运行的保障。两者合起来给了 Agent"知道自己该干什么、干得怎么样"的自我管理框架。

原书列举的应用场景有一个共同结构值得注意：每个场景都同时定义了**目标 + 监控信号 + 未达成时的动作**——客服 Agent 目标是"解决账单问题"，监控确认账单变更与客户反馈，解决不了就**升级**；项目管理 Agent 监控任务状态与资源，里程碑有风险就**标记并建议纠正**。这个三元组（目标 / 信号 / 兜底动作）是把该模式落地成产品需求的最小模板。

### 关键工程细节 · 原书对自身示例的诚实批判

原书给出的示例是一个"生成代码 → 自评 → 修订"循环的编码 Agent（书中假设场景，非真实部署）：LLM 按用户目标清单（简洁 / 功能正确 / 覆盖边界情况）生成代码，再让同一个 LLM 评审并输出 True/False 判定，False 就带着反馈进入下一轮，最多五轮。**这一章最有价值的部分是紧随其后的 Caveats**：

> An LLM may not fully grasp the intended meaning of a goal and might incorrectly assess its performance as successful. Even if the goal is well understood, the model may hallucinate. When the same LLM is responsible for both writing the code and judging its quality, it may have a harder time discovering it is going in the wrong direction.

**中文提炼**：LLM 可能没真正理解目标含义却把自己的表现误判为成功；即便理解了目标，也可能幻觉；**当同一个 LLM 既写代码又评代码时，它更难发现自己走错了方向**。这三句话构成了对"LLM 自我评估"这一常见廉价方案的系统性否定。

> Ultimately, LLMs do not produce flawless code by magic; you still need to run and test the produced code. Furthermore, the "monitoring" in the simple example is basic and creates a potential risk of the process running forever.

**中文提炼**：LLM 不会魔法般产出无瑕疵代码——生成的代码终究要真正运行和测试；而且示例里的"监控"很初级，存在流程永远跑下去的风险。**两个工程铁律：① 能用真实执行验证的（跑测试、编译）绝不用 LLM 口头判定替代 ② 任何目标循环必须有硬性迭代上限与超时。**

修正方向是职责分离的多 Agent 结构：

> In this multi-agent system, the Code Reviewer, acting as a separate entity from the programmer agent, has a prompt similar to the judge in the example, which significantly improves objective evaluation.

**中文提炼**：在多 Agent 系统中，Code Reviewer 作为独立于编程 Agent 的实体承担裁判职责，显著改善评估的客观性。原书作者描述了自己搭建的角色分工（Peer Programmer / Code Reviewer / Documenter / Test Writer / Prompt Refiner）——这种结构天然导向更好的实践，比如由 Test Writer 为 Peer Programmer 的产出写单元测试。

### 何时使用 · Rule of Thumb（原文）

> Use this pattern when an AI agent must autonomously execute a multi-step task, adapt to dynamic conditions, and reliably achieve a specific, high-level objective without constant human intervention.

原书 Key Takeaways 中还有一条可直接落地的目标定义准则：

> Goals should be specific, measurable, achievable, relevant, and time-bound (SMART).

**中文提炼**：Agent 的目标应遵循 SMART 准则——具体、可衡量、可达成、相关、有时限。给 Agent 写目标和给下属定 OKR 是同构问题："提升代码质量"是坏目标，"通过全部单元测试且圈复杂度不超标"才是 Agent 能监控的目标。

### 🆕 2026 视角补充

经查证，《AI Design》（2026）无与"目标设定与监控"模式对应的增量内容（该书 Bonus Chapter 18 讲 Agent 基础与 ReAct 循环，未涉及目标监控机制）。按规范不硬凑。

### 📍 2026 现状对照

**（编辑判断，非原书内容）**本章"裁判独立于执行者 + 优先确定性验证"的原则，与 2026 年 Agent 工程社区普遍强调的 evaluation 实践方向一致（LLM-as-a-Judge 的偏差问题、可验证奖励的价值在业界已被广泛讨论）。原书的 Caveats 段等于提前给出了这些问题的清单。此段为编辑判断，不作行业现状的具体断言。

---

## Pattern 12 · Exception Handling and Recovery（异常处理与恢复）

<aside class="not-prose my-6 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-sm font-bold text-accent-purple tracking-wide uppercase mb-3">📌 管理者速读</h3>
<p class="text-[15px] text-accent-gray-800 leading-relaxed mb-2"><strong>解决什么问题：</strong>真实环境不保证完美条件——工具失败、网络异常、数据损坏随时发生。没有结构化的容错设计，Agent 就是脆弱系统，无法进入关键业务。此模式给 Agent 装上"检测问题 → 优雅处理 → 恢复稳定"的完整链路，或至少保证受控失败。</p>
<p class="text-[15px] text-accent-gray-800 leading-relaxed mb-2"><strong>何时用：</strong>原书的答案是"几乎总是"——任何部署在动态真实环境、以可靠性为要求的 Agent 都需要。这是 21 个模式中少数没有"不适用场景"的一个。</p>
<p class="text-[15px] text-accent-gray-800 leading-relaxed"><strong>架构取舍：</strong>本章的框架价值在于把容错拆成三个必须分别设计的阶段：<strong>检测</strong>（无效工具输出、API 错误码、超时、语义不连贯的响应——注意最后一项是 Agent 特有的：输出格式正确但内容胡说，传统监控抓不到）、<strong>处理</strong>（日志 / 重试 / 降级路径 / 优雅降级 / 通知，五件套）、<strong>恢复</strong>（状态回滚 / 根因诊断 / 自我修正 / 升级人工）。管理者评审时的关键问题不是"有没有 try-catch"，而是：<strong>五件套里哪几件有？状态回滚做得到吗（Agent 干了一半的副作用能撤销吗）？什么条件下升级人工？</strong>与传统软件容错的最大区别在于：Agent 的失败往往不是抛异常，而是"看起来成功了但结果是错的"——所以检测层必须包含对输出内容本身的校验，这也是它与 Pattern 4（反思）天然联动的原因。</p>
</aside>

### 模式定义 · Pattern Overview

> The Exception Handling and Recovery pattern addresses the need for AI agents to manage operational failures. This pattern involves anticipating potential issues, such as tool errors or service unavailability, and developing strategies to mitigate them.

**中文提炼**：异常处理与恢复模式解决的是 AI Agent 管理运行失败的需求——预判潜在问题（工具错误、服务不可用），并制定缓解策略：错误日志、重试、降级路径、优雅降级、通知五类手段。

> Additionally, the pattern emphasizes recovery mechanisms like state rollback, diagnosis, self-correction, and escalation, to restore agents to stable operation.

**中文提炼**：此外，该模式强调恢复机制——状态回滚、诊断、自我修正、升级人工——把 Agent 恢复到稳定运行状态。**"处理"和"恢复"是两个阶段：前者保证当下不崩，后者保证系统回到可信状态并避免复发。很多团队只做了前者。**

与反思模式的联动，原书点得很明确：

> This pattern may sometimes be used with reflection. For example, if an initial attempt fails and raises an exception, a reflective process can analyze the failure and reattempt the task with a refined approach, such as an improved prompt, to resolve the error.

**中文提炼**：此模式可与反思（Pattern 4）配合使用——初次尝试失败抛出异常后，由反思过程分析失败原因，用改进后的方式（如优化的 prompt）重试。**这是"智能重试"与"盲目重试"的分界：带失败分析的重试才有收敛性，简单原样重试对非瞬态错误只是浪费调用。**

### 关键工程细节 · Agent 特有的错误检测面

> This could manifest as invalid or malformed tool outputs, specific API errors such as 404 (Not Found) or 500 (Internal Server Error) codes, unusually long response times from services or APIs, or incoherent and nonsensical responses that deviate from expected formats.

**中文提炼**：错误的表现形式包括：无效或格式错误的工具输出、具体的 API 错误码（404 / 500）、服务响应时间异常拉长、以及**偏离预期格式的不连贯、无意义响应**。前三类是传统系统监控的老面孔；第四类是 LLM 系统特有的——请求成功返回、格式看似正常，但内容是幻觉或胡言。原书还提到可由其他 Agent 或专门监控系统做主动异常检测，在问题恶化前捕获——这与 Pattern 9 SICA 的 overseer 是同一思路。

恢复阶段最难也最重要的一环是状态回滚：

> It could involve reversing recent changes or transactions to undo the effects of the error (state rollback). A thorough investigation into the cause of the error is vital for preventing recurrence.

**中文提炼**：恢复可能涉及撤销近期变更或事务以消除错误影响（状态回滚）；对错误根因的彻底调查是防止复发的关键。**管理含义：如果 Agent 的动作有真实世界副作用（发了邮件、改了数据库、下了单），回滚能力必须在设计工具时就考虑——哪些操作可逆、哪些不可逆、不可逆操作是否要前置人工确认（引出 Pattern 13）。事后想补回滚，通常已经来不及。**

原书的 ADK 示例展示了降级路径的编排化实现（书中示例，非真实部署）：用 SequentialAgent 串三个子 Agent——主处理器尝试精确定位工具，失败则写状态标记；降级处理器检查该标记，失败时改用粗粒度的区域信息工具；响应 Agent 最后统一从状态中取结果呈现，取不到就致歉。**值得注意的设计点：降级逻辑通过共享状态传递失败信号、由确定性的顺序编排保证执行次序——而不是指望单个 LLM 在一段长 prompt 里自己记得"如果失败就换方案"。容错逻辑放进架构，比放进提示词可靠。**

### 何时使用 · Rule of Thumb（原文）

> Use this pattern for any AI agent deployed in a dynamic, real-world environment where system failures, tool errors, network issues, or unpredictable inputs are possible and operational reliability is a key requirement.

### 🆕 2026 视角补充

经查证，《AI Design》（2026）无与"异常处理与恢复"模式对应的增量内容（该书 Agent 章节聚焦 ReAct 循环与工具接入，未涉及容错机制）。按规范不硬凑。

### 📍 2026 现状对照

**（编辑判断，非原书内容）**本章框架与传统 SRE 实践高度同构（错误预算、优雅降级、runbook、事后复盘都能一一对应），这是好事——意味着企业已有的可靠性工程资产大部分可以平移到 Agent 系统。真正的新课题是上文强调的"语义失败"检测：请求层面全绿、内容层面全错。将输出校验（schema 校验、业务规则断言、抽样人工复核）纳入 Agent 的监控面，是 Agent 可靠性工程区别于传统 SRE 的核心增量。此段为编辑判断。

---

## Pattern 13 · Human-in-the-Loop（人在回路）

<aside class="not-prose my-6 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-sm font-bold text-accent-purple tracking-wide uppercase mb-3">📌 管理者速读</h3>
<p class="text-[15px] text-accent-gray-800 leading-relaxed mb-2"><strong>解决什么问题：</strong>在复杂、模糊、高风险领域，AI 的错误代价可能是安全、财务或伦理层面的——完全自主并不明智。HITL 把人类的判断、创造力与情境理解嵌入 AI 工作流，确保关键决策有人类把关，同时保留 AI 在计算与规模上的优势。</p>
<p class="text-[15px] text-accent-gray-800 leading-relaxed mb-2"><strong>何时用：</strong>错误后果重大的领域（医疗、金融、自动系统）；LLM 无法可靠处理的模糊 / 微妙任务（内容审核、复杂客服升级）；需要高质量人工标注持续改进模型的场景。原书列出六种实现形态：人类监督、干预纠正、反馈学习（RLHF）、决策增强（AI 出分析人做决定）、人机协作、升级策略。</p>
<p class="text-[15px] text-accent-gray-800 leading-relaxed"><strong>架构取舍：</strong>原书的 Caveats 段给出了 HITL 的三大硬约束，每一条都是预算与组织问题而非技术问题：<strong>① 不可扩展</strong>——人管不了百万级任务，准确性与吞吐量存在根本 trade-off，现实解是混合架构（自动化管规模、HITL 管精度）<strong>② 依赖专家水平</strong>——AI 能生成代码，但只有熟练开发者能发现细微错误并给出正确修正；标注员也需要专门培训才能产出高质量纠正数据 <strong>③ 隐私成本</strong>——敏感信息暴露给人工前必须严格匿名化，流程复杂度再加一层。<strong>管理判断：HITL 不是"加个审批按钮"，而是一条需要预算的人力生产线——评审方案时要问清人工审核点的预期流量、审核人的技能要求、以及审核疲劳后的质量衰减怎么办。</strong></p>
</aside>

### 模式定义 · Pattern Overview

> In such scenarios, full autonomy—where AI systems function independently without any human intervention—may prove to be imprudent. HITL acknowledges this reality and emphasizes that even with rapidly advancing AI technologies, human oversight, strategic input, and collaborative interactions remain indispensable.

**中文提炼**：在复杂、模糊或高风险场景下，完全自主（AI 独立运行、无人干预）可能并不明智。HITL 承认这一现实：即便 AI 技术快速演进，人类监督、战略输入与协作交互仍不可或缺。定位上，HITL 不把 AI 视为人类的替代，而是增强人类能力的工具——目标是构建一个人与 AI 各展所长的协作生态。

六种实现形态中，**升级策略（Escalation Policies）**是工程上最需要显式设计的一种：

> Escalation Policies are established protocols that dictate when and how an agent should escalate tasks to human operators, preventing errors in situations beyond the agent's capability.

**中文提炼**：升级策略是一套既定协议，规定 Agent 何时、如何把任务升级给人类操作员——防止 Agent 在能力边界之外犯错。**"何时"和"如何"都要事先写死：触发条件（置信度低于阈值 / 命中敏感操作清单 / 用户明确要求）、移交内容（上下文完整交接而非让用户重述）、响应时限。没有显式升级协议的 HITL 只是摆设。**

### 关键工程细节 · 三大硬约束（原书 Caveats）

> Despite its benefits, the HITL pattern has significant caveats, chief among them being a lack of scalability. While human oversight provides high accuracy, operators cannot manage millions of tasks...

**中文提炼**：HITL 最大的缺陷是不可扩展——人工监督精度高，但操作员管不了百万级任务，这个根本性 trade-off 通常要靠混合方案解决：自动化负责规模，HITL 负责精度。

> Furthermore, the effectiveness of this pattern is heavily dependent on the expertise of the human operators; for example, while an AI can generate software code, only a skilled developer can accurately identify subtle errors and provide the correct guidance to fix them.

**中文提炼**：其次，此模式的效果高度依赖人类操作员的专业水平——AI 能生成代码，但只有熟练开发者能准确识别细微错误并给出正确的修正指引。**这条对"用便宜的初级人力做 AI 审核"的常见省钱思路是直接否定：审核者水平低于任务要求时，HITL 提供的是虚假安全感。**

> Lastly, implementing HITL raises significant privacy concerns, as sensitive information must often be rigorously anonymized before it can be exposed to a human operator, adding another layer of process complexity.

**中文提炼**：最后，HITL 带来隐私问题——敏感信息在暴露给人类操作员之前往往必须严格匿名化，又增加一层流程复杂度。

### 变体 · Human-on-the-Loop（人在环上）

> "Human-on-the-loop" is a variation of this pattern where human experts define the overarching policy, and the AI then handles immediate actions to ensure compliance.

**中文提炼**：Human-on-the-loop 是 HITL 的变体——人类专家制定总体政策，AI 在政策约束内处理即时动作。原书两例：交易系统里人定策略（"70% 科技股 30% 债券、单一公司不超 5%、跌破买入价 10% 自动卖出"），AI 实时盯盘高速执行；呼叫中心里经理定规则（"提到服务中断立即转技术专员"），AI 自主执行路由。**区别在介入时点：in-the-loop 是人在执行路径上逐案审批（低吞吐、高保障），on-the-loop 是人在政策层管规则、AI 全速执行（高吞吐、靠事前规则约束）。对不可逆高危操作用前者，对高频规则化决策用后者——这个选择本身就是一次风险分级。**

原书的 ADK 示例（书中示例，非真实部署）展示了最小实现：技术支持 Agent 配三个工具——troubleshoot_issue、create_ticket、escalate_to_human，指令里明确"超出基础排障的复杂问题调用升级工具转人工"。升级能力是作为**工具**建模的——这意味着"转人工"和其他动作一样有明确的调用条件、参数和日志，而不是靠模型临场发挥。

### 何时使用 · Rule of Thumb（原文）

> Use this pattern when deploying AI in domains where errors have significant safety, ethical, or financial consequences, such as in healthcare, finance, or autonomous systems. It is essential for tasks involving ambiguity and nuance that LLMs cannot reliably handle, like content moderation or complex customer support escalations.

### 🆕 2026 视角补充 · Trust Gap 与 Artifacts：审批点前移到计划层

《AI Design》（2026）Appendix I（Guide to Google Antigravity）从开发工具视角给出了 HITL 的一个重要演进——"信任缺口"问题及其解法：

> The fundamental problem in AI coding is trust. When an AI, such as ChatGPT, reports "Done!" after being asked to "fix the bug," a manual code review is still required to verify that no new issues have been introduced. This lack of transparency is a major source of frustration.

**中文提炼**：AI 编码的根本问题是信任——AI 说"搞定了"，人还是得手工 review 确认没引入新问题，这种不透明是挫败感的主要来源。Antigravity 的解法是 Artifacts（工作证据）：

> Artifacts are analogous to a math student showing their work. They don't just provide the final answer, "42"; they detail the steps taken, allowing you to understand the process that led to the solution.

**中文提炼**：Artifacts 就像数学学生"写出解题过程"——不只给最终答案，还展示每一步，让人能理解结论是怎么来的。具体形态包括：**可编辑的计划**（Agent 动手前先写 To-Do 清单，人可以直接改——"用蓝色按钮"可以批注成"改红色"，计划随之更新）、前后对比截图、操作录屏（让 Agent 证明"登录功能可用"时，它录下自己点击登录、输入密码的视频）。**这把 HITL 的介入点从"事后审输出"前移到了"事前审计划"——与第一组 Pattern 6 的 2026 对照（显式计划文件）互相印证：计划可见且可编辑，是人类在 Agent 执行前介入的最高杠杆点。**（原稿定位：2026 书 Appendix I "Part 3: The Trust Gap"，全文 13595 行起。）

此外该书第 10 章在治理幻觉的语境下重申了 HITL 的定位："Get an Expert to Check It (Human in The loop)——对于真正重要的用途，人类专家（如医生或律师）应始终在任何人采取行动之前核查 AI 的答案"（全文 5512-5514 行），与 2025 书的 Decision Augmentation 形态一致，无新增机制。

### 📍 2026 现状对照

**（编辑判断，非原书内容）**HITL 在 2026 年的工程共识方向是"分级审批"：按操作风险分层（只读操作自动放行 / 可逆写操作事后抽查 / 不可逆或高危操作前置确认），而非对所有动作一刀切人工审批——这正是原书"可扩展性硬约束"的必然推论。评审 Agent 方案时，"哪些工具调用需要人工确认"应该是一张显式清单，且与工具权限治理（Pattern 5、10）共用同一套分级。此段为编辑判断。

---

## Pattern 14 · Knowledge Retrieval / RAG（知识检索）

<aside class="not-prose my-6 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-sm font-bold text-accent-purple tracking-wide uppercase mb-3">📌 管理者速读</h3>
<p class="text-[15px] text-accent-gray-800 leading-relaxed mb-2"><strong>解决什么问题：</strong>LLM 的知识是静态的、截止于训练数据，不含实时信息与企业私有数据。RAG 在生成前先从外部知识库检索相关片段、增强进 prompt，让回答基于可验证的最新数据——降低幻觉、支持引用溯源，把 LLM 从"闭卷考试"变成"开卷考试"。</p>
<p class="text-[15px] text-accent-gray-800 leading-relaxed mb-2"><strong>何时用：</strong>需要基于特定、最新或专有信息回答问题时——内部文档问答、客服机器人、需要带引用的事实性回答。这是企业 LLM 应用中渗透率最高的模式，没有之一。</p>
<p class="text-[15px] text-accent-gray-800 leading-relaxed"><strong>架构取舍：</strong>本章给出了三级演进路线，成本与能力同步上升：<strong>标准 RAG</strong>（向量检索 + 增强生成，原书如实列出其结构性短板：答案分散在多个 chunk 时检索不全、检索质量决定一切、矛盾信息难以综合、知识库需预处理且要定期与源同步、延迟 / 成本 / token 全面上升）→ <strong>GraphRAG</strong>（知识图谱替代向量库，擅长跨文档关系推理，但构建维护成本高、灵活性低、效果完全取决于图谱质量）→ <strong>Agentic RAG</strong>（在检索层加推理 Agent 做源验证、矛盾调解、多步分解、工具补漏——代价是复杂度、延迟、成本齐升，且 Agent 本身成为新的错误源）。<strong>管理判断：先把标准 RAG 的地基打好（chunking 策略、混合检索、知识库同步机制），再谈升级——大多数"RAG 效果差"的问题出在数据工程层，不是缺一个更聪明的 Agent。</strong></p>
</aside>

### 模式定义 · Pattern Overview

> RAG enables LLMs to access and integrate external, current, and context-specific information, thereby enhancing the accuracy, relevance, and factual basis of their outputs.

**中文提炼**：RAG 让 LLM 能访问并整合外部的、最新的、特定上下文的信息，从而提升输出的准确性、相关性与事实基础。流程：用户查询先经语义搜索（理解意图而非关键词匹配）从知识库取出最相关的片段，增强进原始 prompt，再交给 LLM 生成——回答因此锚定在检索到的数据上。四大收益：突破训练数据时效限制、降低幻觉、接入企业内部专有知识、支持引用（citation）溯源。

支撑 RAG 的技术底座原书用一章篇幅展开：**Embeddings**（文本的向量化数值表示，语义相近则向量距离近）、**语义相似度**（"a furry feline companion"和"a domestic cat"没有共同实词，但向量空间中高度相近）、**Chunking**（大文档切成可检索的小块——切法直接决定上下文完整性）、**向量数据库**（为语义检索优化的专用存储，HNSW 等算法支撑百万级向量的快速近邻搜索）。检索技术上，原书强调**混合搜索**：向量搜索管语义、BM25 关键词算法管字面精确匹配，两者融合才能同时捕获概念相关与字面命中。

### 关键工程细节 · 标准 RAG 的结构性短板（原书如实列举）

> A primary issue arises when the information needed to answer a query is not confined to a single chunk but is spread across multiple parts of a document or even several documents. In such cases, the retriever might fail to gather all the necessary context, leading to an incomplete or inaccurate answer.

**中文提炼**：首要问题是——当答案所需信息不在单一 chunk 内、而是分散在文档多处甚至多个文档中时，检索器可能收集不全必要上下文，导致答案不完整或不准确。此外检索质量决定一切：取回无关 chunk 就是给 LLM 注入噪声；综合相互矛盾的来源仍是重大难题。

> Consequently, this knowledge requires periodic reconciliation to remain up-to-date, a crucial task when dealing with evolving sources like company wikis. This entire process can have a noticeable impact on performance, increasing latency, operational costs, and the number of tokens used in the final prompt.

**中文提炼**：知识库需要定期与源数据对账才能保持最新——对公司 wiki 这类持续演变的源尤其关键；整条链路对性能有可见影响：延迟、运营成本、最终 prompt 的 token 消耗都会上升。**管理者最容易低估的就是这条：RAG 不是一次性建库，而是一条需要持续运营的数据管线——源变更监测、重嵌入、索引更新、质量回归，都是长期成本。**

### 演进一 · GraphRAG：用关系换深度

> A key advantage is its ability to synthesize answers from information fragmented across multiple documents, a common failing of traditional RAG.

**中文提炼**：GraphRAG 用知识图谱替代简单向量库，通过遍历实体（节点）间的显式关系（边）回答复杂查询——其关键优势正是综合分散在多文档中的信息，这恰好是传统 RAG 的常见失败点。适用场景：金融分析（公司与市场事件的关联）、科研（基因与疾病的关系发现）。

> The primary drawback, however, is the significant complexity, cost, and expertise required to build and maintain a high-quality knowledge graph.

**中文提炼**：主要代价是构建和维护高质量知识图谱所需的复杂度、成本与专业能力都很高；灵活性更低、延迟可能更高，效果完全取决于图谱的质量与完整性。**取舍一句话：深度互联的洞察比速度和简单性更重要时才值得上 GraphRAG。**

### 演进二 · Agentic RAG：在检索层加一个"把关人"

> Instead of just retrieving and augmenting, an "agent"—a specialized AI component—acts as a critical gatekeeper and refiner of knowledge. Rather than passively accepting the initially retrieved data, this agent actively interrogates its quality, relevance, and completeness, as illustrated by the following scenarios.

**中文提炼**：Agentic RAG 不再是"检索了就用"——一个专门的 Agent 充当知识的把关人和精炼者，主动审问检索结果的质量、相关性与完整性。原书给出四种能力（均为书中假设场景）：**① 源验证**——问"公司远程办公政策"，标准 RAG 可能同时捞出 2020 年博客和 2025 年正式政策文件，Agent 会按元数据识别最新权威源、丢弃过期内容 **② 矛盾调解**——预算提案写 €50,000、财务终报写 €65,000，Agent 识别冲突并优先可靠源 **③ 多步分解**——"我们产品与竞品 X 的功能价格对比"被拆成四个子查询分别检索再综合 **④ 缺口识别 + 工具补漏**——内部知识库周更、查不到昨天发布产品的市场反应时，激活实时 web 搜索工具补上。

但原书对代价同样毫不含糊：

> Furthermore, the agent itself can become a new source of error; a flawed reasoning process could cause it to get stuck in useless loops, misinterpret a task, or improperly discard relevant information, ultimately degrading the quality of the final response.

**中文提炼**：Agent 本身会成为新的错误源——有缺陷的推理可能让它陷入无用循环、误解任务、或错误地丢弃相关信息，最终反而拉低回答质量。加上复杂度、成本、延迟的显著上升，**Agentic RAG 是"用一个新的非确定性组件去治理另一个非确定性流程"——收益真实存在，但必须配评估基线：没有对标准 RAG 的量化对比，就无法证明这层 Agent 是在增值还是在添乱。**

### 何时使用 · Rule of Thumb（原文）

> Use this pattern when you need an LLM to answer questions or generate content based on specific, up-to-date, or proprietary information that was not part of its original training data. It is ideal for building Q&A systems over internal documents, customer support bots, and applications requiring verifiable, fact-based responses with citations.

### 🆕 2026 视角补充 · RAG 作为幻觉治理的第一道防线

《AI Design》（2026）第 10 章在讨论 Transformer"编造事实"问题（"Making Stuff Up" Problem）时，把 RAG 列为治理幻觉的首选手段：

> Look Outside for Data (RAG or Retrieval Augmented Generation): The AI can be taught to dig up facts from reliable places, like a legal database or medical books, before writing its answer. It then uses those real, found facts to build its final response, which drastically cuts down on it inventing things (this made-up text is often called "hallucinations").

**中文提炼**：让 AI 在作答前先从可靠来源（法律数据库、医学文献）挖取事实，再基于这些真实找到的事实构建最终回答——大幅削减编造（幻觉）。值得注意的是 2026 书给出的幻觉治理组合拳排序：RAG 找外部事实 → 人类专家核查（HITL，见 Pattern 13）→ 置信度分数与 AI 生成警示 → 用更高质量的事实数据持续训练。**RAG 与 HITL 在这份清单里是互补关系而非替代关系——检索解决"有据可依"，人工核查解决"依据是否被正确使用"。**（原稿定位：2026 书 Chapter 10，全文 5501-5514 行。）

### 📍 2026 现状对照

**（编辑判断，非原书内容）**RAG 在 2026 年的讨论重心已从"要不要建"转向"怎么运营好"——检索质量评估（retrieval eval）、知识库新鲜度管理、以及本章 Agentic RAG 描述的推理层增强，都在向工程化标准演进。同时"长上下文是否杀死 RAG"的争论有了较清晰的收敛方向：两者互补——长上下文降低了 chunking 的精度压力，但企业级知识规模（GB 到 TB 级）、权限隔离、成本控制仍然需要检索层。这与 Pattern 8 中"长上下文不取代长期记忆"是同一逻辑。此段为编辑判断，不作具体行业数据断言。

---

<aside class="not-prose my-10 px-6 py-6 bg-accent-ink text-white rounded">
<h3 class="text-base font-bold tracking-wide uppercase mb-3">📋 第二组小结 · 七个模式的决策关系</h3>
<p class="text-[15px] leading-relaxed mb-3 text-accent-gray-200">第一组解决"控制流"（任务怎么拆、怎么走），第二组解决"状态与知识"（Agent 记什么、学什么、知什么、错了怎么办、人在哪里介入）。评审 Agent 方案时，这七个模式对应七个必答题：</p>
<ol class="space-y-2 text-[15px] leading-relaxed list-decimal pl-5 text-accent-gray-100">
<li><strong>记忆怎么分层（Pattern 8）</strong>——短期靠上下文窗口管理，长期靠外部存储 + 语义检索；状态写入必须事件化、可追溯。长上下文不是记忆系统的替代品。</li>
<li><strong>学习停在哪一层（Pattern 9）</strong>——提示层（few-shot / 记忆召回）够用就别碰权重层；代码级自改必须配独立 overseer + 沙箱 + 可观测，三缺一不可。</li>
<li><strong>工具走协议还是硬编码（Pattern 10）</strong>——工具多、变化快、要跨团队复用就上 MCP；但先做 API 的 Agent 就绪度改造——Agent 需要更强的确定性支撑，不是更少。</li>
<li><strong>目标谁来裁决（Pattern 11）</strong>——目标要 SMART，裁判必须独立于执行者，能用确定性验证（测试 / 指标）就不用 LLM 口头判定，循环必须有硬上限。</li>
<li><strong>失败了怎么办（Pattern 12）</strong>——检测 / 处理 / 恢复三阶段分别设计；Agent 特有的"语义失败"（格式对、内容错）要纳入监控面；不可逆操作先想好回滚。</li>
<li><strong>人在哪里介入（Pattern 13）</strong>——按风险分级：高危不可逆操作 in-the-loop 逐案审批，高频规则化决策 on-the-loop 政策约束；升级协议要显式写死，HITL 是要预算的人力生产线。</li>
<li><strong>知识从哪来（Pattern 14）</strong>——先打好标准 RAG 的数据工程地基（chunking / 混合检索 / 库同步），跨文档关系推理再看 GraphRAG，检索质量治理再看 Agentic RAG——每升一级都是复杂度与成本的跃升。</li>
</ol>
</aside>

---

# 第三组 · 协同与治理模式（Pattern 15-21）

如果说 A 组（1-7）解决的是单个 Agent 的控制流、B 组（8-14）解决的是认知与状态，那么 C 组回答的是**系统级问题**：多个 Agent 之间怎么通信（15）、算力和成本怎么控（16）、推理深度怎么换取答案质量（17）、安全边界怎么设（18）、上线之后怎么评估和监控（19）、任务多了怎么排优先级（20）、以及怎么让 Agent 主动探索未知（21）。这七个模式是 Agent 项目从 Demo 走向生产、从单体走向平台时绕不开的词汇表。

---
## Pattern 15 · Inter-Agent Communication（A2A · 跨框架智能体通信）

<aside class="not-prose my-6 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-sm font-bold text-accent-purple tracking-wide uppercase mb-3">📌 管理者速读</h3>
<p class="text-[15px] text-accent-gray-800 leading-relaxed mb-2"><strong>解决什么问题：</strong>单个 Agent 再强也有能力边界，而现实中不同团队、不同供应商的 Agent 往往构建在不同框架上（LangGraph、CrewAI、Google ADK……），彼此没有共同语言。没有标准化协议，整合这些异构 Agent 的成本高、周期长，也做不出真正的多智能体系统。A2A（Agent2Agent）就是为此设计的开放通信标准。</p>
<p class="text-[15px] text-accent-gray-800 leading-relaxed mb-2"><strong>何时用：</strong>需要编排两个以上 Agent 协作、且它们可能来自不同框架时；需要动态发现并调用其他 Agent 能力时；企业内跨部门/跨供应商的 Agent 工作流编排。</p>
<p class="text-[15px] text-accent-gray-800 leading-relaxed"><strong>架构取舍：</strong>A2A 与 MCP 是互补而非竞争关系——MCP 解决"Agent 怎么接工具和数据"，A2A 解决"Agent 之间怎么协调和委派任务"。评审多 Agent 方案时，第一个该问的问题是：Agent 间通信是私有约定还是开放协议？私有约定短期快，但每新增一个异构 Agent，集成成本线性甚至超线性增长；协议化（Agent Card + 标准交互机制）把 M×N 的集成问题压成 M+N。代价是要接受协议栈的复杂度：任务状态机、多种交互模式、鉴权与审计都要按标准来。</p>
</aside>

### 模式定义 · Pattern Overview

> The Agent2Agent (A2A) protocol is an open standard designed to enable communication and collaboration between different AI agent frameworks. It ensures interoperability, allowing AI agents developed with technologies like LangGraph, CrewAI, or Google ADK to work together regardless of their origin or framework differences.

**中文提炼**：A2A 是一个开放标准，让不同框架构建的 AI Agent 能够互相通信与协作——不管它出身 LangGraph、CrewAI 还是 Google ADK，都能互操作。

原书特别列举了协议的产业支持面：Atlassian、Box、LangChain、MongoDB、Salesforce、SAP、ServiceNow 等公司参与支持，Microsoft 计划将 A2A 集成进 Azure AI Foundry 和 Copilot Studio，Auth0 与 SAP 也在向自家平台集成 A2A 支持（以上为原书成稿时的表述）。

### 核心结构 · Core Concepts

原书把 A2A 的支柱概念归为六块——核心角色、Agent Card、Agent 发现、通信与任务、交互机制、安全。

**① 三个核心角色**：User（发起请求的用户）、A2A Client（代表用户请求动作或信息的客户端 Agent）、A2A Server（提供 HTTP 端点处理请求的远程 Agent）。原书强调远程 Agent 是"不透明"系统：

> The remote agent operates as an "opaque" system, meaning the client does not need to understand its internal operational details.

**中文提炼**：客户端无需理解远程 Agent 的内部实现细节——这是解耦的关键，Agent 之间只依赖声明的能力接口，不依赖实现。

**② Agent Card（数字身份卡）**：

> An agent's digital identity is defined by its Agent Card, usually a JSON file. This file contains key information for client interaction and automatic discovery, including the agent's identity, endpoint URL, and version. It also details supported capabilities like streaming or push notifications, specific skills, default input/output modes, and authentication requirements.

**中文提炼**：Agent Card 通常是一个 JSON 文件，定义了 Agent 的数字身份：名称、端点 URL、版本、支持的能力（流式/推送通知）、具体技能（skills）、默认输入输出模态和鉴权要求。原书给了一个 WeatherBot 的完整示例——它声明了 `get_current_weather` 和 `get_forecast` 两个技能，各带示例问法和标签。可以把 Agent Card 理解为 Agent 世界的"API 文档 + 服务注册信息"合体。

**③ Agent 发现的三条路径**：Well-Known URI（标准路径如 `/.well-known/agent.json`，适合公开可自动发现的场景）、Curated Registries（集中式注册目录，原书明确说这"适合需要集中管理和访问控制的企业环境"）、Direct Configuration（直接配置/私下共享，适合紧耦合私有系统）。

**④ 通信与任务**：

> In the A2A framework, communication is structured around asynchronous tasks, which represent the fundamental units of work for long-running processes. Each task is assigned a unique identifier and moves through a series of states—such as submitted, working, or completed—a design that supports parallel processing in complex operations.

**中文提炼**：A2A 的通信围绕**异步任务**组织——任务是长时间运行流程的基本工作单元，每个任务有唯一 ID，并在 submitted / working / completed 等状态间流转。消息（Message）携带元数据和内容分片（parts），任务产出叫工件（artifacts），可以增量流式返回。底层传输统一走 HTTP(S) + JSON-RPC 2.0，用服务端生成的 `contextId` 把相关任务串起来保持上下文。

**⑤ 四种交互机制**（按任务时长和实时性需求选择）：

- **同步请求/响应**：快速即时操作，一次请求一次完整应答。
- **异步轮询**：服务端先应答 "working" 状态 + 任务 ID，客户端稍后轮询直到 completed / failed。
- **流式更新（SSE）**：服务端到客户端的持久单向连接，持续推送状态变更和部分结果。
- **推送通知（Webhooks）**：超长任务场景，客户端注册回调 URL，任务状态显著变化时服务端主动推送。

原书强调 A2A 是**模态无关**的——这些交互模式不仅适用于文本，也适用于音频、视频等数据类型。

**⑥ 安全机制**：mTLS 加密与双向认证、全量审计日志（记录信息流、参与 Agent 和动作，用于问责与安全分析）、Agent Card 中显式声明鉴权要求、凭证走 HTTP 头传递（OAuth 2.0 token / API key，避免暴露在 URL 或消息体中）。

### A2A 与 MCP 的分工

> While MCP focuses on structuring context for agents and their interaction with external data and tools, A2A facilitates coordination and communication among agents, enabling task delegation and collaboration.

**中文提炼**：MCP 管"Agent 与外部数据和工具的交互"（纵向接入），A2A 管"Agent 之间的协调与通信"（横向协作），两者互补。原书 Key Takeaways 里再次强调这个分层：A2A 是管理 Agent 间任务和工作流的高层协议，MCP 是 LLM 对接外部资源的标准化接口。

### 适用场景与 Trade-off

原书给出的三类典型应用：**跨框架协作**（不同框架的 Agent 组成多智能体系统，各自专精问题的不同侧面）、**自动化工作流编排**（企业场景下 Agent 间委派任务：一个收集数据、一个分析、一个写报告）、**动态信息检索**（主 Agent 向专门的"数据获取 Agent"请求实时市场数据）。

Trade-off 层面值得注意：A2A 把 Agent 间协作从"代码级集成"提升为"协议级集成"，换来的是模块化与可扩展性，付出的是运维复杂度——任务状态管理、多种交互模式的支持、Agent Card 的发布与安全治理都是新增的工程面。对小规模、单框架、紧耦合的系统，直接函数调用或框架内子 Agent 机制（见 Pattern 7）更简单；A2A 的价值在**异构、跨组织边界、需要动态发现**的场景才充分显现。

### 何时使用 · Rule of Thumb（原文）

> Use this pattern when you need to orchestrate collaboration between two or more AI agents, especially if they are built using different frameworks (e.g., Google ADK, LangGraph, CrewAI). It is ideal for building complex, modular applications where specialized agents handle specific parts of a workflow, such as delegating data analysis to one agent and report generation to another. This pattern is also essential when an agent needs to dynamically discover and consume the capabilities of other agents to complete a task.

### 📍 2026 现状对照（编辑判断）

原书成稿于 2025 年，其中"Microsoft 计划集成""各公司支持"等表述反映的是当时的生态承诺。（编辑判断：A2A 协议的治理归属、版本演进与各厂商落地进度均属时效信息，原书未覆盖，引用前需按当期官方文档核实。）对管理者更有参考价值的判断是：**协议竞争的终局尚未到来，但"Agent 间互操作需要开放标准"这个方向已无争议**——评审多 Agent 平台方案时，把"是否遵循开放协议、锁定成本有多高"列为必答题，比赌某个具体协议胜出更稳妥。

---
## Pattern 16 · Resource-Aware Optimization（资源感知优化）

<aside class="not-prose my-6 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-sm font-bold text-accent-purple tracking-wide uppercase mb-3">📌 管理者速读</h3>
<p class="text-[15px] text-accent-gray-800 leading-relaxed mb-2"><strong>解决什么问题：</strong>LLM 应用又贵又慢，如果每个任务都用最强模型，就是在用最贵的方式解决最简单的问题。输出质量和资源消耗之间存在根本性 trade-off——没有动态管理策略，系统既不能适应任务复杂度的变化，也无法在预算和性能约束内运行。</p>
<p class="text-[15px] text-accent-gray-800 leading-relaxed mb-2"><strong>何时用：</strong>API 调用有严格预算约束、延迟敏感的实时应用、边缘设备等资源受限硬件、需要程序化平衡"回答质量 vs 运行成本"、以及不同步骤资源需求差异大的多步工作流。</p>
<p class="text-[15px] text-accent-gray-800 leading-relaxed"><strong>架构取舍：</strong>核心机制是 Router Agent 先给请求分级，再分发给合适档位的模型——简单问题走快而便宜的模型，复杂推理才上旗舰。这与 Pattern 2 的 Routing 是同一机制的不同用途：Routing 按"业务意图"分流，本模式按"成本/能力档位"分流。工程上要防两个坑：<strong>路由器本身也是成本</strong>（用 LLM 做分类每次都是一次调用，高频场景应考虑规则或小模型分类器）；<strong>错误分级的代价不对称</strong>——简单问题误送 Pro 模型只是浪费钱，复杂问题误送 Flash 模型则直接输出劣质结果，需要 Critique Agent 或抽样评估来闭环校正。</p>
</aside>

### 模式定义 · Pattern Overview

> Resource-Aware Optimization enables intelligent agents to dynamically monitor and manage computational, temporal, and financial resources during operation. This differs from simple planning, which primarily focuses on action sequencing. Resource-Aware Optimization requires agents to make decisions regarding action execution to achieve goals within specified resource budgets or to optimize efficiency.

**中文提炼**：资源感知优化让 Agent 在运行中动态监控和管理三类资源——计算、时间、资金。它与单纯的规划（Pattern 6，关注动作排序）不同：这里要求 Agent 在给定资源预算内决定"怎么执行"——在更准但更贵的模型与更快更便宜的模型之间选择，或者决定是多花算力换精细回答、还是快速返回粗略答案。

原书开篇给的例子很直白：金融分析师要一份"立等可取"的初步报告，Agent 就用快而便宜的模型快速总结趋势；同一个分析师要为关键投资决策做高精度预测、且预算和时间充裕，Agent 就调用更强但更慢的模型。

原书特别强调 **fallback（降级回退）机制**：

> A key strategy in this category is the fallback mechanism, which acts as a safeguard when a preferred model is unavailable due to being overloaded or throttled. To ensure graceful degradation, the system automatically switches to a default or more affordable model, maintaining service continuity instead of failing completely.

**中文提炼**：首选模型因过载或限流不可用时，系统自动切换到默认或更便宜的模型——优雅降级、维持服务连续性，而不是整体失败。这在企业生产环境是可用性设计的必选项，不是可选项。

### 核心结构 · Router + Critique 双 Agent 架构

原书给出的标准解法是双角色协作：

**① Router Agent（路由器）**：先对请求分类，再分发。最简单的实现按查询长度分（短的走 Flash、长的走 Pro），更成熟的实现用 LLM 或 ML 模型分析查询的语义复杂度。原书 OpenAI 实战示例给出了三分类法：`simple`（直接作答，走小模型）、`reasoning`（需要多步推理，走推理模型）、`internet_search`（需要时效信息，触发搜索再作答）——这个三分法在实际系统中很有代表性。

**② Critique Agent（评审器）**：

> While not directly managing the budget, the Critique Agent contributes to indirect budget management by identifying suboptimal routing choices, such as directing simple queries to a Pro model or complex queries to a Flash model, which leads to poor results. This informs adjustments that improve resource allocation and cost savings.

**中文提炼**：Critique Agent 不直接管预算，但通过识别次优路由（简单问题送了 Pro、复杂问题送了 Flash 导致结果差）间接参与预算管理，其反馈用于校正路由逻辑、改善资源分配。它同时承担自我修正（发现错误让作答 Agent 重写）和性能监控（追踪准确性、相关性指标）职能——这与 Pattern 4 Reflection 的 Producer-Critic 结构一脉相承。

**平台化的参照**：原书以 OpenRouter 为例说明这层能力可以下沉为基础设施——它提供两种机制：**Automated Model Selection**（`openrouter/auto`，按 prompt 内容自动选优化模型）和 **Sequential Model Fallback**（指定模型序列，主模型因服务不可用/限流/内容过滤失败时自动切到下一个，计费按实际完成计算的模型算）。

### 九种扩展优化技术

原书在动态模型切换之外列了一组资源优化的完整谱系（管理者可当 checklist 用）：

1. **Adaptive Tool Use & Selection**：按 API 成本、延迟、执行时间智能选工具。
2. **Contextual Pruning & Summarization**：裁剪与摘要交互历史，压 prompt token 数、降推理成本。
3. **Proactive Resource Prediction**：预测负载、提前分配资源、防瓶颈。
4. **Cost-Sensitive Exploration**：多 Agent 系统中把通信成本也纳入优化目标。
5. **Energy-Efficient Deployment**：边缘/限电环境的能耗优化。
6. **Parallelization & Distributed Computing Awareness**：跨机器分布计算负载。
7. **Learned Resource Allocation Policies**：靠反馈和指标持续学习优化分配策略。
8. **Graceful Degradation & Fallback**：资源严重受限时降级维持基本功能。
9. **Dynamic Model Switching**：本章主线，按任务复杂度切模型档位。

### 适用场景与 Trade-off

原书列举的实用场景：成本优化的 LLM 使用（按预算约束选大小模型）、延迟敏感操作（实时系统选快速推理路径）、能效（边缘设备省电）、服务可靠性 fallback、数据用量管理（取摘要而非全量下载省带宽）、自适应任务分配（多 Agent 按各自负载自领任务）。

Trade-off 的本质：**这个模式是在用架构复杂度换运行成本**。引入 Router + Critique 意味着多了两个需要维护、评估、迭代的组件，路由错误本身成为新的故障模式。规模小、调用量低的系统，直接全量用一个中档模型可能总成本更低；这个模式的 ROI 随调用量增长而放大——量大到一定程度后，它就从"优化项"变成"生存项"。

### 何时使用 · Rule of Thumb（原文）

> Use this pattern when operating under strict financial budgets for API calls or computational power, building latency-sensitive applications where quick response times are critical, deploying agents on resource-constrained hardware such as edge devices with limited battery life, programmatically balancing the trade-off between response quality and operational cost, and managing complex, multi-step workflows where different tasks have varying resource requirements.

### 📍 2026 现状对照（编辑判断）

这一章在 2026 年的重要性只增不减：随着推理模型（reasoning models）普及，"思考时间"本身成了新的可调资源档位——同一个模型可以设置不同推理深度，成本差可达数倍到数十倍（编辑判断：这是原书成稿后逐渐清晰的趋势，与 Pattern 17 的 Scaling Inference Law 讨论相衔接）。模型路由已成为 LLM 网关类产品的标配能力。评审时该问的问题：模型选择策略是散落在各业务 Agent 里，还是收敛在平台网关层统一治理？降级链路是否真实演练过（而不是只写在配置里）？

---
## Pattern 17 · Reasoning Techniques（推理技术）

<aside class="not-prose my-6 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-sm font-bold text-accent-purple tracking-wide uppercase mb-3">📌 管理者速读</h3>
<p class="text-[15px] text-accent-gray-800 leading-relaxed mb-2"><strong>解决什么问题：</strong>复杂问题一次性直答容易出错。本章是全书信息密度最高的一章，把 Agent 的"思考方式"做成显式、可审计的工程对象：CoT（想一步写一步）、ToT（多路径探索+回溯）、Self-Correction（自我评审迭代）、PALM（把计算卸载给代码执行）、ReAct（想-做-看循环）、CoD/GoD（多模型辩论）、RLVR（训练出会"深想"的推理模型），以及统摄这一切的 Scaling Inference Law。</p>
<p class="text-[15px] text-accent-gray-800 leading-relaxed mb-2"><strong>何时用：</strong>问题复杂到单次直答搞不定、需要拆解和多步逻辑、需要与外部工具/数据交互、需要战略规划与动态调整时；以及"展示推理过程"与答案本身同等重要的场景（审计、医疗、法律）。</p>
<p class="text-[15px] text-accent-gray-800 leading-relaxed"><strong>架构取舍：</strong>本章的统一杠杆是"给推理花更多算力换质量"——Scaling Inference Law 指出：<strong>小模型 + 更大的推理预算，有时能赢过大模型 + 简单生成</strong>。这颠覆了"越大越好"的直觉，也是成本工程的重要抓手（与 Pattern 16 直接联动）。代价同样明确：推理越深，延迟和 token 成本越高，且思考轨迹本身可能冗长跑偏。评审时的关键问题：哪些请求值得深推理、哪些直答即可？推理深度是否可配置、可观测、可计费？</p>
</aside>

### 模式定义 · Pattern Overview

> These techniques go beyond simple sequential operations, making the agent's internal reasoning explicit. This allows agents to break down problems, consider intermediate steps, and reach more robust and accurate conclusions. A core principle among these advanced methods is the allocation of increased computational resources during inference.

**中文提炼**：这些技术的共同点是把 Agent 的内部推理**显式化**——让它拆解问题、考虑中间步骤、得出更稳健准确的结论。核心原则是在**推理阶段（inference）分配更多算力**：不求一次快速通过，而是允许迭代精化、多路径探索、调用外部工具。

### 核心结构 · 技术谱系

**① Chain-of-Thought（CoT，思维链）**——基座技术：

> Instead of providing a direct answer, CoT prompts guide the model to generate a sequence of intermediate reasoning steps. This explicit breakdown allows LLMs to tackle complex problems by decomposing them into smaller, more manageable sub-problems.

**中文提炼**：CoT 引导模型生成一串中间推理步骤而非直接给答案，把难题拆成更小的子问题。实现方式包括 few-shot 示例演示逐步推理，或者干脆指示模型 "think step by step"。原书强调它对 Agent 的特殊意义：推理透明化使 Agent 的行为**更可靠、更可审计**——不只是准确率提升，还有出错时能定位到哪一步错了。

**② Tree-of-Thought（ToT，思维树）**——在 CoT 之上引入分支：模型在不同中间步骤上分叉形成树结构，支持**回溯、自我修正、探索替代方案**，在敲定答案前评估多条推理轨迹。适合需要战略规划与决策的任务。

**③ Self-Correction（自我修正）**：Agent 对自己生成的内容和中间思考做内部评审，识别歧义、信息缺口、不准确之处，迭代调整后再输出。原书用一个社交媒体文案的例子演示五步流程（理解原始需求 → 分析现有内容 → 找差距 → 提具体改进 → 重写），本质是**把质量控制内嵌进生成过程**——与 Pattern 4 Reflection 同源。

**④ Program-Aided Language Models（PALMs，程序辅助）**：

> PALMs offload complex calculations, logical operations, and data manipulation to a deterministic programming environment.

**中文提炼**：让 LLM 生成并执行代码（如 Python），把复杂计算、逻辑运算、数据操作卸载给**确定性的编程环境**——在 LLM 精度不稳的领域（算术、符号操作）用传统程序的强项补位，结果再转回自然语言。

**⑤ RLVR 与推理模型**——本章承前启后的关键段：

> The key innovation enabling these models is a training strategy called Reinforcement Learning from Verifiable Rewards (RLVR). By training the model on problems with known correct answers (like math or code), it learns through trial and error to generate effective, long-form reasoning.

**中文提炼**：标准 CoT 是"一条预定思路走到底"，不会按问题难度自适应。新一代"推理模型"则在回答前投入可变的"思考时间"，产出可达数千 token 的动态思维链，支持自我修正和回溯、难题多想易题少想。使能这一切的训练策略是 RLVR——在有标准答案的问题（数学、代码）上试错学习，无需人工逐步监督，最终产出的不只是答案而是展示规划、监控、评估能力的"推理轨迹"（reasoning trajectory）。

**⑥ ReAct（Reasoning + Acting）**——推理与行动的闭环：

> ReAct operates in an interleaved manner: the agent executes an action, observes the outcome, and incorporates this observation into subsequent reasoning. This iterative loop of “Thought, Action, Observation, Thought...” allows the agent to dynamically adapt its plan, correct errors, and achieve goals requiring multiple interactions with the environment.

**中文提炼**：ReAct 交替进行"思考 → 行动 → 观察"：想清楚下一步、执行工具调用（查数据库、算数、调 API）、观察结果、把观察纳入下一轮思考。相比线性 CoT，它能响应实时反馈、动态调整计划——这是几乎所有现代 Agent 运行时的核心循环。原书补充了一个实用细节：思考频率可调——知识密集型任务（如事实核查）每个动作都插入思考，动作密集型任务（如环境导航）可以更省着用。

**⑦ 多模型辩论：CoD 与 GoD**：CoD（Chain of Debates，Microsoft 提出的正式框架）让多个异构模型像"AI 评审会"一样互相出方案、批评、反驳，以集体智能提升准确性、降低偏差，形成透明可信的推理记录。GoD（Graph of Debates）更进一步把辩论建模为动态非线性网络——论点是节点、支持/反驳是边，结论不在序列末尾产生，而是从整个图中识别"论证最扎实的簇"。

**⑧ MASS（原书标注为可选进阶话题）**：多 Agent 系统的效果高度依赖两件事——单 Agent 的 prompt 质量和 Agent 间的交互拓扑。MASS 框架把这个设计问题自动化，三阶段交替优化：先做块级 prompt 优化（每个 Agent 先调好再组装）、再做工作流拓扑优化（用"增量影响力"加权搜索有效拓扑）、最后做全系统级 prompt 联合优化。其三条设计原则值得管理者直接记下：**先把单个 Agent 的 prompt 调优再组队；组合已被证明有影响力的拓扑而不是无约束乱搜；最后对整个工作流做联合优化处理 Agent 间依赖**。

### Scaling Inference Law · 本章的经济学基石

> A cornerstone of this law is the revelation that superior results can frequently be achieved from a comparatively smaller LLM by augmenting the computational investment at inference time.

**中文提炼**：与训练侧 scaling law（更多数据和训练算力 → 更好模型）不同，推理侧 scaling law 关注**生成答案时**的算力投入。核心发现：给较小的模型更多推理时算力（生成多个候选答案再择优、自洽性采样、更严格的内部校验），常常能得到更优结果——

> The law posits that a smaller model, when granted a more substantial "thinking budget" during inference, can occasionally surpass the performance of a much larger model that relies on a simpler, less computationally intensive generation process.

**中文提炼**：小模型 + 充足"思考预算"，有时能超过大模型 + 简单生成。这为 Agent 系统的部署决策提供了三维平衡框架：模型大小（内存/存储需求）、响应延迟（推理计算增加延迟，找性能增益与延迟的平衡点）、运营成本（大模型的电力与基础设施开销）。它把部署决策从"选多大的模型"升级为"在模型尺寸和思考预算之间找最优组合"。

**Deep Research 作为集大成应用**：原书把 Perplexity、Google Gemini、OpenAI ChatGPT 的深度研究功能归为一类——用户给 AI 一个复杂问题和一个"时间预算"（通常几分钟），AI 自主完成四步循环：初始多路搜索 → 阅读分析并识别缺口和矛盾 → 针对性追加搜索 → 多轮迭代后合成带引用的结构化报告。这正是"推理 + 工具 + 推理时算力"三者叠加的产品化形态（与第一组 Pattern 6 的 Deep Research 补充相呼应）。

### 适用场景与 Trade-off

原书列举：多跳问答（跨源整合+逻辑推演）、数学解题（拆步骤+代码执行精确计算）、代码调试与生成（解释理由+按测试结果迭代）、战略规划（跨选项/后果/前提推理，按实时反馈调整）、医疗诊断（系统评估症状/检验/病史，每步阐明推理）、法律分析（分析文书与判例、保持逻辑一致）。共同特征：**过程与答案同等重要**。

Trade-off：推理深度是一个连续可调的成本杠杆，不是免费午餐。深推理带来准确性、稳健性、可审计性；付出的是延迟、token 成本、以及超长思考轨迹自身跑偏的风险。工程上的正解不是"全局开最深推理"，而是与 Pattern 16 组合——按任务复杂度动态分配思考预算。

### 何时使用 · Rule of Thumb（原文）

> Use these reasoning techniques when a problem is too complex for a single-pass answer and requires decomposition, multi-step logic, interaction with external data sources or tools, or strategic planning and adaptation. They are ideal for tasks where showing the "work" or thought process is as important as the final answer.

### 📍 2026 现状对照（编辑判断）

本章是全书对 2026 年预判最准的一章：RLVR 训练的推理模型已成为各家旗舰的标准形态，"thinking budget"（推理深度档位）成了 API 的常规参数，Deep Research 类产品全面普及。值得管理者注意的新变化（编辑判断）：推理轨迹的**可见性**成了新议题——部分厂商出于安全和竞争考虑隐藏或摘要化思考过程，这与本章"推理显式化带来可审计性"的初衷形成张力；采购和合规评审时应确认推理过程的留存与审计能力。多模型辩论（CoD/GoD）在生产系统中仍属少数派——成本数倍于单模型，多用于高价值、低频、容错代价大的决策场景。

---
## Pattern 18 · Guardrails / Safety Patterns（护栏 / 安全模式）

<aside class="not-prose my-6 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-sm font-bold text-accent-purple tracking-wide uppercase mb-3">📌 管理者速读</h3>
<p class="text-[15px] text-accent-gray-800 leading-relaxed mb-2"><strong>解决什么问题：</strong>Agent 越自主，失控风险越大：有害/偏见/不实输出、jailbreak 对抗攻击、非预期行为——每一项都可能造成真实损害、用户信任流失和法律声誉风险。护栏是一层保护机制，引导 Agent 的行为与输出，拦截有害、偏见、跑题或其他不当响应。</p>
<p class="text-[15px] text-accent-gray-800 leading-relaxed mb-2"><strong>何时用：</strong>只要 Agent 的输出可能影响用户、系统或企业声誉就该上护栏——客服机器人、内容生成平台、金融/医疗/法律等敏感领域尤其关键。</p>
<p class="text-[15px] text-accent-gray-800 leading-relaxed"><strong>架构取舍：</strong>护栏不是单点方案，而是<strong>分层防御（layered defense）</strong>——输入校验、输出过滤、prompt 级行为约束、工具使用限制、外部审核 API、人工介入，多层叠加才有稳健防护。成本上的实用技巧：用一个轻量便宜的模型（如 Flash 级）做输入预筛和输出复核，把安全检查的成本压到主模型调用的零头。评审时的关键问题不是"有没有护栏"，而是：护栏覆盖了哪几层？jailbreak 检测在哪一层？误杀率（false positive）有没有度量？——过严的护栏会把正常请求也拦掉，那是另一种生产事故。</p>
</aside>

### 模式定义 · Pattern Overview

> Guardrails, also referred to as safety patterns, are crucial mechanisms that ensure intelligent agents operate safely, ethically, and as intended, particularly as these agents become more autonomous and integrated into critical systems. They serve as a protective layer, guiding the agent's behavior and output to prevent harmful, biased, irrelevant, or otherwise undesirable responses.

**中文提炼**：护栏（安全模式）确保 Agent 安全、合乎伦理、按预期运行——Agent 越自主、越深入关键系统，这层保护越重要。原书特别澄清定位：

> The primary aim of guardrails is not to restrict an agent's capabilities but to ensure its operation is robust, trustworthy, and beneficial.

**中文提炼**：护栏的目的不是限制 Agent 的能力，而是确保运行稳健、可信、有益。它既是安全措施也是引导机制——没有护栏的 AI 系统是无约束、不可预测、有潜在危险的。

### 核心结构 · 六个实施层

原书开篇即给出护栏的完整分层清单：

1. **Input Validation / Sanitization（输入校验/清洗）**：在 Agent 处理前过滤恶意内容。
2. **Output Filtering / Post-processing（输出过滤/后处理）**：分析生成内容中的毒性或偏见。
3. **Behavioral Constraints（Prompt 级行为约束）**：通过直接指令限定行为边界。
4. **Tool Use Restrictions（工具使用限制）**：限制 Agent 能调用什么。
5. **External Moderation APIs（外部审核 API）**：接入专门的内容审核服务。
6. **Human Oversight / Intervention（人工监督/介入）**：Human-in-the-Loop 机制（与 Pattern 13 衔接）。

原书还给出一个成本敏感的补充手段：

> To further mitigate these risks, a less computationally intensive model can be employed as a rapid, additional safeguard to pre-screen inputs or double-check the outputs of the primary model for policy violations.

**中文提炼**：用一个算力开销更小的模型做快速的额外保险——预筛输入、或复核主模型输出是否违反策略。这是"用便宜模型守护贵模型"的标准做法。

**Prompt 化的策略执行器**：原书用 CrewAI 示例展示了一种有代表性的实现——用专门的"策略执行 Agent"（低温度 + Flash 级模型）按结构化 prompt 对每条输入做合规评估，输出固定 JSON（`compliance_status` / `evaluation_summary` / `triggered_policies`），再用 Pydantic schema 做技术层校验。其策略指令覆盖四大类：指令颠覆（jailbreak，如"无视之前的规则"）、违禁内容（歧视仇恨/危险活动/色情/辱骂）、离题讨论（政治/宗教/敏感争议/代写作业）、品牌与竞对信息。值得注意的裁决协议设计：**证据确凿才判违规，模糊地带默认放行**（"If there is any ambiguity or uncertainty regarding a violation, default to 'compliant'"）——这是在安全性和可用性之间的一个明确取舍选择，方向相反的系统（模糊默认拦截）适合更高风险的场景。

**平台级安全能力**：Vertex AI 的多层方法包括：身份与授权、输入输出过滤、内嵌安全控制的工具设计、Gemini 内置安全特性（内容过滤器与系统指令）、通过回调校验模型和工具调用。原书给出的进阶清单：轻量模型做额外保险、隔离的代码执行环境、严格评估与监控、安全网络边界（如 VPC Service Controls），并且——

> Before implementing these, conduct a detailed risk assessment tailored to the agent's functionalities, domain, and deployment environment.

**中文提炼**：实施前先做与 Agent 功能、领域、部署环境匹配的详细风险评估。另一个易被忽略的点：模型生成的内容在展示到用户界面前要做清洗，防止浏览器端恶意代码执行。工具调用前回调（before_tool_callback）是一个值得记住的机制——在工具真正执行前校验参数（如比对会话中的用户 ID 与工具参数是否一致），不一致直接拦截，把安全检查插入 Agent 与工具之间。

### 工程可靠性 · Engineering Reliable Agents

本章后半段把话题从"内容安全"扩展到"系统可靠性"，核心论点：

> Building reliable AI agents requires us to apply the same rigor and best practices that govern traditional software engineering.

**中文提炼**：构建可靠的 Agent，需要的正是治理传统软件工程的那套严谨与最佳实践。Agent 不是全新物种，而是更需要成熟工程纪律的复杂系统。原书列了四条：

- **Checkpoint & Rollback**：Agent 管理复杂状态、可能跑偏，检查点相当于事务系统的 commit，回滚是容错机制——把错误恢复变成主动的质量保障策略（与 Pattern 12 异常处理衔接）。
- **模块化与关注点分离**：单体全能 Agent 脆弱难调试，正解是小而专的 Agent/工具协作（一个管检索、一个管分析、一个管用户沟通），可独立优化、更新、调试，还能并行处理。
- **结构化日志的可观测性**：不只看最终输出，要捕获完整"思考链"——调了哪些工具、收到什么数据、下一步的推理依据、决策置信度。
- **最小权限原则**：

> An agent should be granted the absolute minimum set of permissions required to perform its task. [...] This drastically limits the "blast radius" of potential errors or malicious exploits.

**中文提炼**：Agent 只授予完成任务所需的最小权限——总结公开新闻的 Agent 只该有新闻 API 权限，不该能读私有文件或碰其他公司系统。这样能大幅收窄错误或恶意利用的"爆炸半径"。

### 适用场景与 Trade-off

原书列举的应用域：客服机器人（拦截冒犯性语言、错误医疗/法律建议、跑题回复）、内容生成系统（合规、法律要求、伦理标准）、教育助手（防错误答案与偏见观点、遵循课程大纲）、法律研究助手（不提供确定性法律意见、引导咨询执业律师）、招聘与 HR 工具（过滤歧视性语言保证公平）、社媒内容审核、科研助手（防捏造数据与无依据结论）。

Trade-off 的核心是**安全性与可用性的双向误差**：护栏太松，有害内容漏过（false negative）；太紧，正常请求被误杀（false positive），用户体验和业务转化直接受损。原书的"模糊默认放行"协议是一种选择，反向选择同样合理——关键是这个阈值应该是**显式的、按场景风险定的、可度量可调的**，而不是隐含在某段 prompt 里没人知道。

### 何时使用 · Rule of Thumb（原文）

> Guardrails should be implemented in any application where an AI agent's output can impact users, systems, or business reputation. They are critical for autonomous agents in customer-facing roles (e.g., chatbots), content generation platforms, and systems handling sensitive information in fields like finance, healthcare, or legal research. Use them to enforce ethical guidelines, prevent the spread of misinformation, protect brand safety, and ensure legal and regulatory compliance.

### 📍 2026 现状对照（编辑判断）

护栏在 2026 年的显著变化是从"应用层自建"走向"多层供给"：模型厂商内置安全分类器、云平台提供托管护栏服务、开源生态有专门的 guardrail 框架——企业的问题从"怎么建"变成"各层怎么分工、责任怎么划"。另一个升温的议题是 **Agent 特有的攻击面**：间接提示注入（恶意指令藏在 Agent 读取的网页/文档/邮件里，而非用户输入）在 Agent 有工具和权限后破坏力远超传统 chatbot 场景——本章的工具调用回调、最小权限、爆炸半径思路正是应对这类威胁的基础，但具体防御手段仍在快速演进（编辑判断：此领域当期最佳实践更新很快，落地前应核对最新安全指南）。

---
## Pattern 19 · Evaluation and Monitoring（评估与监控）

<aside class="not-prose my-6 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-sm font-bold text-accent-purple tracking-wide uppercase mb-3">📌 管理者速读</h3>
<p class="text-[15px] text-accent-gray-800 leading-relaxed mb-2"><strong>解决什么问题：</strong>Agent 是概率性系统，传统软件的 pass/fail 测试不够用；上线后还会遇到数据漂移、意外交互、偏离目标等问题——性能会随时间退化而你不知道。本章讲的是对 Agent 的效果、效率、合规的<strong>持续外部度量</strong>：定义指标、建反馈回路、建报告系统。</p>
<p class="text-[15px] text-accent-gray-800 leading-relaxed mb-2"><strong>何时用：</strong>生产环境部署（实时性能与可靠性关键）、需要系统性对比 Agent 版本（A/B）、受监管或高风险领域（合规/安全/伦理审计）、性能可能随环境漂移退化、以及需要评估行为轨迹和主观质量（如"有帮助程度"）的场景。</p>
<p class="text-[15px] text-accent-gray-800 leading-relaxed"><strong>架构取舍：</strong>评估手段是一个三角：人工评估（最能捕捉细微行为，但贵、慢、难扩展）、LLM-as-a-Judge（一致、高效、可扩展，但可能漏看中间步骤、受评审模型能力上限约束）、自动化指标（可扩展、客观，但难以覆盖完整能力）。生产系统的正解是组合使用+分层触发：自动指标全量跑、LLM 评审抽样跑、人工评估处理边界案例和校准评审器本身。<strong>只评最终输出不够——轨迹（trajectory）评估才能发现"结果对但过程错"的隐患。</strong></p>
</aside>

### 模式定义 · Pattern Overview

> While Chapter 11 outlines goal setting and monitoring, and Chapter 17 addresses Reasoning mechanisms, this chapter focuses on the continuous, often external, measurement of an agent's effectiveness, efficiency, and compliance with requirements. This includes defining metrics, establishing feedback loops, and implementing reporting systems to ensure agent performance aligns with expectations in operational environments...

**中文提炼**：本章与 Pattern 11（目标设定与监控，Agent 内部的进度追踪）区分开：这里讲的是**持续的、通常是外部的**度量——效果、效率、合规三个维度，配套指标定义、反馈回路和报告系统，确保 Agent 在运行环境中的表现符合预期。

### 核心结构 · 从基础指标到轨迹评估

**① 基础指标层**：响应质量评估（事实正确性、流畅度、语法、是否贴合用户意图）、延迟监控、token 用量追踪（LLM 计费按 token 走，省 token 就是省运营成本，还能暴露 prompt 工程的改进空间）。原书特意用一个反面示例说明**朴素精确匹配的陷阱**："The capital of France is Paris." 和 "Paris is the capital of France." 语义完全相同，但字符串比对给 0 分。真实评估需要更高级的手段：字符串相似度（Levenshtein/Jaccard）、关键词分析、嵌入余弦相似度的语义比对、LLM-as-a-Judge，以及 RAG 专属指标（faithfulness / relevance）。另一个工程常识：延迟数据打印到控制台没用，要落到持久化系统——结构化日志、时序数据库、数据仓库或可观测平台。

**② LLM-as-a-Judge（模型评审）**：评估"有帮助程度"这类主观质量，超出了客观指标的能力。解法是让一个 LLM 按预定义评分量表（rubric）评审另一个 Agent 的输出。原书用"法律调研问卷质量评审"做示例：五维度评分（清晰精确 / 中立无偏 / 相关聚焦 / 完整性 / 受众适配，各 1-5 分），输出结构化 JSON（总分、理由、分维度反馈、疑虑清单、建议动作），低温度保证评审确定性。原书对该技术的定位很克制："Though in development, this technique shows promise for automating and scaling qualitative evaluations"——有前景，但仍在发展中。

**③ 轨迹评估（Agent Trajectories）**——本章最有 Agent 特色的部分：

> Standard code yields predictable pass/fail results, whereas agents operate probabilistically, necessitating qualitative assessment of both the final output and the agent's trajectory—the sequence of steps taken to reach a solution.

**中文提炼**：传统代码测试产出可预测的 pass/fail，Agent 是概率性运行的，必须同时定性评估**最终输出和轨迹**——即达成解的步骤序列。把 Agent 的实际动作序列与理想的 ground truth 轨迹比对，识别错误和低效。原书给出六种比对口径：精确匹配（完美复刻理想序列）、按序匹配（顺序对、允许多余步骤）、任意序匹配（动作对、顺序不限、允许多余步骤）、精确率（预测动作的相关性）、召回率（覆盖了多少必要动作）、单工具检查（是否调用了特定动作）。**选哪种取决于场景风险**：高风险场景可能要求精确匹配，宽松场景用按序/任意序即可。

工程配套：测试文件（JSON 单会话，适合开发期单元测试）与 evalset 文件（多会话长对话数据集，适合集成测试）两级评估资产。Google ADK 提供三种执行方式：web UI 交互评估、pytest 编程集成进 CI、命令行 `adk eval` 自动化跑批。

**④ 多 Agent 系统评估**：像评估团队项目——既看每个 Agent 的本职表现，也看整体协作。原书给出四个关键问题（各配了旅行规划的例子）：Agent 间是否有效协作（订完机票有没有把正确日期传给酒店 Agent）？是否制定并遵守了计划（酒店 Agent 有没有抢在机票确认前订房、有没有卡死在"找完美租车"上）？任务是否派给了对的 Agent（问天气该用实时数据的天气 Agent 而不是泛泛而谈的通用 Agent）？加 Agent 是否真的提升了整体表现（还是引入冲突拖慢系统——可扩展性问题）？

### 🆕 从 Agent 到"承包商"（Contractor）· 原书前瞻提案

本章末尾引入了一个前瞻性框架（原书注明出自 Agent Companion, gulli et al.）：从简单 Agent 演进到**"承包商"模式**——从概率性、常不可靠的系统，走向面向复杂高风险环境的更确定、可问责的系统。核心诊断：

> Today's common AI agents operate on brief, underspecified instructions, which makes them suitable for simple demonstrations but brittle in production, where ambiguity leads to failure.

**中文提炼**：今天常见的 Agent 靠简短、欠规范的指令运行，做 Demo 够用，进生产就脆——歧义直接导致失败。承包商模式用类似人类世界服务合同的方式，在用户与 AI 之间建立正式化关系，四大支柱：

1. **正式化合同（Formalized Contract）**：任务的单一可信源，远超一句 prompt——不是"分析上季度销售"，而是"20 页 PDF、分析 2025 Q1 欧洲市场销售、含 5 个指定数据可视化、对比 2024 Q1、基于所附供应链中断数据集做风险评估"，交付物、规格、数据源、工作范围、预期算力成本和完成时间全部显式定义，结果**客观可验证**。
2. **协商与反馈的动态生命周期**：合同不是静态命令而是对话起点——Agent 可以分析条款并协商（"指定的 XYZ 数据库无法访问，请提供凭证或批准替代公共数据库"），在执行前消除误解、标记歧义与风险。
3. **质量优先的迭代执行**：与低延迟 Agent 不同，承包商优先正确性——代码生成合同下，Agent 会生成多种算法方案、按合同定义的单元测试编译运行、按性能/安全/可读性打分，只提交通过全部验证的版本。
4. **通过子合同层级分解**：主承包商像项目经理一样把大目标拆成正式"子合同"（电商 App 拆成 UI/UX 设计、鉴权模块、数据库 schema、支付集成），每份子合同独立完整、可派给其他专门 Agent。

这个提案与本章主题的关系：合同的"可验证交付物"本质上是**把评估标准前置到任务定义里**——评估不再是事后度量，而是任务契约的一部分。原书亦在企业应用清单中提出对应的治理工具：AI "Contract" 作为管控 Agentic AI 的动态协议，编码目标、规则与控制。

### 适用场景与 Trade-off

原书列举：生产系统性能追踪（客服机器人的解决率、响应时间）、A/B 测试（并行比较不同版本/策略）、合规与安全审计（自动生成审计报告、由人或另一个 Agent 复核、触发 KPI 或告警）、漂移检测（输入分布变化导致的性能退化）、行为异常检测（错误、恶意攻击或涌现的非预期行为）、学习进度评估。

Trade-off：评估本身有成本——LLM-as-a-Judge 每次评审都是模型调用，全量评审可能比业务调用本身还贵；轨迹级 ground truth 的标注成本高、且环境变化后需要维护。务实的分层是：便宜的自动指标全量、贵的评审抽样、最贵的人工只做校准和仲裁。**评估体系自己也需要被评估**（评审器与人类判断的一致率），否则 LLM-as-a-Judge 的系统性偏差会静默污染所有下游决策。

### 何时使用 · Rule of Thumb（原文）

> Use this pattern when deploying agents in live, production environments where real-time performance and reliability are critical. Additionally, use it when needing to systematically compare different versions of an agent or its underlying models to drive improvements, and when operating in regulated or high-stakes domains requiring compliance, safety, and ethical audits.

### 📍 2026 现状对照（编辑判断）

Agent 评估在 2026 年已从"论文话题"变成"工程刚需"，可观测平台普遍加入了 trace 级的 Agent 轨迹视图，LLM-as-a-Judge 成为标准工装。但两个本章预见的问题仍未很好解决（编辑判断）：一是**多 Agent 协作质量的度量**依然缺少公认指标，各家自定义；二是评审模型的偏差校准（judge 偏爱某种风格、对自家模型输出打分偏高等）在学界持续有讨论。"承包商"提案中的合同化方向，与 2026 年业界对 Agent 任务规格化（明确交付物与验收标准再执行）的实践趋势方向一致——但完整的四支柱框架尚未见大规模产品化（编辑判断，需按当期实态核实）。

---
## Pattern 20 · Prioritization（优先级排序）

<aside class="not-prose my-6 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-sm font-bold text-accent-purple tracking-wide uppercase mb-3">📌 管理者速读</h3>
<p class="text-[15px] text-accent-gray-800 leading-relaxed mb-2"><strong>解决什么问题：</strong>复杂动态环境中，Agent 面对大量可选动作、相互冲突的目标和有限资源。没有明确的"下一步做什么"的决策流程，Agent 会效率低下、运行延误，甚至无法达成关键目标。优先级排序让 Agent 按重要性、紧迫性、依赖关系和既定标准评估并排序任务。</p>
<p class="text-[15px] text-accent-gray-800 leading-relaxed mb-2"><strong>何时用：</strong>Agentic 系统需要在资源约束下自主管理多个（常常冲突的）任务或目标、且要在动态环境中有效运转时。</p>
<p class="text-[15px] text-accent-gray-800 leading-relaxed"><strong>架构取舍：</strong>这是七个模式里概念最直白的一个，但工程含金量在两处：一是<strong>排序标准必须显式化</strong>——紧迫性、重要性、依赖、资源可用性、成本收益、用户偏好，这些标准藏在 prompt 里还是做成可配置规则，决定了系统行为是否可预测可审计；二是<strong>动态重排</strong>——环境一变（新的紧急事件、临近的 deadline）就要能调整优先级，这要求优先级不是任务创建时一次性打的标签，而是持续再评估的状态。评审时问：优先级冲突时的仲裁规则是什么？谁能覆盖 Agent 的排序（人工 override 路径）？</p>
</aside>

### 模式定义 · Pattern Overview

> The prioritization pattern addresses this issue by enabling agents to assess and rank tasks, objectives, or actions based on their significance, urgency, dependencies, and established criteria. This ensures the agents concentrate efforts on the most critical tasks, resulting in enhanced effectiveness and goal alignment.

**中文提炼**：优先级模式让 Agent 按显著性、紧迫性、依赖关系和既定标准评估并排序任务、目标或动作，确保精力集中在最关键的事情上，提升效果和目标对齐度。它在资源受限、时间有限、目标可能冲突的真实场景中尤其重要。

### 核心结构 · 四个基本要素

原书把 Agent 优先级排序拆成四个组成部分：

**① 标准定义（Criteria Definition）**：建立任务评估的规则或度量——**紧迫性**（时间敏感度）、**重要性**（对主目标的影响）、**依赖关系**（是否是其他任务的前置）、**资源可用性**（所需工具或信息是否就绪）、**成本/收益分析**（投入 vs 预期产出）、**用户偏好**（个性化 Agent 场景）。

**② 任务评估（Task Evaluation）**：按上述标准评估每个候选任务，方法从简单规则到复杂打分、再到 LLM 推理不等。

**③ 调度/选择逻辑（Scheduling or Selection Logic）**：基于评估结果选出最优下一步动作或任务序列的算法，可以用队列，也可以用高级规划组件。

**④ 动态重排（Dynamic Re-prioritization）**：

> Finally, dynamic re-prioritization allows the agent to modify priorities as circumstances change, such as the emergence of a new critical event or an approaching deadline, ensuring agent adaptability and responsiveness.

**中文提炼**：环境变化时（新的关键事件出现、deadline 临近）Agent 能修改优先级——这是保证适应性和响应性的关键，也是区分"静态排序"和"真正优先级管理"的分水岭。

**三个层级**：优先级排序可以发生在不同粒度——选总体目标（高层目标优先级）、排计划内步骤顺序（子任务优先级）、从可选项中挑下一个立即动作（动作选择）。原书类比人类团队管理：管理者综合所有成员的输入来排任务优先级。

**实现参考**：原书用 LangChain 做了一个项目经理 Agent 示例——系统 prompt 明确了操作规程（先建任务拿 ID → 分析请求中是否提及优先级或指派人 → "urgent/ASAP/critical" 映射为 P0 → 信息缺失时按默认规则处理：P1 + Worker A → 最后列全量任务确认状态），配四个工具（建任务/设优先级/派人/列任务），P0/P1/P2 三级。这个例子的可借鉴之处在于**把优先级判断规则写进系统 prompt 并给默认值兜底**——语义映射（"急"→P0）交给 LLM，但级别体系和兜底规则是确定性的。

### 适用场景与 Trade-off

原书列举的七个应用域：自动化客服（系统宕机报告优先于密码重置，高价值客户优先）、云计算资源调度（峰值时段优先关键应用、批处理挪到低谷时段省成本）、自动驾驶（刹车避撞永远优先于车道保持和省油）、金融交易（按行情、风险偏好、利润空间、实时新闻排交易优先级）、项目管理（按 deadline、依赖、团队可用性、战略重要性排任务）、网络安全（按威胁严重度、潜在影响、资产关键性排告警响应）、个人助理（按用户定义的重要性、临近 deadline、当前上下文管理日程和提醒）。

Trade-off：优先级标准之间本身会冲突（最紧急的不一定最重要、成本最低的不一定收益最高），需要显式的仲裁规则或权重；LLM 做优先级推理灵活但不确定，规则排序确定但僵硬——典型的混合方案是规则定框架、LLM 在框架内做语义判断（如上例）。另一个常被忽略的问题是**饥饿（starvation）**：永远排在后面的低优任务可能永远轮不到，需要老化机制（等待越久优先级越高）之类的公平性设计——这在传统调度系统是常识，Agent 系统同样适用。

### 何时使用 · Rule of Thumb（原文）

> Use the Prioritization pattern when an Agentic system must autonomously manage multiple, often conflicting, tasks or goals under resource constraints to operate effectively in a dynamic environment.

### 📍 2026 现状对照（编辑判断）

优先级排序在 2026 年的主要落点是**长时程自主 Agent**（跑数小时到数天的任务队列）和**多 Agent 编排层**（中枢调度器给子 Agent 派工时的排序决策）。与本章成书时相比，变化在于优先级决策越来越多地与 Pattern 16（资源感知）和 Pattern 11（目标监控）耦合成统一的调度层——单独讨论"优先级"的场景变少，作为调度系统一个维度的场景变多（编辑判断）。管理者视角的检查点不变：排序标准是否显式、冲突仲裁是否有规则、人工 override 是否随时可用。

---
## Pattern 21 · Exploration and Discovery（探索与发现）

<aside class="not-prose my-6 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-sm font-bold text-accent-purple tracking-wide uppercase mb-3">📌 管理者速读</h3>
<p class="text-[15px] text-accent-gray-800 leading-relaxed mb-2"><strong>解决什么问题：</strong>Agent 通常在预定义的知识和解空间内运行，面对开放式问题和"未知的未知"（unknown unknowns）无能为力。本模式让 Agent 从被动响应/已知空间内优化，转向<strong>主动探索</strong>：进入陌生领域、试验新方法、生成新知识——这是全书最后一个模式，也是"真正 agentic"的试金石。</p>
<p class="text-[15px] text-accent-gray-800 leading-relaxed mb-2"><strong>何时用：</strong>开放式、复杂或快速演变的领域，解空间未被完全定义时；需要生成新假设、新策略、新洞见的任务——科研、市场分析、创意内容；目标是发现"未知的未知"而非优化已知流程的场景。</p>
<p class="text-[15px] text-accent-gray-800 leading-relaxed"><strong>架构取舍：</strong>本章的两个参考系统（Google Co-Scientist、Agent Laboratory）给出了共同的架构答案：<strong>用多 Agent 分工模拟科学方法本身</strong>——生成、评审、排序、演化各设专职 Agent，配合"测试时算力扩展"迭代提升产出质量。管理者要看清它的定位：这是七个模式中离日常业务最远、算力最贵、验证周期最长的一个，其价值锚点是"加速人类专家的探索"而非"替代判断"——原书反复强调 scientist-in-the-loop。上马前先确认：产出的假设/洞见有没有可行的验证闭环？没有验证闭环的探索系统只是在批量生产未经检验的猜想。</p>
</aside>

### 模式定义 · Pattern Overview

> Exploration and discovery differ from reactive behaviors or optimization within a predefined solution space. Instead, they focus on agents proactively venturing into unfamiliar territories, experimenting with new approaches, and generating new knowledge or understanding.

**中文提炼**：探索与发现不同于被动响应或在预定义解空间内做优化——它关注 Agent 主动进入陌生领域、试验新方法、生成新知识或新理解。对运行在开放式、复杂或快速演变领域的 Agent 而言，静态知识和预编程方案不够用，这个模式强调 Agent **扩展自身理解与能力**的能力。

### 核心结构 · Google Co-Scientist 的六 Agent 架构

原书以 Google Research 的 AI co-scientist 为主案例——一个基于 Gemini 的"计算型科研协作者"，辅助人类科学家做假设生成、提案精化、实验设计。其架构是一个受监督 Agent 协调的多 Agent 框架（异步任务执行、算力弹性伸缩），六个专职 Agent 模拟科研协作的迭代过程：

- **Generation agent（生成）**：通过文献探索和模拟科学辩论产出初始假设。
- **Reflection agent（反思）**：扮演同行评审，批判性评估假设的正确性、新颖性和质量。
- **Ranking agent（排序）**：用基于 Elo 的锦标赛机制，通过模拟辩论比较、排序、筛选假设。
- **Evolution agent（演化）**：持续精化头部假设——简化概念、综合想法、探索非常规推理。
- **Proximity agent（邻近度）**：计算邻近图对相似想法聚类，辅助探索假设空间。
- **Meta-review agent（元评审）**：综合所有评审与辩论的洞见，识别共性模式并提供反馈，让系统持续自我改进。

整体循环是"generate, debate, and evolve"（生成、辩论、演化），镜像科学方法本身；系统还采用 **test-time compute scaling**——分配更多推理时算力来迭代提升输出质量（与 Pattern 17 的 Scaling Inference Law 直接呼应）。

**验证结果**（原书报告的数据，属该系统一手验证研究）：GPQA 困难"diamond set"上 top-1 准确率 78.4%，且内部 Elo 评分与结果准确率一致；跨 200+ 研究目标的分析显示测试时算力扩展持续提升假设质量；在 15 个挑战性问题上超过其他 SOTA 模型和人类专家的"最佳猜测"。端到端湿实验验证包括：AML（急性髓系白血病）药物再利用——提出的全新候选药 KIRA6（此前无 AML 预临床证据）经体外实验证实在临床相关浓度下抑制多个 AML 细胞系的肿瘤细胞活性；肝纤维化新表观遗传靶点经人类肝类器官实验验证；抗微生物耐药性课题上，系统两天内的最高排名假设复现了一个独立研究组**十余年研究**才得出的未发表实验发现（cf-PICIs 与多样噬菌体尾部相互作用以扩展宿主范围）。

**定位与局限**（原书如实列出）：

> The design philosophy behind the AI co-scientist emphasizes augmentation rather than complete automation of human research.

**中文提炼**：设计哲学是**增强而非完全自动化**人类研究——研究者通过自然语言与系统交互、提供反馈、贡献想法、引导探索方向（"scientist-in-the-loop"协作范式）。局限也很实在：知识受限于开放获取文献（付费墙后的关键先行工作可能缺失）；几乎拿不到阴性实验结果（很少发表但对资深科学家至关重要）；继承底层 LLM 的事实错误与幻觉风险。安全方面：研究目标输入即审、生成的假设也要过检，1,200 个对抗性研究目标的初步安全评估显示系统能稳健拒绝危险输入。

### Agent Laboratory · 自主研究工作流的开源参照

原书第二个案例是 Agent Laboratory（Samuel Schmidgall 开发，MIT License）——自主研究工作流框架，同样定位于"增强而非替代"人类科研。四个阶段：**文献综述**（LLM Agent 自主采集分析文献，从 arXiv 等外部库建立知识基座）→ **实验**（协作设计实验、准备数据、执行与分析，集成 Python 代码执行和 Hugging Face 模型访问，按实时结果迭代优化）→ **报告撰写**（综合实验发现与文献洞见，按学术惯例组织结构，LaTeX 排版）→ **知识共享**（AgentRxiv——自主研究 Agent 的去中心化仓库，让 Agent 能在彼此成果上累积推进）。

两个值得管理者留意的设计细节：

**① 三重评审机制**：系统用三个独立评审 Agent 从不同视角打分（一个盯实验洞见、一个盯领域影响力、一个盯新颖性），模拟人类评审的多面性；评审输出是结构化 JSON（含 Originality / Quality / Clarity / Significance 等 1-4 分项、1-10 总分、Accept/Reject 二元决定），把主观评审变成可解析、可统计的数据。

**② 学术层级式角色分工**：Professor Agent 定研究议程、派任务；PostDoc Agent 执行研究（能写和跑代码）；Reviewer Agents 做同行评审；SW Engineer Agent 指导 ML Engineer Agent 写数据准备代码——且 prompt 里明确要求"aim for simple code... not complex code"（简单直接优先）。这个层级镜像人类科研团队的组织方式，与 Pattern 7（多 Agent 协作）的层级拓扑一脉相承。

### 适用场景与 Trade-off

原书列举：科研自动化（设计运行实验、分析结果、形成新假设——新材料/候选药物/科学原理）、游戏与策略生成（探索博弈状态、发现涌现策略，如 AlphaGo）、市场研究与趋势捕捉（扫描社媒/新闻/报告等非结构化数据）、安全漏洞发现（探测系统或代码库找攻击面）、创意内容生成（探索风格/主题/数据的组合）、个性化教育（按学生进度和薄弱点排学习路径）。

Trade-off 的核心是**探索-利用权衡（exploration-exploitation dilemma）**——原书在参考文献中把它列为强化学习与不确定性决策的基础问题：花多少资源探索未知（可能颗粒无收）、花多少资源利用已知（可能错过更好的解）。落到企业语境：探索型 Agent 的产出是概率性的假设而非确定性的交付物，投入产出周期长、方差大，适合有真实验证管线（实验室、A/B 平台、安全测试环境）的组织；同时自主探索能力越强，越需要 Pattern 18 的护栏前置——原书 co-scientist 的输入输出双向安全审查就是范例。

### 何时使用 · Rule of Thumb（原文）

> Use the Exploration and Discovery pattern when operating in open-ended, complex, or rapidly evolving domains where the solution space is not fully defined. It is ideal for tasks requiring the generation of novel hypotheses, strategies, or insights, such as in scientific research, market analysis, and creative content generation. This pattern is essential when the objective is to uncover "unknown unknowns" rather than merely optimizing a known process.

### 📍 2026 现状对照（编辑判断）

"AI for Science"在 2026 年是资本与算力投入最集中的方向之一，多家机构推出了科研 Agent 产品或计划；本章描述的"生成-辩论-演化 + 湿实验验证"路线已被更多团队采用，但**端到端可复现的重大发现仍是个案而非常态**（编辑判断：具体进展属时效信息，引用前需按当期文献核实）。对非科研企业，本模式更现实的映射是：竞争情报与市场扫描、安全红队自动化、产品创意的批量生成与筛选——共同点是都需要一个"便宜且快的验证闭环"来消化 Agent 产出的假设。没有闭环，先别上这个模式。

---

<aside class="not-prose my-10 px-6 py-6 bg-accent-ink text-white rounded">
<h3 class="text-base font-bold tracking-wide uppercase mb-3">📋 第三组小结 · 七个模式的内在联系</h3>
<p class="text-[15px] leading-relaxed text-accent-gray-200">C 组七个模式的内在联系：15（A2A）解决多 Agent 的通信基础设施，20（Prioritization）解决多任务的排序调度，16（Resource-Aware）+ 17（Reasoning/Scaling Inference Law）构成"质量-成本"的双向调节旋钮，18（Guardrails）划定安全边界，19（Evaluation）提供持续度量与改进闭环，21（Exploration）是在前面所有能力齐备后，Agent 才有资格触碰的"主动生成新知识"。从架构评审视角：15/18/19 是生产系统的必答题，16/20 是规模化后的成本题，17 是能力上限题，21 是战略选择题。</p>
</aside>

> **📌 全书完**：21 个模式（三组：基础编排 / 认知与状态 / 协同与治理）已全部上线。英文引文逐字摘自原书，出处与核验记录随内部台账留存；🆕 2026 视角补充与 📍 2026 现状对照均为编辑增补，非原书内容。
