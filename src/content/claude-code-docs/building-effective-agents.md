---
slug: anthropic-building-effective-agents
title: "Building Effective AI Agents"
subtitle: "Anthropic 官方 · Agent 架构领域被引用最多的实践文章 · Workflow First 原则的出处"
sourceUrl: "https://www.anthropic.com/engineering/building-effective-agents"
sourceLabel: "anthropic.com/engineering/building-effective-agents"
updated: "2026-08-28"
---

<aside class="not-prose my-8 px-6 py-6 bg-gradient-to-br from-accent-purple/10 to-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-base font-bold text-accent-purple tracking-wide uppercase mb-3">🎯 核心观点汇总（给忙人看的精华）</h3>
<ul class="space-y-2 text-[15px] text-accent-gray-800 leading-relaxed list-disc pl-5">
<li><strong>Workflow 和 Agent 是两种架构，不要混为一谈</strong>。Workflow = LLM 和工具沿开发者预定义的代码路径编排；Agent = LLM 自主决定流程和工具使用。这是全文最重要的概念区分。</li>
<li><strong>先找最简单的方案，只在必要时增加复杂度</strong>——这可能意味着根本不需要 agentic 系统。Agentic 系统用延迟和成本换任务表现，要先想清楚这笔交易划不划算。</li>
<li><strong>Workflow 优先（Workflow First）</strong>：任务定义清晰时，workflow 提供可预测性和一致性；只有当需要大规模的灵活性和模型驱动决策时，agent 才是更好的选择。多数应用场景下，优化单次 LLM 调用（配检索和示例）就够了。</li>
<li><strong>复杂度阶梯</strong>：增强型 LLM → Prompt Chaining → Routing → Parallelization → Orchestrator-Workers → Evaluator-Optimizer（以上全是 workflow）→ 最后才是 Autonomous Agent。逐级上，不跳级。</li>
<li><strong>Agent 的适用边界</strong>：开放式问题、步数无法预测、路径无法硬编码的场景。代价是更高的成本和错误累积（compounding errors）的风险——必须在沙箱里充分测试 + 配套 guardrails。</li>
<li><strong>慎用框架</strong>：Claude Agent SDK、Strands、Rivet、Vellum 等框架能加速起步，但额外抽象层会掩盖底层 prompt 和响应，增加调试难度，还会诱惑你过度设计。建议先直接用 LLM API，很多模式几行代码就能实现；用框架必须理解底层。</li>
<li><strong>三条实现原则</strong>：① 保持 agent 设计的简单性 ② 通过显式展示规划步骤保持透明 ③ 精心打磨 agent-computer interface（ACI，工具文档与测试）——SWE-bench 项目上花在工具优化上的时间比整体 prompt 还多。</li>
<li><strong>两个已验证的落地场景</strong>：客服（对话 + 工具 + 可量化的解决率）和编程（自动化测试提供天然反馈回路）。共同点：既需要对话又需要行动、成功标准清晰、有反馈回路、有人工监督。</li>
</ul>
</aside>

> **写在前面**：这篇文章发布于 2024 年 12 月，是 "workflow first, agent only when needed"（工作流优先，仅在必要时用 agent）理念的原始出处，也是企业级 Agent 架构讨论中被引用最多的官方文献。文首 Anthropic 补充说明：文中提到的工具生态已有变化，最新方法可参考 Claude Managed Agents 文档——但架构原则本身经受住了时间考验。

Note: Much of the tooling landscape described in this post has changed since December 2024. For our current approach, see [how we built Claude Managed Agents](https://www.anthropic.com/engineering/managed-agents) and the [Managed Agents documentation](https://platform.claude.com/docs/en/managed-agents/overview).

Over the past year, we've worked with dozens of teams building large language model (LLM) agents across industries. Consistently, the most successful implementations weren't using complex frameworks or specialized libraries. Instead, they were building with simple, composable patterns.

In this post, we share what we've learned from working with our customers and building agents ourselves, and give practical advice for developers on building effective agents.

---

<aside class="not-prose my-8 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-sm font-bold text-accent-purple tracking-wide uppercase mb-2">📌 章节导读 · 1. 什么是 Agent？</h3>
<p class="text-[15px] text-accent-gray-800 leading-relaxed">本节给出全文最核心的架构区分：<strong>Workflow（工作流）</strong>是 LLM 和工具通过预定义代码路径编排的系统；<strong>Agent（智能体）</strong>是 LLM 动态指挥自身流程和工具使用、自主掌控任务完成方式的系统。两者统称 agentic systems，但架构性质完全不同——这个区分是后文所有选型建议的基础。</p>
</aside>

## What are agents?

"Agent" can be defined in several ways. Some customers define agents as fully autonomous systems that operate independently over extended periods, using various tools to accomplish complex tasks. Others use the term to describe more prescriptive implementations that follow predefined workflows. At Anthropic, we categorize all these variations as agentic systems, but draw an important architectural distinction between workflows and agents:

- **Workflows** are systems where LLMs and tools are orchestrated through predefined code paths.
- **Agents**, on the other hand, are systems where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks.

Below, we will explore both types of agentic systems in detail. In Appendix 1 ("Agents in Practice"), we describe two domains where customers have found particular value in using these kinds of systems.

---

<aside class="not-prose my-8 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-sm font-bold text-accent-purple tracking-wide uppercase mb-2">📌 章节导读 · 2. 何时（不）使用 Agent</h3>
<p class="text-[15px] text-accent-gray-800 leading-relaxed">"Workflow First" 原则的原始出处就在本节。三层递进：① 先找最简单的方案——可能根本不用 agentic 系统；② 确需更多复杂度时，任务定义明确选 workflow（可预测、一致），需要灵活性和模型驱动决策才选 agent；③ 对多数应用而言，优化单次 LLM 调用 + 检索 + 上下文示例就已足够。Agentic 系统的本质是<strong>用延迟和成本换任务表现</strong>——先算清这笔账。</p>
</aside>

## When (and when not) to use agents

When building applications with LLMs, we recommend finding the simplest solution possible, and only increasing complexity when needed. This might mean not building agentic systems at all. Agentic systems often trade latency and cost for better task performance, and you should consider when this tradeoff makes sense.

When more complexity is warranted, workflows offer predictability and consistency for well-defined tasks, whereas agents are the better option when flexibility and model-driven decision-making are needed at scale. For many applications, however, optimizing single LLM calls with retrieval and in-context examples is usually enough.

---

<aside class="not-prose my-8 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-sm font-bold text-accent-purple tracking-wide uppercase mb-2">📌 章节导读 · 3. 何时以及如何使用框架</h3>
<p class="text-[15px] text-accent-gray-800 leading-relaxed">对 Claude Agent SDK、Strands、Rivet、Vellum 等框架的态度：<strong>能加速起步，但要警惕抽象税</strong>。框架的额外抽象层会掩盖底层 prompt 和响应、增加调试难度、诱导过度设计。Anthropic 的建议是先直接用 LLM API（很多模式几行代码即可实现）；如果用框架，必须理解底层实现——对框架内部机制的错误假设是客户侧最常见的错误来源。</p>
</aside>

## When and how to use frameworks

There are many frameworks that make agentic systems easier to implement, including:

- The [Claude Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview);
- [Strands Agents SDK by AWS](https://strandsagents.com/latest/);
- [Rivet](https://rivet.ironcladapp.com/), a drag and drop GUI LLM workflow builder; and
- [Vellum](https://www.vellum.ai/), another GUI tool for building and testing complex workflows.

These frameworks make it easy to get started by simplifying standard low-level tasks like calling LLMs, defining and parsing tools, and chaining calls together. However, they often create extra layers of abstraction that can obscure the underlying prompts and responses, making them harder to debug. They can also make it tempting to add complexity when a simpler setup would suffice.

We suggest that developers start by using LLM APIs directly: many patterns can be implemented in a few lines of code. If you do use a framework, ensure you understand the underlying code. Incorrect assumptions about what's under the hood are a common source of customer error.

See our [cookbook](https://platform.claude.com/cookbook/patterns-agents-basic-workflows) for some sample implementations.

---

<aside class="not-prose my-8 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-sm font-bold text-accent-purple tracking-wide uppercase mb-2">📌 章节导读 · 4. 构建块与五种 Workflow 模式</h3>
<p class="text-[15px] text-accent-gray-800 leading-relaxed">全文的方法论主体：从基础构建块 <strong>Augmented LLM</strong>（增强了检索、工具、记忆的 LLM）出发，按复杂度递增给出五种 workflow 模式——<strong>Prompt Chaining</strong>（任务串行分解，步骤间可加程序化检查门）、<strong>Routing</strong>(先分类再分流到专门化后续任务)、<strong>Parallelization</strong>（并行，分 Sectioning 切分子任务 和 Voting 多次投票两种）、<strong>Orchestrator-Workers</strong>（中心 LLM 动态拆解任务分派给 worker）、<strong>Evaluator-Optimizer</strong>（一个生成、一个评估反馈的循环）。每种模式都附「何时使用」判据和真实用例——这是给企业架构师的模式目录（pattern catalog），选型时逐条对照即可。</p>
</aside>

## Building blocks, workflows, and agents

In this section, we'll explore the common patterns for agentic systems we've seen in production. We'll start with our foundational building block—the augmented LLM—and progressively increase complexity, from simple compositional workflows to autonomous agents.

### Building block: The augmented LLM

The basic building block of agentic systems is an LLM enhanced with augmentations such as retrieval, tools, and memory. Our current models can actively use these capabilities—generating their own search queries, selecting appropriate tools, and determining what information to retain.

We recommend focusing on two key aspects of the implementation: tailoring these capabilities to your specific use case and ensuring they provide an easy, well-documented interface for your LLM. While there are many ways to implement these augmentations, one approach is through our recently released [Model Context Protocol](https://www.anthropic.com/news/model-context-protocol), which allows developers to integrate with a growing ecosystem of third-party tools with a simple client implementation.

For the remainder of this post, we'll assume each LLM call has access to these augmented capabilities.

### Workflow: Prompt chaining

Prompt chaining decomposes a task into a sequence of steps, where each LLM call processes the output of the previous one. You can add programmatic checks (see "gate" in the diagram below) on any intermediate steps to ensure that the process is still on track.

**When to use this workflow:** This workflow is ideal for situations where the task can be easily and cleanly decomposed into fixed subtasks. The main goal is to trade off latency for higher accuracy, by making each LLM call an easier task.

Examples where prompt chaining is useful:

- Generating Marketing copy, then translating it into a different language.
- Writing an outline of a document, checking that the outline meets certain criteria, then writing the document based on the outline.

### Workflow: Routing

Routing classifies an input and directs it to a specialized followup task. This workflow allows for separation of concerns, and building more specialized prompts. Without this workflow, optimizing for one kind of input can hurt performance on other inputs.

**When to use this workflow:** Routing works well for complex tasks where there are distinct categories that are better handled separately, and where classification can be handled accurately, either by an LLM or a more traditional classification model/algorithm.

Examples where routing is useful:

- Directing different types of customer service queries (general questions, refund requests, technical support) into different downstream processes, prompts, and tools.
- Routing easy/common questions to smaller, cost-efficient models like Claude Haiku 4.5 and hard/unusual questions to more capable models like Claude Sonnet 4.5 to optimize for best performance.

### Workflow: Parallelization

LLMs can sometimes work simultaneously on a task and have their outputs aggregated programmatically. This workflow, parallelization, manifests in two key variations:

- **Sectioning:** Breaking a task into independent subtasks run in parallel.
- **Voting:** Running the same task multiple times to get diverse outputs.

**When to use this workflow:** Parallelization is effective when the divided subtasks can be parallelized for speed, or when multiple perspectives or attempts are needed for higher confidence results. For complex tasks with multiple considerations, LLMs generally perform better when each consideration is handled by a separate LLM call, allowing focused attention on each specific aspect.

Examples where parallelization is useful:

- **Sectioning:**
  - Implementing guardrails where one model instance processes user queries while another screens them for inappropriate content or requests. This tends to perform better than having the same LLM call handle both guardrails and the core response.
  - Automating evals for evaluating LLM performance, where each LLM call evaluates a different aspect of the model's performance on a given prompt.
- **Voting:**
  - Reviewing a piece of code for vulnerabilities, where several different prompts review and flag the code if they find a problem.
  - Evaluating whether a given piece of content is inappropriate, with multiple prompts evaluating different aspects or requiring different vote thresholds to balance false positives and negatives.

### Workflow: Orchestrator-workers

In the orchestrator-workers workflow, a central LLM dynamically breaks down tasks, delegates them to worker LLMs, and synthesizes their results.

**When to use this workflow:** This workflow is well-suited for complex tasks where you can't predict the subtasks needed (in coding, for example, the number of files that need to be changed and the nature of the change in each file likely depend on the task). Whereas it's topographically similar, the key difference from parallelization is its flexibility—subtasks aren't pre-defined, but determined by the orchestrator based on the specific input.

Example where orchestrator-workers is useful:

- Coding products that make complex changes to multiple files each time.
- Search tasks that involve gathering and analyzing information from multiple sources for possible relevant information.

### Workflow: Evaluator-optimizer

In the evaluator-optimizer workflow, one LLM call generates a response while another provides evaluation and feedback in a loop.

**When to use this workflow:** This workflow is particularly effective when we have clear evaluation criteria, and when iterative refinement provides measurable value. The two signs of good fit are, first, that LLM responses can be demonstrably improved when a human articulates their feedback; and second, that the LLM can provide such feedback. This is analogous to the iterative writing process a human writer might go through when producing a polished document.

Examples where evaluator-optimizer is useful:

- Literary translation where there are nuances that the translator LLM might not capture initially, but where an evaluator LLM can provide useful critiques.
- Complex search tasks that require multiple rounds of searching and analysis to gather comprehensive information, where the evaluator decides whether further searches are warranted.

---

<aside class="not-prose my-8 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-sm font-bold text-accent-purple tracking-wide uppercase mb-2">📌 章节导读 · 5. Agents（自主智能体）</h3>
<p class="text-[15px] text-accent-gray-800 leading-relaxed">复杂度阶梯的最后一级。Agent 的实现通常很简单——<strong>就是 LLM 在循环里基于环境反馈使用工具</strong>，但适用条件严格：开放式问题、步数无法预测、路径无法硬编码，且你必须对模型决策有一定信任度。关键工程要点：每一步都要从环境获取 ground truth（工具结果/代码执行）评估进度、在 checkpoint 或遇阻时暂停等人类反馈、设置停止条件（如最大迭代数）保持控制。代价被明确点名：<strong>更高的成本 + 错误累积风险</strong>——务必沙箱充分测试并配 guardrails。这正是 IT 运营 / RCA 这类"根因不可穷举"场景的架构依据：诊断内核用 agent 循环，但必须包在确定性外壳里。</p>
</aside>

### Agents

Agents are emerging in production as LLMs mature in key capabilities—understanding complex inputs, engaging in reasoning and planning, using tools reliably, and recovering from errors. Agents begin their work with either a command from, or interactive discussion with, the human user. Once the task is clear, agents plan and operate independently, potentially returning to the human for further information or judgement. During execution, it's crucial for the agents to gain "ground truth" from the environment at each step (such as tool call results or code execution) to assess its progress. Agents can then pause for human feedback at checkpoints or when encountering blockers. The task often terminates upon completion, but it's also common to include stopping conditions (such as a maximum number of iterations) to maintain control.

Agents can handle sophisticated tasks, but their implementation is often straightforward. They are typically just LLMs using tools based on environmental feedback in a loop. It is therefore crucial to design toolsets and their documentation clearly and thoughtfully. We expand on best practices for tool development in Appendix 2 ("Prompt Engineering your Tools").

**When to use agents:** Agents can be used for open-ended problems where it's difficult or impossible to predict the required number of steps, and where you can't hardcode a fixed path. The LLM will potentially operate for many turns, and you must have some level of trust in its decision-making. Agents' autonomy makes them ideal for scaling tasks in trusted environments.

The autonomous nature of agents means higher costs, and the potential for compounding errors. We recommend extensive testing in sandboxed environments, along with the appropriate guardrails.

Examples where agents are useful (from our own implementations):

- A coding Agent to resolve [SWE-bench tasks](https://www.anthropic.com/research/swe-bench-sonnet), which involve edits to many files based on a task description;
- Our ["computer use" reference implementation](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo), where Claude uses a computer to accomplish tasks.

---

<aside class="not-prose my-8 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-sm font-bold text-accent-purple tracking-wide uppercase mb-2">📌 章节导读 · 6. 组合模式与总结</h3>
<p class="text-[15px] text-accent-gray-800 leading-relaxed">这些模式不是教条，而是可以组合、裁剪的通用形状。成功的关键是<strong>度量表现、持续迭代</strong>——只有在复杂度可证明地改善结果时才增加复杂度。总结提出实现 agent 的三条核心原则：① 保持设计简单 ② 显式展示 agent 的规划步骤以保持透明 ③ 通过完善的工具文档和测试打磨 agent-computer interface（ACI）。框架可以帮你快速起步，但走向生产时不要犹豫削减抽象层、用基础组件重建。</p>
</aside>

## Combining and customizing these patterns

These building blocks aren't prescriptive. They're common patterns that developers can shape and combine to fit different use cases. The key to success, as with any LLM features, is measuring performance and iterating on implementations. To repeat: you should consider adding complexity only when it demonstrably improves outcomes.

## Summary

Success in the LLM space isn't about building the most sophisticated system. It's about building the right system for your needs. Start with simple prompts, optimize them with comprehensive evaluation, and add multi-step agentic systems only when simpler solutions fall short.

When implementing agents, we try to follow three core principles:

1. Maintain **simplicity** in your agent's design.
2. Prioritize **transparency** by explicitly showing the agent's planning steps.
3. Carefully craft your agent-computer interface (ACI) through thorough tool **documentation and testing**.

Frameworks can help you get started quickly, but don't hesitate to reduce abstraction layers and build with basic components as you move to production. By following these principles, you can create agents that are not only powerful but also reliable, maintainable, and trusted by their users.

### Acknowledgements

Written by Erik S. and Barry Zhang. This work draws upon our experiences building agents at Anthropic and the valuable insights shared by our customers, for which we're deeply grateful.

---

<aside class="not-prose my-8 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-sm font-bold text-accent-purple tracking-wide uppercase mb-2">📌 章节导读 · 附录 1. Agent 落地实践（客服 + 编程）</h3>
<p class="text-[15px] text-accent-gray-800 leading-relaxed">两个已被客户验证的高价值场景。<strong>客服</strong>：对话流天然契合 + 工具可拉取客户数据/订单/知识库 + 退款等动作可程序化执行 + 解决率可量化——已有公司敢按"成功解决数"收费，说明对 agent 效果有信心。<strong>编程</strong>：自动化测试提供天然反馈回路 + 问题空间结构清晰 + 输出质量可客观度量。共同特征值得记住：<strong>既需对话又需行动、成功标准清晰、有反馈回路、有人工监督</strong>——评估自己场景适不适合 agent 时就对照这四条。</p>
</aside>

## Appendix 1: Agents in practice

Our work with customers has revealed two particularly promising applications for AI agents that demonstrate the practical value of the patterns discussed above. Both applications illustrate how agents add the most value for tasks that require both conversation and action, have clear success criteria, enable feedback loops, and integrate meaningful human oversight.

### A. Customer support

Customer support combines familiar chatbot interfaces with enhanced capabilities through tool integration. This is a natural fit for more open-ended agents because:

- Support interactions naturally follow a conversation flow while requiring access to external information and actions;
- Tools can be integrated to pull customer data, order history, and knowledge base articles;
- Actions such as issuing refunds or updating tickets can be handled programmatically; and
- Success can be clearly measured through user-defined resolutions.

Several companies have demonstrated the viability of this approach through usage-based pricing models that charge only for successful resolutions, showing confidence in their agents' effectiveness.

### B. Coding agents

The software development space has shown remarkable potential for LLM features, with capabilities evolving from code completion to autonomous problem-solving. Agents are particularly effective because:

- Code solutions are verifiable through automated tests;
- Agents can iterate on solutions using test results as feedback;
- The problem space is well-defined and structured; and
- Output quality can be measured objectively.

In our own implementation, agents can now solve real GitHub issues in the [SWE-bench Verified](https://www.anthropic.com/research/swe-bench-sonnet) benchmark based on the pull request description alone. However, whereas automated testing helps verify functionality, human review remains crucial for ensuring solutions align with broader system requirements.

---

<aside class="not-prose my-8 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-sm font-bold text-accent-purple tracking-wide uppercase mb-2">📌 章节导读 · 附录 2. 给工具做提示词工程（ACI）</h3>
<p class="text-[15px] text-accent-gray-800 leading-relaxed">很多人忽略的重点：<strong>工具定义值得和整体 prompt 同等的打磨投入</strong>。核心建议：给模型足够的"思考 token"避免把自己写进死角、格式贴近模型在互联网上自然见过的文本、消除格式开销（别让模型数行数或转义代码）。方法论类比：人机界面（HCI）投入多少设计精力，agent-computer interface（ACI）就该投入多少——包括写像给初级工程师看的 docstring、跑大量输入观察模型犯错、用 poka-yoke（防呆设计）改参数让错误更难发生。实证：Anthropic 做 SWE-bench 时在工具优化上花的时间比整体 prompt 还多，比如把相对路径改成强制绝对路径后模型错误消失。</p>
</aside>

## Appendix 2: Prompt engineering your tools

No matter which agentic system you're building, tools will likely be an important part of your agent. [Tools](https://www.anthropic.com/news/tool-use-ga) enable Claude to interact with external services and APIs by specifying their exact structure and definition in our API. When Claude responds, it will include a tool use block in the API response if it plans to invoke a tool. Tool definitions and specifications should be given just as much prompt engineering attention as your overall prompts. In this brief appendix, we describe how to prompt engineer your tools.

There are often several ways to specify the same action. For instance, you can specify a file edit by writing a diff, or by rewriting the entire file. For structured output, you can return code inside markdown or inside JSON. In software engineering, differences like these are cosmetic and can be converted losslessly from one to the other. However, some formats are much more difficult for an LLM to write than others. Writing a diff requires knowing how many lines are changing in the chunk header before the new code is written. Writing code inside JSON (compared to markdown) requires extra escaping of newlines and quotes.

Our suggestions for deciding on tool formats are the following:

- Give the model enough tokens to "think" before it writes itself into a corner.
- Keep the format close to what the model has seen naturally occurring in text on the internet.
- Make sure there's no formatting "overhead" such as having to keep an accurate count of thousands of lines of code, or string-escaping any code it writes.

One rule of thumb is to think about how much effort goes into human-computer interfaces (HCI), and plan to invest just as much effort in creating good agent-computer interfaces (ACI). Here are some thoughts on how to do so:

- **Put yourself in the model's shoes.** Is it obvious how to use this tool, based on the description and parameters, or would you need to think carefully about it? If so, then it's probably also true for the model. A good tool definition often includes example usage, edge cases, input format requirements, and clear boundaries from other tools.
- **How can you change parameter names or descriptions to make things more obvious?** Think of this as writing a great docstring for a junior developer on your team. This is especially important when using many similar tools.
- **Test how the model uses your tools:** Run many example inputs in our workbench to see what mistakes the model makes, and iterate.
- **[Poka-yoke](https://en.wikipedia.org/wiki/Poka-yoke) your tools.** Change the arguments so that it is harder to make mistakes.

While building our agent for SWE-bench, we actually spent more time optimizing our tools than the overall prompt. For example, we found that the model would make mistakes with tools using relative filepaths after the agent had moved out of the root directory. To fix this, we changed the tool to always require absolute filepaths—and we found that the model used this method flawlessly.
