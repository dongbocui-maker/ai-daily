---
order: 5
slug: llmops
docNum: "05 · 柱 3"
docColor: p3
title: "LLMOps / AgentOps"
feishuToken: T9PJd9NsCo1M0UxN3zhcS91gnNe
words: "~13K 字"
---
# 柱 3：LLMOps / AgentOps

> 本板块基于以下源：#26, #27, #28, #29, #30, #31, #32, #33, #34, #35

## 一、核心观点

1. **「Semantic Observability」是 LLMOps 与传统 monitoring 的根本分界**：传统监控看 uptime / CPU / 错误率，LLM 失败是 semantic & behavioral——hallucination、partial answer、syntactically correct but semantically wrong。Fractal 直陈：「Traditional monitoring focuses on system health metrics… LLM failures are semantic and behavioral, requiring visibility into prompts, agent decisions, token usage, and retrieval context.」出处：Fractal, LLMOps Architecture for GenAI<sup>[[1]](#ref-1)</sup>。

1. **「MLOps → LLMOps → AgentOps」是逐级递进的运维体系**：MLOps 关注模型训练-部署-监控；LLMOps 增加 prompt versioning、RAG pipelines、token economy；AgentOps 进一步增加 tool 调用、规划与反思、long-running execution、人工干预循环。三者在企业内并存，不是替代关系。出处：Covasant, MLOps vs LLMOps vs AgentOps<sup>[[2]](#ref-2)</sup>（#30）、Iguazio, LLMOps vs MLOps<sup>[[3]](#ref-3)</sup>（参见 #30 引用）。

1. **「Hallucination 在 2024 年造成 $67B 业务损失」**：Galileo 在 2026 年 2 月报告引用该数据，指明这是 LLMOps 平台核心要解决的问题，purpose-built evaluation frameworks 必须能在生产时实时检测幻觉。出处：Galileo, 7 Best LLMOps Platforms<sup>[[4]](#ref-4)</sup>。

1. **「S&P Global 2025：42% 企业放弃 AI 项目，比上年翻倍（17% → 42%）」**：Galileo 把这归因为缺少 observability / evaluation / governance 三位一体的 LLMOps 平台。出处：Galileo<sup>[[4]](#ref-4)</sup>。

1. **「Token-Level Cost Tracking 是 LLMOps 的入场券」**：ByteDance 通过 token 优化做到 50% cost reduction，业内有 90x improvement 的极端案例。Galileo Luna-2 evaluation 模型把 evaluation 自身成本降低 97% vs GPT-4。这意味着「systematic continuous evaluation」在经济上变得可行。出处：Galileo<sup>[[4]](#ref-4)</sup>。

1. **「Agent Graph Visualization」是 multi-agent 调试的关键工具**：当 cascading failure 在 reasoning chain 里发生时，必须能可视化每一步推理、每一次 tool 调用、每一次 LLM 输出。Galileo Agent Graph、LangSmith End-to-End Tracing、Arize Phoenix 都在做这件事。出处：Galileo<sup>[[4]](#ref-4)</sup>。

1. **「Continuous Evaluation」是 evaluation 的范式转移**：传统 ML 用 hold-out test set 一次性评估；LLM 系统必须在生产环境持续评估——prompt、模型、数据三者中任一变化都会导致行为漂移。IJCESEN 论文系统化提出 continuous evaluation framework：包括 functional accuracy / safety / fairness / cost / latency 五维度持续度量。出处：IJCESEN, Continuous Evaluation Methodologies for AI Agents<sup>[[5]](#ref-5)</sup>（#32）。

1. **「Prompt 是新的代码」，必须版本化 + A/B 测试 + rollback**：Covasant 明确指出 prompts are the 'new code' but unversioned and unmanaged 是 LLMOps 头号痛点。LangSmith、PromptLayer、LangFuse、PromptHub 都在解决这个问题。出处：Covasant<sup>[[2]](#ref-2)</sup>。

1. **「AgentOps 必须包含 long-running execution 管理」**：Agent 可能跑数分钟到数小时，普通监控工具按 request-response 设计，无法覆盖。AgentOps 工具需要 trace 状态机、failed-step 重试、人工 takeover、计划修改、cost 追溯。出处：OneReach, LLMOps Goes Agentic<sup>[[6]](#ref-6)</sup>（#29）、LinkedIn, AgentOps Operational Observability<sup>[[7]](#ref-7)</sup>（#31）。

1. **「ZenML 案例数据库 = 457 个真实生产案例库」**，是当前公开最完整的 LLMOps 实战数据库，覆盖从初创到 Fortune 100 的多行业部署，对 Accenture、AWS、Microsoft、Google Cloud、Databricks、Snowflake、Anthropic 等都有专题。出处：ZenML LLMOps Database<sup>[[8]](#ref-8)</sup>（#33）、ZenML LLMOps Database (overview)<sup>[[9]](#ref-9)</sup>（#34）。

## 二、重要性综述

LLMOps / AgentOps 是 Agentic AI 落地的「神经系统」——如果架构是骨骼、数据是血肉、API 治理是循环系统，那么 LLMOps 就是让你能看见、能诊断、能干预这个有机体的神经网络。

**为什么传统监控不行**？Fractal 用一句话讲清：「LLM failures are semantic and behavioral.」Hallucination 不会让服务器宕机、不会让 HTTP 返回 500，它会用看似正确的语法返回错误的事实。传统 APM（Datadog、New Relic、Dynatrace）按指标（uptime、CPU、error rate）报警，它看不见「这个回答在事实上错了 20%」——这就是为什么 Galileo 强调 semantic observability 是 LLMOps 平台的差异化定义。

**LLMOps 的核心能力可以归为 4 类**：

1. **Tracing / Observability**：捕获每次 LLM 调用、每次 tool 调用、每个 retrieval 命中，组成一条完整的 reasoning chain。LangSmith、Galileo、Arize Phoenix、Langfuse 是这一赛道头部玩家。

1. **Evaluation**：Online evaluation（生产流量上做轻量评估）+ offline evaluation（用 golden dataset 做回归测试）+ human-in-the-loop evaluation（运营/SME 抽检并标注）。IJCESEN 论文把 evaluation 维度系统化为 5 类——functional accuracy / safety / fairness / cost / latency。

1. **Prompt & Model Lifecycle Management**：prompt 版本管理 + A/B 测试 + rollback；model registry + version pinning + canary deployment；以及在不同 LLM provider 间的 fallback 策略。

1. **Cost & Performance Optimization**：per-agent / per-use-case token budgets；smart routing（便宜模型先试、复杂任务才上贵模型）；caching；prompt compression。

**Agentic 时代，LLMOps 必须升级为 AgentOps**——增加：

- **Multi-step trace**：不只是「prompt + response」，而是「intent → plan → tool_call_1 → result_1 → reflect → tool_call_2 → result_2 → final_response」的完整状态机。

- **Tool invocation accuracy**：评估「Agent 选对了 tool 吗、传对了参数吗、解读对了返回吗」。Tool selection accuracy 在多 tool 场景下是关键 KPI。

- **Long-running execution**：Agent 可能跑 30 分钟到 30 小时；需要 checkpoint、resume、partial-rollback。

- **Human takeover**：当 Agent 进入低置信度区或触及高风险动作时，必须能交接给人。AgentOps 工具要记录每次 takeover 的上下文，便于事后复盘和模型改进。

- **Cost attribution**：把 token / API / GPU 成本分配到具体业务用例、具体客户、具体团队。

**ZenML 案例数据库（457 个真实案例）的价值**：这是当前公开材料里**唯一**做到「企业 LLMOps 工程化」横截面的数据库。Accenture、CircleCI、Cisco、Codeium、Co-op、BuzzFeed、Cedars Sinai、Cambrium、Canva、Capital One、Chevron Phillips Chemical 等案例均有详细技术写真。对埃森哲提案、客户 benchmarking、内部技术选型都是高价值素材（ZenML LLMOps Database<sup>[[8]](#ref-8)</sup>）。

## 三、方案利弊

### 方案 A：综合性 LLMOps 平台（Galileo / LangSmith / Arize）

- **概述**：覆盖 tracing + evaluation + prompt management + runtime guardrails 全栈。

- **适用场景**：中大型企业有 5-20 个生产 LLM/Agent 用例；监管行业。

- **优势**：开箱即用；compliance 认证（SOC 2 / HIPAA / GDPR）完整；vendor 持续迭代跟进新模型。

- **劣势**：成本中等偏高（典型 enterprise plan 1M/年）；evaluation logic 与 vendor 绑定。

- **代表能力**：Galileo Luna-2（97% cheaper evaluation）、Agent Graph、Insights Engine；LangSmith End-to-End Tracing + Visual Agent Builder。

- **出处**：Galileo<sup>[[4]](#ref-4)</sup>、Pratik on LLMOps<sup>[[10]](#ref-10)</sup>（#28）。

### 方案 B：开源 stack（Langfuse + Phoenix + OpenLLMetry + 自建 evaluation harness）

- **概述**：用开源组件搭建 LLMOps 栈，自建 evaluation 框架。

- **适用场景**：技术驱动型企业；数据主权要求；预算受限的快速增长企业。

- **优势**：成本可控（基础设施 + 工程师时间）；完全可控；可与企业内部数据平台深度集成。

- **劣势**：工程投入大；evaluation 框架需要长期维护；缺少 SOC2/HIPAA 认证（如果需要要自建）。

- **出处**：Fractal, LLMOps Architecture<sup>[[1]](#ref-1)</sup>、ZenML 案例库中的 Cisco / Codeium 自建栈案例。

### 方案 C：Cloud-native LLMOps（Azure AI Foundry / AWS Bedrock Agents / Google Vertex AI）

- **概述**：用云厂商的 LLMOps 工具链，紧贴 LLM 推理服务。

- **适用场景**：已经深度使用某一云栈的企业；用例集中在该云内的服务。

- **优势**：与 IAM / 数据平台 / 监控 / 计费 深度集成；vendor 一站式支持；compliance 继承云。

- **劣势**：跨云 / 跨 LLM 弹性差；功能上不及专门 LLMOps 平台精细。

- **出处**：Fractal<sup>[[1]](#ref-1)</sup>（Azure AI Foundry 案例）、AWS Bedrock 案例（ZenML 库）。

### 方案 D：「数据平台 + LLMOps」双轨（Databricks / Snowflake / Iguazio）

- **概述**：数据平台厂商在原有 MLOps 能力上扩展 LLMOps，强调 data + model 一体化。

- **适用场景**：已经在 Databricks / Snowflake 上做数据现代化的企业。

- **优势**：data → feature → model → prompt → evaluation 端到端一致；MLOps 资产可复用。

- **劣势**：Agent 编排能力相对弱；需要外挂 Agent 框架（LangGraph / AutoGen）。

- **出处**：Iguazio, LLMOps vs MLOps<sup>[[3]](#ref-3)</sup>（参见 #30）、ZenML 库 Databricks/Snowflake 案例。

### 选型建议

埃森哲典型客户：**A + D 混合**——A 提供 LLMOps 平台标杆能力，D 提供数据底座的一致性。方案 C 适合「all-in 某一云」的客户；方案 B 仅适合科技驱动型客户。

## 四、风险

1. **「Vanity Metrics 陷阱」**：只看 token 量、调用次数、latency，看不见 hallucination 率、tool selection accuracy、user task completion。对策：从 Day 1 把 semantic 指标（accuracy、faithfulness、relevance、harmfulness）作为核心 KPI，不只看技术指标。出处：Galileo<sup>[[4]](#ref-4)</sup>、IJCESEN<sup>[[5]](#ref-5)</sup>。

1. **「Eval Set 陈旧」**：评估数据集一次性建好后不更新，与生产分布漂移；evaluation 通过但生产仍出错。对策：rolling eval set，每月从生产 trace 中抽样新增样本；建立 SME 参与的标注流程。出处：IJCESEN<sup>[[5]](#ref-5)</sup>。

1. **「Prompt-Tool-Model 三角漂移」**：升级了任一项（换了 prompt 模板 / 换了 tool 描述 / 换了 LLM 版本），其他两项不重测，行为整体漂移。对策：把 prompt / tool / model 三者绑定成 release artifact；强制三者一起 release。出处：arXiv 2512.08769<sup>[[11]](#ref-11)</sup>。

1. **「LLM 厂商单点依赖」**：只用 OpenAI，一次 outage 全部 Agent 停摆。对策：multi-provider routing（OpenAI + Azure OpenAI + Anthropic + 自建开源）+ 自动 fallback。Galileo / Portkey / LiteLLM 都支持。出处：Galileo<sup>[[4]](#ref-4)</sup>、Pratik on LLMOps<sup>[[12]](#ref-12)</sup>。

1. **「Long-Running 卡死」**：Agent 进入死循环或在某个 tool 上无限重试，token 烧光、用户挂死。对策：strict execution budget（最大 step 数 + 最大 token + 最大 wall-clock）+ 异常超阈值自动 escalate。出处：Cygnet<sup>[[13]](#ref-13)</sup>。

1. **「Observability 自身就是攻击面」**：Trace 数据包含敏感 prompt 内容（包括客户数据），可能存到外部 SaaS。对策：选支持 VPC / on-prem 部署的工具；启用 trace masking；与数据治理（底座）联动。出处：Galileo<sup>[[4]](#ref-4)</sup>（VPC / on-prem 选项）。

## 五、适用场景

**优先重投 LLMOps**：

- 任何已经有 ≥ 3 个生产 LLM/Agent 用例的企业；

- 监管行业（金融、医疗、政府）——SOC 2/HIPAA 必备；

- 单一 Agent 失误成本 > $10k 的高风险场景（合同生成、客服自动决策、金融预测）。

**可分阶段投入**：

- 仅 1-2 个用例的早期阶段：先用云厂商内置 monitoring，等用例 ≥ 5 个再上专门平台；

- 内容生成类轻量场景：先用 SDK 级 logging（OpenLLMetry）。

**可暂缓**：

- 纯实验阶段，没有生产部署：不需要专门 LLMOps，用 notebook + git + manual review 即可。

## 六、最佳实践案例

### 案例 1：Galileo + 金融服务客户（$6.4 万亿 AUM）

**场景**：合规要求极严的金融客户，敏感客户数据，需要 SOC 2 + HIPAA + GDPR + ISO 27001 + VPC 部署。
**做法**：Galileo Luna-2 evaluation（成本相比 GPT-4 降 97%）+ Agent Graph 可视化 + runtime protection（< 200ms 拦截有害输出）。
**结果**：30%+ efficiency gain at massive scale；media 客户「100% accuracy across 400+ deployments」。
**出处**：Galileo, Best LLMOps Platforms<sup>[[4]](#ref-4)</sup>。

### 案例 2：Cisco LLMOps Framework

**场景**：将 DevOps 实践适配到 LLM 应用规模化部署。
**做法**：自建 LLMOps 框架；focus on continuous delivery, robust monitoring, stringent security, specialized operational support；强调 enterprise-specific considerations like scalability, integration with existing systems, governance。
**意义**：Fortune 100 自建 LLMOps 的标杆案例。
**出处**：ZenML LLMOps Database, Cisco case<sup>[[8]](#ref-8)</sup>。

### 案例 3：CircleCI LLM-Based Application Testing

**场景**：AI error summarizer，处理非确定性输出和主观评估的挑战。
**做法**：model-graded evaluations + robust error handling + user feedback loops；强调测试 LLM-based app 需要新的测试策略，超越 simple string matching。
**结果**：valuable AI features 通过 focused exploration + iterative development 达成；不需要复杂自研模型。
**出处**：ZenML LLMOps Database, CircleCI case<sup>[[8]](#ref-8)</sup>。

### 案例 4：Canva Magic Switch 评估框架

**场景**：systematic LLM evaluation framework；定义 success criteria 和 measurable metrics before implementation。
**做法**：rule-based + LLM-based evaluators 评估 content quality；维度 = information preservation / intent alignment / format；regression testing 保证 prompt 改进不退化整体质量。
**意义**：把 evaluation engineering 做成产品级实践，可作为埃森哲为客户设计 evaluation 体系的参考。
**出处**：ZenML LLMOps Database, Canva case<sup>[[8]](#ref-8)</sup>。

### 案例 5：Convirza 多 LoRA 服务架构

**场景**：分析数百万条 call center 对话，sub-0.1s 推理。
**做法**：Llama 3B + LoRA adapters via Predibase；multi-adapter serving on single GPU；vs OpenAI 节省 10x 成本；F1 提升 8%；吞吐提升 80%。
**意义**：smaller fine-tuned model + multi-LoRA 是 enterprise high-volume Agent 的可重复模式。
**出处**：ZenML LLMOps Database, Convirza case<sup>[[8]](#ref-8)</sup>。

### 案例 6：Cleric AI SRE Agent

**场景**：AI-powered SRE 自主调查生产事件。
**做法**：reasoning engine + tool integrations + memory system；continuous learning（捕获 feedback 并 generalize patterns）；transparent decision-making + configurable model selection + human oversight for remediation。
**意义**：可作为 IT Operations 部门 Agent 部署的参考模板。
**出处**：ZenML LLMOps Database, Cleric AI case<sup>[[8]](#ref-8)</sup>。

### 案例 7：Coval — 应用自动驾驶仿真原则做 Agent 测试

**场景**：从 manual testing → probabilistic approach with dynamic scenarios + multi-layered testing architectures。
**做法**：用 LLM benchmark agent performance against human capabilities；提供 dynamic scenario generation + performance monitoring 工具。
**意义**：Agent testing 范式从「单 case PASS/FAIL」演进为「概率分布 + 场景空间覆盖」。
**出处**：ZenML LLMOps Database, Coval case<sup>[[8]](#ref-8)</sup>。

### 案例 8：Character.ai — 30,000 messages per second 规模化

**场景**：大规模对话 AI 平台。
**做法**：自建 foundation models + multi-query attention（GPU cache 减少）+ 自研 GPU cache 系统 + prompt management system「prompt-poet」。
**意义**：超大规模 Agent 服务的可参考做法（虽然多数客户不会到此规模，但架构思路有价值）。
**出处**：ZenML LLMOps Database, Character.ai case<sup>[[8]](#ref-8)</sup>。

---

下一节：柱 4：风险治理 + IAM

---

## 参考文献

<a id="ref-1"></a>1. [Fractal, LLMOps Architecture for GenAI](https://fractal.ai/blog/llmops-architecture-for-generative-ai-systems)

<a id="ref-2"></a>2. [Covasant, MLOps vs LLMOps vs AgentOps](https://www.covasant.com/blog/mlops-vs-llmops-vs-agentops-key-differences)

<a id="ref-3"></a>3. [Iguazio, LLMOps vs MLOps](https://www.iguazio.com)

<a id="ref-4"></a>4. [Galileo, 7 Best LLMOps Platforms](https://galileo.ai/blog/best-agent-observability-platforms-scaling-generative-ai)

<a id="ref-5"></a>5. [IJCESEN, Continuous Evaluation Methodologies for AI Agents](https://www.ijcesen.com)

<a id="ref-6"></a>6. [OneReach, LLMOps Goes Agentic](https://onereach.ai/blog/llmops-agentic-ai)

<a id="ref-7"></a>7. [LinkedIn, AgentOps Operational Observability](https://www.linkedin.com/pulse/agentops-operational-observability-agentic-ai-vishvambhar-dayal-yfxpc)

<a id="ref-8"></a>8. [ZenML LLMOps Database](https://www.zenml.io/llmops-database)

<a id="ref-9"></a>9. [ZenML LLMOps Database (overview)](https://www.zenml.io)

<a id="ref-10"></a>10. [Pratik on LLMOps](https://medium.com/@pratik.gajbhiye)

<a id="ref-11"></a>11. [arXiv 2512.08769](https://arxiv.org/html/2512.08769v1)

<a id="ref-12"></a>12. [Pratik on LLMOps](https://medium.com)

<a id="ref-13"></a>13. [Cygnet](https://www.cygnet.one/feeds/blog/ai-agents-enterprise-deployment-november-2025)
