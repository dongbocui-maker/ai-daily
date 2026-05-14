---
order: 3
slug: architecture
docNum: "03 · 柱 1"
docColor: p1
title: "Agentic 架构与 Mesh"
feishuToken: Lr8Fd9uHlofhhuxLwipc9eTVn2b
words: "~14K 字"
---
# 柱 1：架构

> 本板块基于以下源：#01, #02, #03, #04, #05, #06, #07, #08, #09, #10, #12, #13, #14, #15, #16

## 一、核心观点

1. **企业架构必须从「静态 API + 确定性数据流」转向「Agentic Mesh + 动态编排」**。McKinsey 提出三组重写：①Systems built around fixed APIs and deterministic data flows are misaligned with agentic requirements；②Human-mediated handoffs become bottlenecks；③Governance models designed for predictable, sequential processes cannot audit machine-speed decisions at scale。出处：McKinsey, Rethinking Enterprise Architecture for the Agentic Era<sup>[[1]](#ref-1)</sup>（via syndicated summary）。

1. **「Domain-Based Modernization」是绝大多数企业的现实路径**。完全替换不可行、纯增量太慢，McKinsey 建议沿高价值工作流（domain）做现代化，由 agentic mesh 编排层连接 Agent 之间和 Agent 与遗留系统之间——「prevents incremental modernization from becoming unmanageable」。出处：McKinsey<sup>[[1]](#ref-1)</sup>。

1. **「Tool-First Design over MCP」是 arXiv 2512.08769 给出的第一条工程铁律**。先把能力定义为 tool（明确的输入输出 schema），再决定是否通过 MCP 暴露——而不是先选 MCP 协议、再硬塞业务逻辑。这一原则保证了 tool 的可复用性、可测试性和可治理性。出处：A Practical Guide for Designing Production-Grade Agentic Workflows<sup>[[2]](#ref-2)</sup>。

1. **「Pure-Function Invocation」是另一条核心铁律**：所有 tool 调用必须是纯函数（无副作用、可重放、可缓存），副作用通过显式的「writeback agent」聚合，避免 Agent 随时随地写数据库。出处：arXiv 2512.08769<sup>[[2]](#ref-2)</sup>。

1. **「Single-Tool / Single-Responsibility Agent」原则反对「万能 Agent」**。每个 Agent 应该只负责一类决策、调用一组紧密相关的 tool；通过 Workflow 把多个专门 Agent 编排起来，而不是让一个 Agent 同时做检索、推理、写入、通知。出处：arXiv 2512.08769<sup>[[2]](#ref-2)</sup>、InfoQ, Architecting Agentic MLOps<sup>[[3]](#ref-3)</sup>。

1. **MCP 和 A2A 是互补的、不是替代的**。MCP（Model Context Protocol）解决「Agent ↔ 外部工具/数据」的接口；A2A（Agent-to-Agent Protocol）解决「Agent ↔ Agent」的通信。MLConference 和 InfoQ 都强调企业 Agent 平台需要同时支持两者——MCP 把 OpenAPI 转换成 agent-ready tools；A2A 让多 Agent 系统跨 vendor 协作。出处：MLConference, MCP vs A2A<sup>[[4]](#ref-4)</sup>、InfoQ<sup>[[3]](#ref-3)</sup>、Towards AI, A2A vs MCP<sup>[[5]](#ref-5)</sup>。

1. **多 Agent 编排模式有 4 种主流形态：监督者-工人（Supervisor-Worker）、流水线（Pipeline）、辩论（Debate）、市场（Marketplace）**。OnAbout 把这些与 ROI / latency / governance 难度做了对照——监督者-工人模式可解释性最强、最适合企业；辩论模式准确性最高但成本和 latency 极差。出处：OnAbout, Mastering Multi-Agent Orchestration Architectures<sup>[[6]](#ref-6)</sup>、Medium Ozkaya, Agentic AI Patterns<sup>[[7]](#ref-7)</sup>。

1. **BCG「Building Effective Enterprise Agents」给出四章节框架**：①Why companies struggle to build Agents（legacy stack、messy data、国际化、复杂治理）②How to design Agents（明确 task、tool inventory、guardrails）③How to build Agents（platform thinking, governance integration）④How to assemble an Agent Platform（reusable building blocks + GUI）。出处：BCG, Building Effective Enterprise Agents<sup>[[8]](#ref-8)</sup>。

1. **AWS Prescriptive Guidance 强调「governance-first 架构」**：在设计 Agentic AI 时，governance、observability、IAM 必须与功能架构并列设计，而不是事后补加。出处：AWS, Governing and Architecting Agentic AI<sup>[[9]](#ref-9)</sup>。

1. **「Human Checkpoint Embedded into Architecture」**：McKinsey 直接说「Speed without governance creates compounding risk. Human checkpoints must be embedded into architecture, not added after the fact.」每个架构决策必须连到 measurable business outcome——不是为现代化而现代化。出处：McKinsey<sup>[[1]](#ref-1)</sup>。

## 二、重要性综述

架构是 Agentic AI 落地的核心赌注。错误的架构选择不只增加成本，会直接决定企业能不能从 PoC 走到生产、能不能跨多个用例复用基础设施、能不能在 12-24 个月后还活着。

**第一个核心张力：完全替换 vs 增量改造**。McKinsey 把这写得很直白：「Agentic AI offers a fundamental architectural choice: incremental integration on existing systems, or comprehensive transformation from the ground up. Most organizations will pursue a middle path—domain-based modernization that starts with high-value workflows and expands outward.」企业不可能为了 Agent 全盘重写 ERP/CRM/OA，但只在前端套个 LLM 也无法满足 Agent 的动态调用需求。中间路径——按业务域（订单履约、客服、销售支持、合规审计……）逐域现代化——成为绝大多数企业的现实选择。这条路径需要一个**编排层**把现代化的域和未现代化的遗留域桥起来，这就是 *agentic mesh*（McKinsey<sup>[[1]](#ref-1)</sup>）。

**第二个核心张力：自主性 vs 确定性**。Agentic AI 的卖点是自主决策，但企业的卖点是可预测性。arXiv 2512.08769 提出的「九大工程铁律」核心思想是：**用确定性的编排框架 + 可控的 tool 调用 + 外置化的 prompt 管理，来承载 LLM 的不确定推理**。具体落点包括：

- **Workflow logic 与 MCP server 解耦**：编排逻辑用代码（Python / TypeScript）固化，MCP server 只暴露 tool；这样可以单独测试 workflow，可以单独升级 tool，可以单独治理两端。

- **Externalized prompt management**：prompt 不写在代码里，存到版本化的 prompt store（如 LangFuse / PromptHub），可独立 A/B 测试、独立审计、独立 rollback。

- **Containerized deployment + Kubernetes**：每个 Agent / Workflow / Tool 都是独立可部署单元，可独立扩缩容、独立失败隔离。

- **KISS principle**：能用一个 Agent 解决就不用三个；能用规则解决就不用 LLM。

**第三个核心张力：单 Agent vs 多 Agent**。Medium Ozkaya 和 InfoQ 都强调 single-Agent 系统在大多数生产场景中比 multi-Agent 更稳定、更便宜、更易调试；只有当任务确实需要 specialization 或 parallel reasoning 时才上多 Agent。BCG 的四章节框架第三章「How to build Agents」里也警告：**不要被 multi-agent debate / society 这类研究 hype 带偏，企业最常用的是 supervisor-worker 模式 + 1-3 个 worker agent**（BCG, Building Effective Enterprise Agents<sup>[[8]](#ref-8)</sup>、OnAbout<sup>[[6]](#ref-6)</sup>、Medium Ozkaya<sup>[[7]](#ref-7)</sup>）。

**第四个核心张力：MCP vs A2A vs 私有协议**。MCP 在 2024 年底由 Anthropic 推出后迅速成为「Agent 接外部能力」的事实标准；A2A 由 Google 主导，瞄准「Agent 间通信」。两者不是二选一，而是**用在不同层**——MCP 是「数据/工具层协议」，A2A 是「编排层协议」。但 MCP 本身还不成熟（详见柱 4 风险 IAM 板块对 MCP 安全的讨论），所以企业级架构通常需要在 MCP 上加一层 *AI Gateway*（详见柱 2）来做认证、配额、审计。出处：MLConference<sup>[[4]](#ref-4)</sup>、InfoQ<sup>[[3]](#ref-3)</sup>、Towards AI<sup>[[5]](#ref-5)</sup>。

## 三、方案利弊

### 方案 A：单体 Agent 平台（vendor-managed end-to-end）—— Salesforce Agentforce / Microsoft Copilot Studio / Google Vertex AI Agent Builder

- **概述**：完整的 Agent 构建、部署、治理、监控一站式平台，绑定 vendor 生态。

- **适用场景**：已经深度使用 Salesforce / Microsoft 365 / Google Cloud 生态的企业；用例集中在 vendor 覆盖的 SaaS。

- **优势**：上线快（典型 PoC 4-8 周）；治理、IAM、audit 默认集成；vendor 全程支持。

- **劣势**：vendor lock-in 严重；跨 vendor 数据/能力需要额外网关；定价随用量陡增；不利于自研差异化能力。

- **出处**：Google Cloud, Choose your components for Agent Builder<sup>[[10]](#ref-10)</sup>、Microsoft Tech Community, AI Agents Reference Architecture<sup>[[11]](#ref-11)</sup>。

### 方案 B：自建编排层 + 开源 Agent 框架（LangGraph / AutoGen / CrewAI / Semantic Kernel）

- **概述**：用开源框架自建编排，MCP/A2A 接外部能力，配合自建/购买的可观测平台。

- **适用场景**：技术能力强的大型企业；需要跨多云、跨多 LLM 厂商的用例；有数据主权要求。

- **优势**：灵活、可定制、避免锁定；可与已有 DevOps/SRE 体系深度融合；成本可控。

- **劣势**：工程量大（典型 9-18 个月才能投产）；治理需要自建；开源框架本身在快速迭代，存在重写风险。

- **出处**：Fractal, LLMOps Architecture for Generative AI Systems<sup>[[12]](#ref-12)</sup>（#27）、InfoQ<sup>[[3]](#ref-3)</sup>。

### 方案 C：Agentic Mesh + 多 vendor 异构（MuleSoft Agent Fabric + Omni Gateway / Kong AI Gateway + LangChain）

- **概述**：把不同 vendor 的 Agent / 不同 LLM 通过统一 Mesh 编排和治理；可同时使用 Salesforce Agentforce、Microsoft Copilot、自建 LangGraph workflow。

- **适用场景**：年营收数百亿美元的大型集团；既有 Salesforce 又有 Microsoft，业务多元；并购多、IT 异构度高。

- **优势**：避免单一锁定；治理统一；可按业务域选最优 vendor。

- **劣势**：Mesh 层本身需要投入和持续运维；vendor 协议演进快可能导致 Mesh 频繁升级。

- **出处**：Salesforce, MuleSoft Omni Gateway for Agentic Enterprise<sup>[[13]](#ref-13)</sup>（#19）、McKinsey, Rethinking EA<sup>[[1]](#ref-1)</sup>（#06）。

### 方案 D：Hybrid — 业务侧用 vendor 平台 + 平台侧自建编排

- **概述**：业务部门用 vendor 提供的 low-code Agent Builder（速度优先）；CIO 团队自建 Agentic Mesh + Gateway + 可观测层（治理优先）。

- **适用场景**：组织成熟度差异大的大型集团；业务方 IT 能力弱但需要自主性。

- **优势**：业务速度和平台治理都不牺牲；vendor 锁定可控（只锁在前端）。

- **劣势**：边界协议复杂；需要明确「哪些动作必须经过中央 Mesh」。

- **出处**：BCG, Building Effective Enterprise Agents<sup>[[8]](#ref-8)</sup> 第四章「Agent Platform Assembly」、Cygnet, Best Practices for Enterprise AI Agent Deployment<sup>[[14]](#ref-14)</sup>。

### 选型建议

对于埃森哲典型客户（500–5000 亿美元营收，IT 异构、监管复杂、AI 投资 $100M+），**方案 C 是目标态、方案 D 是过渡态**。方案 A 仅适合用例单一的中型客户；方案 B 适合科技公司或有强自研需求的客户。

## 四、风险

1. **「Agent Sprawl」失控**：业务团队各自上 Agent，没有统一目录和治理，导致 IT 不知道企业里有多少 Agent、各 Agent 调用哪些数据/API。Cygnet 把这列为第一大落地阻碍。对策：从 Day 1 强制 Agent 注册到中央 catalog；Mesh 层拒绝未注册 Agent 的流量。出处：Cygnet<sup>[[14]](#ref-14)</sup>。

1. **MCP 协议未成熟期的「假标准」陷阱**：MCP 仍在快速演进，今天的 MCP server 可能 6 个月后需要重写。Salesforce 在 Omni Gateway 文章里指出：「MCP itself is still maturing as a standard…leaving real open questions around security and governance.」对策：把 MCP 隔在网关后面，业务代码不直接 import MCP SDK；可平滑替换。出处：Salesforce MuleSoft<sup>[[13]](#ref-13)</sup>。

1. **过度设计：拿研究模式做生产**：debate-style、society-of-agents 等模式在论文里漂亮，落地后 latency 数倍于 supervisor-worker，cost 也是。对策：默认 supervisor-worker；只在精度极敏感场景才考虑 debate。出处：OnAbout<sup>[[6]](#ref-6)</sup>、Medium Ozkaya<sup>[[7]](#ref-7)</sup>。

1. **「Implicit behavior」漂移**：当 prompt、tool 描述、LLM 模型版本三者中任一发生改变，Agent 行为可能整体漂移。arXiv 2512.08769 把这列为生产 agentic 系统最大风险之一。对策：prompt 版本化 + tool schema 锁定 + LLM 版本 pin。出处：arXiv 2512.08769<sup>[[2]](#ref-2)</sup>。

1. **「Bypass Standard Safeguards」**：CIO.com 引用 Trustwise COO Kamal Anand：「prototype success and production-ready systems where traditional safety controls fail against reasoning agents that can bypass standard safeguards.」对策：guardrails 必须做在 Mesh 层和 Tool 层（不可旁路），不能只靠 prompt 约束。出处：CIO.com, Change Management for AI Agents<sup>[[15]](#ref-15)</sup>（#57）。

1. **Mesh 自己成为单点故障**：Mesh / Gateway 故障会导致全企业 Agent 失能。对策：Mesh 必须做高可用、多区域；保留 fallback 通道；详细日志支持事后回溯。出处：Salesforce MuleSoft<sup>[[13]](#ref-13)</sup>。

## 五、适用场景

**优先重投架构现代化**：

- 业务流程已经数字化但跨多个系统的企业（保险理赔、银行客户服务、供应链）。

- 多并购历史导致 IT 异构、要做新生数据流的企业。

- 跨多个 vendor / 多 LLM 的客户（典型大型零售、消费品集团）。

**可分阶段投入**：

- 用例集中在单一部门的中型客户：先用 vendor 平台，2-3 年后再考虑 Mesh。

- 高合规行业但 IT 能力一般：先用 vendor 平台 + 治理外挂，不强求自建。

**可暂缓**：

- PoC 阶段、用例 < 3 个、跨系统调用 < 5 个 API：架构投入 ROI 不明显，先用代码级编排。

## 六、最佳实践案例

### 案例 1：Salesforce MuleSoft Agent Fabric + Omni Gateway

**架构定位**：Agent Fabric 是 Agent 编排控制平面，Omni Gateway 是治理 traffic 平面；二者解耦。
**关键能力**：

- Federated visibility：把第三方 gateway（Kong / Apigee）和自建 gateway 都纳入统一管控。

- MCP conversion：把现有 OpenAPI REST 自动转换成 agent-ready MCP tools，继承认证和合规策略。

- Unified LLM access：token 用量、model routing、guardrails 在共享 policy layer。

- End-to-end correlation IDs：跨整个 agent chain 留 audit trail。

**落地价值**：「policies applied once, consistently, regardless of which underlying gateway is handling the traffic」。
**出处**：Salesforce, MuleSoft Omni Gateway<sup>[[13]](#ref-13)</sup>。

### 案例 2：arXiv 2512.08769 案例 — 多模态新闻分析与媒体生成 Workflow

**场景**：自动 scrape 网页 → 主题过滤 → 生成 podcast script（agent consortium）→ 整合推理输出 → 生成 audio/video → 发布到 GitHub。

**架构特点**：

- 多 LLM 协同（OpenAI + Gemini + Llama + Anthropic）；

- 严格的 tool-first design over MCP；

- pure-function invocation；

- single-tool single-responsibility agents；

- containerized deployment + Kubernetes。

**贡献**：这是当前公开论文中最完整的、可复用的生产级 agentic workflow 蓝本。
**出处**：arXiv 2512.08769<sup>[[2]](#ref-2)</sup>。

### 案例 3：Cognition AI — Devin 自主软件工程 Agent

**场景**：自主 SE Agent，集成 GitHub / Slack / VS Code，能在完整开发环境里管理 machine state、处理 PR、debug。
**架构特点**：parallel task processing；与现有 dev workflow 深度集成；machine state management（不像无状态 LLM）。
**出处**：ZenML LLMOps Database, Cognition AI / Devin case<sup>[[16]](#ref-16)</sup>。

### 案例 4：Chaos Labs — Edge AI Oracle 多 Agent 共识系统

**场景**：预测市场查询裁决；用 LangChain + LangGraph 构建 decentralized AI agent 网络，多 LLM 共识。
**架构特点**：specialized agents；configurable consensus requirements；transparent, traceable results。
**出处**：ZenML LLMOps Database, Chaos Labs case<sup>[[16]](#ref-16)</sup>。

### 案例 5：BCG 报告中提及的「Agent Platform」模式

**核心思想**：把 Agent 平台拆为 reusable building blocks（tools、prompts、evaluators、observability hooks）+ GUI（business analyst 自助组装）。
**关键原则**：先建 platform，再让业务自助上线 Agent；platform 是产品，不是项目。
**出处**：BCG, Building Effective Enterprise Agents, Chapter 4<sup>[[8]](#ref-8)</sup>。

### 案例 6：AWS Prescriptive Guidance — Govern & Architect Agentic AI

**贡献**：AWS 官方 prescriptive guide，覆盖 reference architecture、guardrails、observability、scaling patterns；可作为 AWS 上 Agent 部署的标准依据。
**出处**：AWS Prescriptive Guidance<sup>[[9]](#ref-9)</sup>。

### 案例 7：Microsoft Azure AI Foundry Reference Architecture

**贡献**：Azure AI Foundry + Container Apps + Key Vault + Cosmos DB 的 enterprise reference architecture；强调 modularity、scalability、deep IAM 集成。
**出处**：Microsoft TechCommunity, Architecting AI Agents on Azure AI Foundry<sup>[[11]](#ref-11)</sup>。

---

**下一节**：柱 2：API 治理

---

## 参考文献

<a id="ref-1"></a>1. [McKinsey, Rethinking Enterprise Architecture for the Agentic Era](https://www.taazaa.com/blog/rethinking-enterprise-architecture-agentic-era)

<a id="ref-2"></a>2. [A Practical Guide for Designing Production-Grade Agentic Workflows](https://arxiv.org/html/2512.08769v1)

<a id="ref-3"></a>3. [InfoQ, Architecting Agentic MLOps](https://www.infoq.com/articles/architecting-agentic-mlops-a2a-mcp/)

<a id="ref-4"></a>4. [MLConference, MCP vs A2A](https://mlconference.ai/blog/mcp-vs-a2a-ai-agent-communication-enterprise/)

<a id="ref-5"></a>5. [Towards AI, A2A vs MCP](https://pub.towardsai.net/architecting-intelligent-multi-agent-ai-systems-a2a-vs-mcp-8c3268ccc1c3)

<a id="ref-6"></a>6. [OnAbout, Mastering Multi-Agent Orchestration Architectures](https://www.onabout.ai/p/mastering-multi-agent-orchestration-architectures-patterns-roi-benchmarks-for-2025-2026)

<a id="ref-7"></a>7. [Medium Ozkaya, Agentic AI Patterns](https://mehmetozkaya.medium.com/agentic-ai-architectures-with-patterns-frameworks-mcp-25afcc97ae62)

<a id="ref-8"></a>8. [BCG, Building Effective Enterprise Agents](https://www.bcg.com/assets/2025/building-effective-enterprise-agents.pdf)

<a id="ref-9"></a>9. [AWS, Governing and Architecting Agentic AI](https://docs.aws.amazon.com/prescriptive-guidance/latest/govern-architect-agentic-ai/)

<a id="ref-10"></a>10. [Google Cloud, Choose your components for Agent Builder](https://cloud.google.com/blog/products/ai-machine-learning/choose-the-right-components-for-your-agents-on-vertex-ai-agent-builder)

<a id="ref-11"></a>11. [Microsoft Tech Community, AI Agents Reference Architecture](https://techcommunity.microsoft.com/blog/azurearchitectureblog/architecting-ai-agents-on-microsoft-azure-ai-foundry/)

<a id="ref-12"></a>12. [Fractal, LLMOps Architecture for Generative AI Systems](https://fractal.ai/blog/llmops-architecture-for-generative-ai-systems)

<a id="ref-13"></a>13. [Salesforce, MuleSoft Omni Gateway for Agentic Enterprise](https://www.salesforce.com/blog/mulesoft-omni-gateway-agentic-ai-governance/)

<a id="ref-14"></a>14. [Cygnet, Best Practices for Enterprise AI Agent Deployment](https://www.cygnet.one/feeds/blog/ai-agents-enterprise-deployment-november-2025)

<a id="ref-15"></a>15. [CIO.com, Change Management for AI Agents](https://www.cio.com/article/4079017/cios-must-lead-change-management-for-ai-agent-rollouts-thats-not-easy.html)

<a id="ref-16"></a>16. [ZenML LLMOps Database, Cognition AI / Devin case](https://www.zenml.io/llmops-database)
