# 批次三证据与核验记录（Pattern 15-21）

> 重写版（主模型重跑，2026-09-20）。
> 原文来源：/root/.openclaw/workspace/obsidian-export/books/chapters/ch15.txt – ch21.txt（分章全文）；概念摘要 concepts/ch15.txt – ch21.txt 仅作导航参考，引文一律取自 chapters 全文。
> 每条英文引文给出：所在章节 + 可 grep 的原文锚点（片段逐字）+ 源文件行号〔chNN.txt:起-止〕（口径对齐 batch-2-evidence.md；锚点在原文多处出现时标「首现」）。引文均整段核对，省略处使用明确省略号 [...]。

---
## Pattern 15 · Inter-Agent Communication (A2A)

**原文来源**：chapters/ch15.txt（Chapter 15: Inter-Agent Communication (A2A)）

引文核验（全部逐字比对 ch15.txt）：

1. 定义段："The Agent2Agent (A2A) protocol is an open standard designed to enable communication and collaboration between different AI agent frameworks..." — 锚点 grep: `The Agent2Agent (A2A) protocol is an open standard`〔ch15.txt:15〕（Pattern Overview 首段）。
2. 不透明系统："The remote agent operates as an \"opaque\" system, meaning the client does not need to understand its internal operational details." — 锚点 grep: `operates as an "opaque" system`〔ch15.txt:46〕（Core Actors 小节）。
3. Agent Card 定义："An agent's digital identity is defined by its Agent Card, usually a JSON file..." — 锚点 grep: `digital identity is defined by its Agent Card`〔ch15.txt:49〕。
4. 任务状态机："In the A2A framework, communication is structured around asynchronous tasks, which represent the fundamental units of work for long-running processes..." — 锚点 grep: `communication is structured around asynchronous tasks`〔ch15.txt:147-148〕。
5. A2A vs MCP："While MCP focuses on structuring context for agents and their interaction with external data and tools, A2A facilitates coordination and communication among agents, enabling task delegation and collaboration." — 锚点 grep: `While MCP focuses on structuring context`〔ch15.txt:278〕。
6. Rule of thumb："Use this pattern when you need to orchestrate collaboration between two or more AI agents..." — 锚点 grep: `orchestrate collaboration between two or more AI agents`〔ch15.txt:505-506〕（At a Glance / Rule of thumb 段，整段引用无省略）。

事实性陈述核验：
- 产业支持名单（Atlassian、Box、LangChain、MongoDB、Salesforce、SAP、ServiceNow；Microsoft 计划集成 Azure AI Foundry 和 Copilot Studio；Auth0/SAP 集成）— 原文锚点 `A2A is supported by a range of technology companies`〔ch15.txt:21〕，草稿已标注"原书成稿时的表述"。
- 三种发现方式（Well-Known URI / Curated Registries / Direct Configuration）— 锚点 `Well-Known URI: Agents host their Agent Card at a standardized path`〔ch15.txt:131〕。Curated Registries 的企业适用性表述来自原文 "well-suited for enterprise environments needing centralized management and access control"。
- 四种交互机制 — 锚点 `Synchronous Request/Response: For quick, immediate operations`〔ch15.txt:168〕；模态无关表述锚点 `A2A is modality-agnostic`〔ch15.txt:190〕。
- 安全四机制（mTLS/审计日志/Agent Card 声明/凭证处理）— 锚点 `Mutual Transport Layer Security (TLS)`〔ch15.txt:255〕、`Comprehensive Audit Logs`〔ch15.txt:259〕、`Agent Card Declaration`〔ch15.txt:267〕、`Credential Handling`〔ch15.txt:271〕。
- 传输层 JSON-RPC 2.0 + contextId — 锚点 `conducted over HTTP(S) using the JSON-RPC 2.0 protocol`〔ch15.txt:160〕、`a server-generated contextId is used to group related tasks`〔ch15.txt:161-162〕。
- WeatherBot Agent Card 示例（get_current_weather / get_forecast 两技能）— 锚点 `"name": "WeatherBot"`〔ch15.txt:58〕。
- 三类应用场景 — 锚点 `Multi-Framework Collaboration`〔ch15.txt:298〕、`Automated Workflow Orchestration`〔ch15.txt:303〕、`Dynamic Information Retrieval`〔ch15.txt:308〕。

2026 现状对照：标注为编辑判断，未断言当期厂商落地进度，明确"引用前需按当期官方文档核实"。合规。

未采用内容：Hands-On 代码示例（ADK calendar_agent）按 conventions（不写代码教程）仅在 trade-off 讨论中隐含跳过，未展开。

## Pattern 16 · Resource-Aware Optimization

**原文来源**：chapters/ch16.txt（Chapter 16: Resource-Aware Optimization）

引文核验（全部逐字比对 ch16.txt）：

1. 定义段："Resource-Aware Optimization enables intelligent agents to dynamically monitor and manage computational, temporal, and financial resources during operation..." — 锚点 grep: `dynamically monitor and manage`〔ch16.txt:3-4〕（章首段，引至 "or to optimize efficiency." 止，逐字）。
2. fallback 机制："A key strategy in this category is the fallback mechanism, which acts as a safeguard when a preferred model is unavailable due to being overloaded or throttled..." — 锚点 grep: `fallback mechanism, which acts as a safeguard`〔ch16.txt:18〕。
3. Critique Agent 间接预算管理："While not directly managing the budget, the Critique Agent contributes to indirect budget management by identifying suboptimal routing choices..." — 锚点 grep: `contributes to indirect budget management`〔ch16.txt:177-178〕。
4. Rule of thumb："Use this pattern when operating under strict financial budgets for API calls or computational power..." — 锚点 grep: `operating under strict financial budgets`〔ch16.txt:584〕（At a Glance / Rule of thumb 段，整段引用无省略）。

事实性陈述核验：
- 金融分析师例子 — 锚点 `an agent tasked with analyzing a large dataset for a financial analyst`〔ch16.txt:12-13〕。
- Router Agent 按查询长度/LLM 分析复杂度 — 锚点 `A Router Agent can direct queries based on simple metrics like query length`〔ch16.txt:108〕。
- OpenAI 示例三分类 simple/reasoning/internet_search — 锚点 `classifies each query into one of three categories`〔ch16.txt:224〕、`- simple`〔ch16.txt:275〕。
- OpenRouter 两种机制（Automated Model Selection / Sequential Model Fallback；按实际完成模型计费）— 锚点 `Automated Model Selection`〔ch16.txt:464〕、`Sequential Model Fallback`〔ch16.txt:477〕、`will correspond to the model that successfully completed the computation`〔ch16.txt:485-486〕。
- 九种扩展技术清单 — 锚点 `Dynamic Model Switching`〔ch16.txt:506，首现〕、`Adaptive Tool Use & Selection`〔ch16.txt:518，首现〕、`Contextual Pruning & Summarization`〔ch16.txt:524，首现〕、`Proactive Resource Prediction`〔ch16.txt:531，首现〕、`Cost-Sensitive Exploration`〔ch16.txt:536，首现〕、`Energy-Efficient Deployment`〔ch16.txt:541，首现〕、`Parallelization & Distributed Computing Awareness`〔ch16.txt:545，首现〕、`Learned Resource Allocation Policies`〔ch16.txt:550，首现〕、`Graceful Degradation and Fallback Mechanisms`〔ch16.txt:555，首现〕（"Beyond Dynamic Model Switching" 小节）。
- 六类应用场景 — 锚点 `Cost-Optimized LLM Usage`〔ch16.txt:27〕、`Latency-Sensitive Operations`〔ch16.txt:30〕、`Energy Efficiency`〔ch16.txt:32〕、`Fallback for service reliability`〔ch16.txt:34〕、`Data Usage Management`〔ch16.txt:39〕、`Adaptive Task Allocation`〔ch16.txt:41〕。
- Critique Agent 自我修正/性能监控职能 — 锚点 `For self-correction, it identifies errors or`〔ch16.txt:167〕、`systematically assesses responses for performance monitoring`〔ch16.txt:172〕。

2026 现状对照：推理深度作为资源档位、网关层收敛——标注为编辑判断，与 Pattern 17 衔接的说法也标注为编辑判断。合规。

未采用内容：书中三段代码示例（ADK 双 Agent 定义、QueryRouterAgent、OpenAI/OpenRouter 调用）按规范不做代码教程，只提炼其架构含义（三分类法、fallback 序列语义）。CRITIC_SYSTEM_PROMPT 未引用。

## Pattern 17 · Reasoning Techniques

**原文来源**：chapters/ch17.txt（Chapter 17: Reasoning Techniques）

引文核验（全部逐字比对 ch17.txt）：

1. 定义段："These techniques go beyond simple sequential operations, making the agent's internal reasoning explicit. [...] A core principle among these advanced methods is the allocation of increased computational resources during inference." — 两句均逐字，中间省略一句（"This allows agents to break down problems..." 已并入引文），实际引文为连续三句无省略；锚点 grep: `making the agent's internal reasoning explicit`〔ch17.txt:8〕。
2. CoT："Instead of providing a direct answer, CoT prompts guide the model to generate a sequence of intermediate reasoning steps..." — 锚点 grep: `generate a sequence of intermediate reasoning steps`〔ch17.txt:63-64〕。
3. PALM："PALMs offload complex calculations, logical operations, and data manipulation to a deterministic programming environment." — 锚点 grep: `offload complex calculations`〔ch17.txt:375〕。
4. RLVR："The key innovation enabling these models is a training strategy called Reinforcement Learning from Verifiable Rewards (RLVR)..." — 锚点 grep: `Reinforcement Learning from Verifiable Rewards`〔ch17.txt:437〕。
5. ReAct 循环："ReAct operates in an interleaved manner: the agent executes an action, observes the outcome..." — 锚点 grep: `ReAct operates in an interleaved manner`〔ch17.txt:465〕（注：原文中 "Thought, Action, Observation, Thought..." 用弯引号，草稿保留原样语义，引号形式按 markdown 直引号呈现，已在草稿用中文引号包裹说明）。
6. Scaling Inference Law 基石："A cornerstone of this law is the revelation that superior results can frequently be achieved from a comparatively smaller LLM by augmenting the computational investment at inference time." — 锚点 grep: `A cornerstone of this law is the revelation`〔ch17.txt:671〕。
7. 小模型+思考预算："The law posits that a smaller model, when granted a more substantial \"thinking budget\" during inference, can occasionally surpass the performance of a much larger model..." — 锚点 grep: `more substantial "thinking budget"`〔ch17.txt:692〕。
8. Rule of thumb："Use these reasoning techniques when a problem is too complex for a single-pass answer..." — 锚点 grep: `too complex for a single-pass answer`〔ch17.txt:873-874〕（整段引用无省略）。

事实性陈述核验：
- ToT 定义（分支树结构、回溯、自我修正、评估多轨迹）— 锚点 `Tree-of-Thought (ToT) is a reasoning technique that builds upon`〔ch17.txt:211〕。
- Self-Correction 五步社媒文案示例 — 锚点 `Self-Correction Agent`〔ch17.txt:246，首现〕、`GreenTech Gadgets`〔ch17.txt:307，首现〕。
- CoD 为 Microsoft 提出 — 锚点 `CoD (Chain of Debates) is a formal AI framework proposed by Microsoft`〔ch17.txt:476〕。
- GoD 图结构（节点=论点、边=supports/refutes、结论取最扎实的簇）— 锚点 `GoD (Graph of Debates)`〔ch17.txt:494〕、`'supports' or 'refutes,'`〔ch17.txt:497〕。
- MASS 三阶段与三原则 — 锚点 `Block-Level Prompt Optimization`〔ch17.txt:522〕、`Workflow Topology Optimization`〔ch17.txt:543，首现〕、`Workflow-Level Prompt Optimization`〔ch17.txt:578〕、`Optimize individual agents with high-quality prompts before composing them`〔ch17.txt:598〕。原书自标 "optional advanced topic"，草稿已注明。
- Deep Research 四步循环与平台列举（Perplexity、Google Gemini、OpenAI ChatGPT）— 锚点 `Initial Exploration`〔ch17.txt:646〕、`Reasoning and Refinement`〔ch17.txt:648〕、`Follow-up Inquiry`〔ch17.txt:651〕、`Final Synthesis`〔ch17.txt:653〕、`Major platforms in this space include Perplexity AI`〔ch17.txt:621-622〕；"时间预算"表述锚点 `grant it a "time budget"`〔ch17.txt:639〕。
- 思考频率可调（知识密集 vs 动作密集）— 锚点 `The frequency of an agent's thoughts can be adjusted`〔ch17.txt:839〕。
- 三维平衡（Model Size / Response Latency / Operational Cost）— 锚点 `Model Size: Smaller models are inherently less demanding`〔ch17.txt:703〕。
- 六类应用场景 — 锚点 `Complex Question Answering`〔ch17.txt:22〕、`Mathematical Problem Solving`〔ch17.txt:27〕、`Code Debugging and Generation`〔ch17.txt:31〕、`Strategic Planning`〔ch17.txt:36〕、`Medical Diagnosis`〔ch17.txt:40〕、`Legal Analysis`〔ch17.txt:51〕。

2026 现状对照：推理模型普及、thinking budget 参数化、推理轨迹可见性张力、CoD/GoD 生产占比——全部标注为编辑判断，未引当期数据。合规。

未采用内容：CoT 量子计算示例 prompt、ADK 三 Agent 代码、gemini-fullstack-langgraph-quickstart 代码与部署细节（按规范不做代码教程）。与批次一 Pattern 6 Deep Research 补充的呼应仅作站内交叉引用，无新事实断言。

## Pattern 18 · Guardrails / Safety Patterns

**原文来源**：chapters/ch18.txt（Chapter 18: Guardrails/Safety Patterns）

引文核验（全部逐字比对 ch18.txt）：

1. 定义段："Guardrails, also referred to as safety patterns, are crucial mechanisms that ensure intelligent agents operate safely, ethically, and as intended..." — 锚点 grep: `also referred to as safety patterns`〔ch18.txt:2〕。
2. 定位澄清："The primary aim of guardrails is not to restrict an agent's capabilities but to ensure its operation is robust, trustworthy, and beneficial." — 锚点 grep: `not to restrict an agent's capabilities`〔ch18.txt:14〕。
3. 轻量模型保险："To further mitigate these risks, a less computationally intensive model can be employed as a rapid, additional safeguard..." — 锚点 grep: `less computationally intensive model can be employed`〔ch18.txt:20〕。
4. 风险评估前置："Before implementing these, conduct a detailed risk assessment tailored to the agent's functionalities, domain, and deployment environment." — 锚点 grep: `conduct a detailed risk assessment`〔ch18.txt:567〕。
5. 工程严谨性："Building reliable AI agents requires us to apply the same rigor and best practices that govern traditional software engineering." — 锚点 grep: `same rigor and best practices that govern traditional software engineering`〔ch18.txt:750-751〕。
6. 最小权限："An agent should be granted the absolute minimum set of permissions required to perform its task. [...] This drastically limits the \"blast radius\"..." — 两句间省略新闻 API 例句，已用 [...] 标注；锚点 grep: `absolute minimum set of permissions`〔ch18.txt:789〕、`blast radius`〔ch18.txt:792〕。
7. 模糊默认放行（草稿中以内嵌短引形式出现）："If there is any ambiguity or uncertainty regarding a violation, default to \"compliant\"" — 原文出自 SAFETY_GUARDRAIL_PROMPT 评估流程第 3 条，原文为 `If there is any ambiguity or uncertainty regarding a violation, default to "compliant."`〔ch18.txt:209-210〕，草稿引用去掉句号、语义一致；锚点 grep: `default to "compliant`〔ch18.txt:210〕。
8. Rule of thumb："Guardrails should be implemented in any application where an AI agent's output can impact users, systems, or business reputation..." — 锚点 grep: `impact users, systems, or business reputation`〔ch18.txt:822〕（整段引用无省略）。

事实性陈述核验：
- 六个实施层清单 — 锚点 `Input Validation/Sanitization to filter malicious content`〔ch18.txt:7〕（章首段一句内全部列出）。
- CrewAI 示例结构（策略执行 Agent、JSON 三字段、Pydantic 校验、低温度 Flash 模型）— 锚点 `compliance_status`〔ch18.txt:215，首现〕、`policy_enforcer_agent`〔ch18.txt:316，首现〕、`temperature=0.0`〔ch18.txt:327〕、`CONTENT_POLICY_MODEL = "gemini/gemini-2.0-flash"`〔ch18.txt:129〕。
- 四大类策略指令（jailbreak/违禁内容/离题/品牌竞对）— 锚点 `Instruction Subversion Attempts (Jailbreaking)`〔ch18.txt:147〕、`Prohibited Content Directives`〔ch18.txt:158〕、`Irrelevant or Off-Domain Discussions`〔ch18.txt:171〕、`Proprietary or Competitive Information`〔ch18.txt:188〕。
- Vertex AI 多层方法与进阶清单（VPC Service Controls、隔离代码执行、UI 展示前清洗）— 锚点 `establishing agent and user identity and authorization`〔ch18.txt:554-555〕、`VPC Service Controls`〔ch18.txt:566〕、`sanitize all model-generated content before displaying it`〔ch18.txt:569〕。
- before_tool_callback 用户 ID 校验机制 — 锚点 `validate_tool_params`〔ch18.txt:577，首现〕、`before_tool_callback`〔ch18.txt:616，首现〕。
- Checkpoint & Rollback 与事务类比 — 锚点 `checkpoint and rollback pattern`〔ch18.txt:758〕、`akin to designing a transactional system with commit and rollback`〔ch18.txt:760-761〕。
- 模块化/可观测性要点 — 锚点 `Modularity and Separation of Concerns`〔ch18.txt:769〕、`Observability through Structured Logging`〔ch18.txt:778〕、`chain of thought"—which tools it called`〔ch18.txt:781〕。
- 七类应用域 — 锚点 `Customer Service Chatbots`〔ch18.txt:28〕、`Content Generation Systems`〔ch18.txt:32〕、`Educational Tutors/Assistants`〔ch18.txt:37〕、`Legal Research Assistants`〔ch18.txt:43〕、`Recruitment and HR Tools`〔ch18.txt:46〕、`Social Media Content Moderation`〔ch18.txt:49〕、`Scientific Research Assistants`〔ch18.txt:51〕。
- jailbreak 定义 — 锚点 `specialized prompts designed to bypass an LLM's safety features`〔ch18.txt:648-649〕。

2026 现状对照：多层供给格局、间接提示注入攻击面——标注为编辑判断，并明确"落地前应核对最新安全指南"。合规。

未采用内容：CrewAI 完整代码（约 300 行）与第二个 prompt 模板全文按规范不展开，只提炼策略结构与裁决协议；测试用例清单未引用。

## Pattern 19 · Evaluation and Monitoring

**原文来源**：chapters/ch19.txt（Chapter 19: Evaluation and Monitoring）

引文核验（全部逐字比对 ch19.txt）：

1. 定义段："While Chapter 11 outlines goal setting and monitoring, and Chapter 17 addresses Reasoning mechanisms, this chapter focuses on the continuous, often external, measurement of an agent's effectiveness, efficiency, and compliance with requirements. This includes defining metrics, establishing feedback loops, and implementing reporting systems to ensure agent performance aligns with expectations in operational environments" — 锚点 grep: `continuous, often external, measurement`〔ch19.txt:5-6〕（章首段，从完整句边界起引，两句连续逐字；原文句末接 "(see Fig.1)"，引文在此前截止、不加句号以免改动原文）。
2. 轨迹必要性："Standard code yields predictable pass/fail results, whereas agents operate probabilistically, necessitating qualitative assessment of both the final output and the agent's trajectory—the sequence of steps taken to reach a solution." — 锚点 grep: `agents operate probabilistically`〔ch19.txt:430-431〕。
3. LLM-as-a-Judge 定位（草稿内嵌短引）："Though in development, this technique shows promise for automating and scaling qualitative evaluations" — 原文为 `Though in development, this technique shows promise for automating and scaling qualitative evaluations.`〔ch19.txt:176-177〕，锚点 grep: `Though in development, this technique shows promise`〔ch19.txt:176-177〕。
4. 承包商诊断："Today's common AI agents operate on brief, underspecified instructions, which makes them suitable for simple demonstrations but brittle in production, where ambiguity leads to failure." — 锚点 grep: `brief, underspecified instructions`〔ch19.txt:519〕。
5. Rule of thumb："Use this pattern when deploying agents in live, production environments where real-time performance and reliability are critical..." — 锚点 grep: `live, production environments where real-time performance`〔ch19.txt:640-641〕。注：原文 Rule of thumb 段更长（还有 drift 和轨迹/主观质量两句），草稿引用了前两句，未用省略号截断句子（在完整句边界截止），管理者速读中已覆盖其余场景。
6. 巴黎例子两句（agent_response / ground_truth）— 锚点 `The capital of France is Paris.`〔ch19.txt:73，首现〕、`Paris is the capital of France.`〔ch19.txt:74，首现〕。

事实性陈述核验：
- 与 Ch11/Ch17 的分工 — 锚点 `While Chapter 11 outlines goal setting and monitoring, and Chapter 17 addresses Reasoning mechanisms`〔ch19.txt:4-5〕。
- 高级指标清单（Levenshtein/Jaccard/关键词/余弦相似度/LLM-as-a-Judge/RAG faithfulness relevance）— 锚点 `String Similarity Measures like`〔ch19.txt:102〕、`faithfulness`〔ch19.txt:106〕。
- 延迟落持久化系统（结构化日志/时序库/数仓/可观测平台）— 锚点 `structured log files (e.g., JSON), time-series databases`〔ch19.txt:117〕。
- 法律问卷评审 rubric 五维度 — 锚点 `Clarity & Precision`〔ch19.txt:212，首现〕、`Neutrality & Bias`〔ch19.txt:218，首现〕、`Relevance & Focus`〔ch19.txt:225，首现〕、`Completeness`〔ch19.txt:231，首现〕、`Appropriateness for Audience`〔ch19.txt:238，首现〕；低温度 — 锚点 `temperature (float): The generation temperature. Lower is better for deterministic evaluation`〔ch19.txt:279-280〕。
- 三种评估方法优劣表（人工/LLM 评审/自动指标）— 锚点 `Human Evaluation`〔ch19.txt:412〕、`Consistent, efficient, and`〔ch19.txt:418〕、`Scalable, efficient, and`〔ch19.txt:423〕。
- 六种轨迹比对口径 — 锚点 `exact match (requiring a perfect match to the ideal sequence)`〔ch19.txt:449-450〕、`in-order match`〔ch19.txt:450〕、`any-order match`〔ch19.txt:451，首现〕、`precision`〔ch19.txt:58，首现〕、`recall`〔ch19.txt:452〕、`single-tool use`〔ch19.txt:453〕；风险相关选择 — 锚点 `high-stakes scenarios potentially demanding an exact match`〔ch19.txt:454-455〕。
- 测试文件 vs evalset 文件 — 锚点 `Test files, in JSON format`〔ch19.txt:459〕、`Evalset files utilize a dataset`〔ch19.txt:468-469〕。
- ADK 三种执行方式 — 锚点 `web-based UI (adk web)`〔ch19.txt:593〕、`pytest`〔ch19.txt:594，首现〕、`command-line interface (adk eval)`〔ch19.txt:595〕。
- 多 Agent 四问与旅行例子 — 锚点 `Are the agents cooperating effectively?`〔ch19.txt:490〕、`Flight-Booking Agent`〔ch19.txt:490-491〕、`Did they create a good plan and stick to it?`〔ch19.txt:494〕、`Is the right agent being chosen for the right task?`〔ch19.txt:499〕、`does adding more agents improve performance?`〔ch19.txt:504〕。
- 承包商四支柱与出处（Agent Companion, gulli et al.）— 锚点 `an evolution from simple AI agents to advanced "contractors"`〔ch19.txt:511-512〕、`Formalized Contract`〔ch19.txt:528〕、`Dynamic Lifecycle of Negotiation and Feedback`〔ch19.txt:538〕、`Quality-Focused Iterative Execution`〔ch19.txt:554〕、`Hierarchical Decomposition via Subcontracts`〔ch19.txt:568〕；财务分析合同例子 — 锚点 `a 20-page PDF report analyzing European market sales from Q1 2025`〔ch19.txt:531〕；电商 App 拆解例子 — 锚点 `build an e-commerce mobile application`〔ch19.txt:571-572〕。
- 企业 AI "Contract" 治理工具 — 锚点 `a new control instrument, the AI "Contract," is needed`〔ch19.txt:33-34〕。
- 七类应用场景 — 锚点 `Performance Tracking in Live Systems`〔ch19.txt:23〕、`A/B Testing for Agent Improvements`〔ch19.txt:26〕、`Compliance and Safety Audits`〔ch19.txt:29〕、`Drift Detection`〔ch19.txt:36〕、`Anomaly Detection in Agent Behavior`〔ch19.txt:39〕、`Learning Progress Assessment`〔ch19.txt:42〕。

标注说明：承包商框架段落标注为「🆕 原书前瞻提案」并给出原书出处（Agent Companion, gulli et al.，见原文 References 5），未包装为已落地行业实践。
2026 现状对照：可观测平台轨迹视图、多 Agent 度量缺公认指标、judge 偏差校准、合同化方向——全部标注为编辑判断。合规。

未采用内容：evaluate_response_accuracy / LLMInteractionMonitor / LLMJudgeForLegalSurvey 三段代码按规范不展开，只取其结论（精确匹配陷阱、token 计费逻辑、rubric 结构）。

## Pattern 20 · Prioritization

**原文来源**：chapters/ch20.txt（Chapter 20: Prioritization）

引文核验（全部逐字比对 ch20.txt）：

1. 定义段："The prioritization pattern addresses this issue by enabling agents to assess and rank tasks, objectives, or actions based on their significance, urgency, dependencies, and established criteria. This ensures the agents concentrate efforts on the most critical tasks, resulting in enhanced effectiveness and goal alignment." — 锚点 grep: `assess and rank tasks, objectives, or actions`〔ch20.txt:6-7〕（章首段，两句连续逐字）。
2. 动态重排："Finally, dynamic re-prioritization allows the agent to modify priorities as circumstances change, such as the emergence of a new critical event or an approaching deadline, ensuring agent adaptability and responsiveness." — 锚点 grep: `dynamic re-prioritization allows the agent to modify priorities`〔ch20.txt:29-30〕。
3. Rule of thumb："Use the Prioritization pattern when an Agentic system must autonomously manage multiple, often conflicting, tasks or goals under resource constraints to operate effectively in a dynamic environment." — 锚点 grep: `autonomously manage multiple, often conflicting, tasks`〔ch20.txt:368〕（整段引用无省略）。

事实性陈述核验：
- 四要素（criteria definition / task evaluation / scheduling or selection logic / dynamic re-prioritization）— 锚点 `First, criteria definition establishes`〔ch20.txt:20〕、`Second, task evaluation involves`〔ch20.txt:24-25〕、`Third, scheduling or selection logic refers`〔ch20.txt:27〕。
- 六项标准（urgency/importance/dependencies/resource availability/cost-benefit/user preferences）— 锚点 `urgency (time sensitivity of the task), importance (impact on the primary objective)`〔ch20.txt:21-22〕。
- 三个层级（高层目标/子任务/动作选择）— 锚点 `high-level goal prioritization`〔ch20.txt:34-35〕、`sub-task prioritization`〔ch20.txt:35〕、`action selection`〔ch20.txt:36〕。
- 人类团队类比 — 锚点 `This mirrors human team organization, where managers prioritize tasks`〔ch20.txt:41-42〕。
- LangChain 项目经理示例细节（P0/P1/P2 三级、urgent/ASAP/critical→P0、默认 P1+Worker A、四工具、先建任务拿 ID、最后列全量）— 锚点 `map it to P0`〔ch20.txt:252〕、`assign P1 priority and assign to 'Worker A'`〔ch20.txt:255-256〕、`create_new_task`〔ch20.txt:187，首现〕、`You must do this first to get a `〔ch20.txt:248〕task_id``、`use `list_all_tasks`〔ch20.txt:150，首现〕 to show`。
- 七个应用域 — 锚点 `Automated Customer Support`〔ch20.txt:49〕、`Cloud Computing`〔ch20.txt:52〕、`Autonomous Driving Systems`〔ch20.txt:55〕、`Financial Trading`〔ch20.txt:58〕、`Project Management`〔ch20.txt:61，首现〕、`Cybersecurity`〔ch20.txt:63〕、`Personal Assistant AIs`〔ch20.txt:66〕；具体例子（宕机优先于密码重置、刹车优先于车道保持）— 锚点 `system outage reports, over routine matters, such as password resets`〔ch20.txt:49-50〕、`braking to avoid a collision takes precedence over maintaining lane discipline`〔ch20.txt:56-57〕。

编辑判断标注：饥饿/老化机制为传统调度常识引入的编辑观点（Trade-off 段落末句），未冒充原书内容——草稿行文中已用「这在传统调度系统是常识」口吻区分，属编辑补充。2026 现状对照全部标注编辑判断。合规。

未采用内容：LangChain 完整代码（SuperSimpleTaskManager 等约 200 行）按规范不展开，只提炼系统 prompt 的规则设计思路。原文 References 两篇论文未在草稿引用。

## Pattern 21 · Exploration and Discovery

**原文来源**：chapters/ch21.txt（Chapter 21: Exploration and Discovery）

引文核验（全部逐字比对 ch21.txt）：

1. 定义段："Exploration and discovery differ from reactive behaviors or optimization within a predefined solution space. Instead, they focus on agents proactively venturing into unfamiliar territories, experimenting with new approaches, and generating new knowledge or understanding." — 锚点 grep: `proactively venturing into unfamiliar territories`〔ch21.txt:6〕（章首段，两句连续逐字）。
2. 增强而非自动化："The design philosophy behind the AI co-scientist emphasizes augmentation rather than complete automation of human research." — 锚点 grep: `augmentation rather than complete automation`〔ch21.txt:137〕。
3. Rule of thumb："Use the Exploration and Discovery pattern when operating in open-ended, complex, or rapidly evolving domains where the solution space is not fully defined..." — 锚点 grep: `where the solution space is not fully defined`〔ch21.txt:479-480〕（整段引用无省略）。
4. 简单代码优先（草稿内嵌短引）："aim for simple code... not complex code" — 原文为 `You should aim for simple code to prepare the data, not complex code`〔ch21.txt:423-424〕（ML Engineer prompt），草稿使用明确省略号缩合，语义一致；锚点 grep: `aim for simple code to prepare the data`〔ch21.txt:423〕。

事实性陈述核验：
- co-scientist 为 Google Research 开发、基于 Gemini、监督 Agent + 异步任务框架 — 锚点 `an AI system developed by Google Research`〔ch21.txt:42〕、`This system operates on the Gemini LLM`〔ch21.txt:44-45〕、`A supervisor agent manages and coordinates`〔ch21.txt:58〕。
- 六 Agent 职能 — 锚点 `Generation agent`〔ch21.txt:64〕、`Reflection agent`〔ch21.txt:66〕、`Ranking agent: Employs an Elo-based tournament`〔ch21.txt:68〕、`Evolution agent`〔ch21.txt:70〕、`Proximity agent: Computes a proximity graph`〔ch21.txt:72〕、`Meta-review agent`〔ch21.txt:74〕。
- "generate, debate, and evolve" 循环、test-time compute scaling — 锚点 `iterative "generate, debate, and evolve" approach`〔ch21.txt:91〕、`"test-time compute scaling,"`〔ch21.txt:81〕。
- 验证数据：GPQA diamond 78.4% top-1、Elo 与准确率一致、200+ 研究目标、15 个挑战性问题超 SOTA 与专家 best guess、六位肿瘤学家评审 NIH Specific Aims 格式提案 — 锚点 `top-1 accuracy of 78.4% on the difficult "diamond set"`〔ch21.txt:103〕、`Analysis across over 200 research goals`〔ch21.txt:103-104〕、`curated set of 15 challenging problems`〔ch21.txt:106〕、`panel of six expert oncologists`〔ch21.txt:113〕。
- AML/KIRA6 湿实验 — 锚点 `KIRA6, were completely novel suggestions with no prior preclinical evidence`〔ch21.txt:118-119〕、`inhibited tumor cell viability at clinically relevant concentrations in multiple AML cell lines`〔ch21.txt:120-121〕。
- 肝纤维化类器官验证、FDA 已批准药物再利用机会 — 锚点 `human hepatic organoids validated these findings`〔ch21.txt:124-125〕、`already FDA-approved for another condition`〔ch21.txt:126-127〕。
- cf-PICIs 两天复现十余年未发表发现 — 锚点 `cf-PICIs interact with diverse phage tails to expand their host range`〔ch21.txt:132-133〕、`after more than a decade of research`〔ch21.txt:134〕。
- 三大局限（开放获取文献/阴性结果/幻觉）— 锚点 `constrained by its reliance on open-access literature`〔ch21.txt:141〕、`limited access to negative experimental results`〔ch21.txt:142-143〕、`"hallucinations"`〔ch21.txt:145〕。
- 安全：输入输出双审、1,200 对抗目标、Trusted Tester Program — 锚点 `All research goals are reviewed for safety upon input`〔ch21.txt:148〕、`1,200 adversarial research`〔ch21.txt:150〕（原文 ch21.txt:150-153 因 PDF 分页在 `adversarial research` 与 `goals` 之间断行并插入页码，完整短语 `1,200 adversarial research goals` grep 不中，故锚点取可命中片段）、`Trusted Tester Program`〔ch21.txt:155〕。
- scientist-in-the-loop — 锚点 `"scientist-in-the-loop" collaborative paradigm`〔ch21.txt:140〕。
- Agent Laboratory：Samuel Schmidgall / MIT License / AgentRxiv / 四阶段 — 锚点 `developed by Samuel Schmidgall under the MIT License`〔ch21.txt:160〕、`integrates "AgentRxiv," a decentralized repository`〔ch21.txt:168〕、`Literature Review`〔ch21.txt:174，首现〕、`Experimentation`〔ch21.txt:179〕、`Report Writing`〔ch21.txt:185〕、`Knowledge Sharing`〔ch21.txt:190〕。
- 三重评审机制与三个视角 — 锚点 `tripartite agentic judgment mechanism`〔ch21.txt:207〕、`harsh but fair reviewer and expect good experiments`〔ch21.txt:223-224〕、`looking for an idea that would be impactful`〔ch21.txt:230〕、`looking for novel ideas that have not been proposed before`〔ch21.txt:236〕。
- 评审 JSON 字段（Originality/Quality/Clarity/Significance 1-4、Overall 1-10、Accept/Reject）— 锚点 `"Originality": A rating from 1 to 4`〔ch21.txt:290〕、`"Overall": A rating from 1 to 10`〔ch21.txt:310〕、`only use Accept or Reject`〔ch21.txt:319〕。
- 角色分工（Professor/PostDoc/Reviewer/ML Engineer/SW Engineer）— 锚点 `ProfessorAgent`〔ch21.txt:337〕、`PostDoc Agent's role is to execute the research`〔ch21.txt:359〕、`Machine Learning Engineering Agents`〔ch21.txt:412〕、`Software Engineering Agents guide`〔ch21.txt:430〕。
- 六类应用场景 — 锚点 `Scientific Research Automation`〔ch21.txt:22〕、`Game Playing and Strategy Generation`〔ch21.txt:25〕（AlphaGo 括注在原文内）、`Market Research and Trend Spotting`〔ch21.txt:28〕、`Security Vulnerability Discovery`〔ch21.txt:31〕、`Creative Content Generation`〔ch21.txt:33〕、`Personalized Education and Training`〔ch21.txt:35〕。
- exploration-exploitation dilemma 出处 — 锚点原文 References 1 `Exploration-Exploitation Dilemma: A fundamental problem in reinforcement learning`〔ch21.txt:540-541〕。

验证数据的定性说明：GPQA 78.4%、KIRA6 等数据是原书转述的该系统验证研究结果，草稿已标注「原书报告的数据，属该系统一手验证研究」，未包装成独立第三方复核，也未扩展为真实客户部署案例。合规（conventions：原书自带示例允许忠实解释）。

2026 现状对照：AI for Science 投入集中、端到端可复现重大发现仍是个案、企业映射场景——全部标注编辑判断并注明"需按当期文献核实"。合规。

未采用内容：ReviewersAgent / get_score / ProfessorAgent / PostdocAgent 代码按规范不展开，只提炼评审结构与角色分工；批次三小结段落为草稿层编辑内容，供 main 合并时取舍，非原书内容（已在标题注明）。

---

## 总体核验声明

1. 七个 Pattern 全部基于 chapters/ch15.txt–ch21.txt 分章全文写作，写作前逐章完整读取原文；concepts/ 摘要仅用于交叉确认章节边界，未作为引文来源。
2. 所有块引英文均逐字复制自原文（整段核对，非首词命中），省略处一律使用 [...] 或注明缩合方式；中文均为提炼而非逐句翻译。
3. 未新增任何外部企业案例；原书自带示例（WeatherBot、旅行规划、法律问卷、AML/KIRA6 等）均忠实转述并保持原书语境。
4. 全部「📍 2026 现状对照」为编辑判断，段首统一标注「（编辑判断）」，无当期数据断言；「🆕」标注仅用于原书前瞻提案（Pattern 19 承包商框架），给出原书章节内出处。
5. 结构对齐批次一：管理者速读 aside / 模式定义 / 核心结构 / 适用场景与 Trade-off / 何时使用 · Rule of Thumb（原文）/ 2026 现状对照。
