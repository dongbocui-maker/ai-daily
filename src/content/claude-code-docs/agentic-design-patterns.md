---
slug: agentic-design-patterns
title: "Agentic Design Patterns · 21 个 Agent 设计模式精读"
subtitle: "Google Cloud CTO 办公室 Antonio Gulli · 482 页原著中英对照 · 管理者视角提炼：模式定义 / 适用场景 / 架构取舍 · 附两本原版 PDF"
sourceUrl: "https://link.springer.com/book/10.1007/978-3-032-01402-3"
sourceLabel: "Springer（2025-10-30 正式出版）"
updated: "2026-09-19"
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
| **A. 基础编排**（本批） | 1 Prompt Chaining · 2 Routing · 3 Parallelization · 4 Reflection · 5 Tool Use · 6 Planning · 7 Multi-Agent | 控制流问题：任务怎么拆、怎么走、怎么并行、怎么自查、怎么接外部世界 |
| **B. 认知与状态**（批次 2） | 8 Memory · 9 Learning & Adaptation · 10 MCP · 11 Goal Setting · 12 Exception Handling · 13 Human-in-the-Loop · 14 RAG | 状态问题：Agent 记什么、学什么、怎么接知识、出错怎么办、人在哪里介入 |
| **C. 协同与治理**（批次 3） | 15 A2A · 16 Resource-Aware · 17 Reasoning · 18 Guardrails · 19 Evaluation · 20 Prioritization · 21 Exploration | 系统问题：多 Agent 怎么通信、成本怎么控、怎么推理、怎么防护、怎么评估 |

> **一句话判断该不该往下读**：如果你正在或即将主导 Agent 类项目的架构评审，A 组的七个模式是评审时的最小词汇表——不掌握这七个，很难判断团队给出的方案是过度设计还是能力不足。

---

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

> **📌 批次说明**：以上为第一组「基础编排模式」（Pattern 1-7）。第二组「认知与状态」（Memory / Learning / MCP / Goal Setting / Exception Handling / Human-in-the-Loop / RAG）与第三组「协同与治理」（A2A / Resource-Aware / Reasoning / Guardrails / Evaluation / Prioritization / Exploration）将在同一页面内陆续补全。
