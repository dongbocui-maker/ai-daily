<!-- 批次三草稿 · 第三组 · 协同与治理模式（Pattern 15-21） -->

> 草稿状态：重写版（主模型重跑，2026-09-20）。覆盖原书第 15–21 章。
> 结构对齐已上线批次一（Pattern 1–7）风格：管理者速读 / 模式定义 / 核心结构 / 适用场景与 Trade-off / 何时使用 · Rule of Thumb（原文）。
> 所有英文引文逐字来自 obsidian-export/books/chapters/ch15–21.txt；出处锚点见 batch-3-evidence.md。

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

**Deep Research 作为集大成应用**：原书把 Perplexity、Google Gemini、OpenAI ChatGPT 的深度研究功能归为一类——用户给 AI 一个复杂问题和一个"时间预算"（通常几分钟），AI 自主完成四步循环：初始多路搜索 → 阅读分析并识别缺口和矛盾 → 针对性追加搜索 → 多轮迭代后合成带引用的结构化报告。这正是"推理 + 工具 + 推理时算力"三者叠加的产品化形态（与批次一 Pattern 6 的 Deep Research 补充相呼应）。

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

## 附：批次三小结（草稿层，供合并时取舍）

C 组七个模式的内在联系：15（A2A）解决多 Agent 的通信基础设施，20（Prioritization）解决多任务的排序调度，16（Resource-Aware）+ 17（Reasoning/Scaling Inference Law）构成"质量-成本"的双向调节旋钮，18（Guardrails）划定安全边界，19（Evaluation）提供持续度量与改进闭环，21（Exploration）是在前面所有能力齐备后，Agent 才有资格触碰的"主动生成新知识"。从架构评审视角：15/18/19 是生产系统的必答题，16/20 是规模化后的成本题，17 是能力上限题，21 是战略选择题。

