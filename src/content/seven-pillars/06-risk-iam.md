---
order: 6
slug: risk-iam
docNum: "06 · 柱 4"
docColor: p4
title: "风险治理 + IAM"
feishuToken: ShovdCMBxokvmXxWl3NcOrUsnnf
words: "~15K 字"
---
# 柱 4：风险治理 + IAM

> 本板块基于以下源：#11, #36, #37, #38, #39, #40, #41, #42, #43, #44, #45, #48, #49, #50

## 一、核心观点

1. **「AI Agent = 非人身份（Non-Human Identity, NHI）」是 IAM 在 agentic 时代必须接受的新范式**。Okta 直陈：在云原生环境里，「service accounts and API keys often outnumber human users」；Agent 作为 NHI 必须像人类员工一样有完整的生命周期管理（onboarding / entitlement / certification / deprovisioning）。出处：Okta, The Role of AI in IAM<sup>[[1]](#ref-1)</sup>。

1. **「AI Agent 必须用 delegated authority 而不是 user impersonation」**。OpenID 白皮书（10/2025）核心论断：「User impersonation by agents should be replaced by delegated authority…True delegation requires explicit 'on-behalf-of' flows where agents prove their delegated scope while remaining identifiable as distinct from the user they represent.」出处：OpenID, AI Identity, Authentication, and Authorization Whitepaper<sup>[[2]](#ref-2)</sup>。

1. **OAuth 2.1 + Token Exchange (RFC 8693) 是当前可用的事实标准**。Okta 列出 5 大 AI Agent 控制项：①Delegated Authority（OAuth 2.0 token exchange + workload identity federation）②Fine-Grained Authorization（ReBAC / ABAC 替代 RBAC）③ISPM（Identity Security Posture Management）④HITL via CIBA ⑤CAEP（Continuous Access Evaluation）。出处：Okta<sup>[[1]](#ref-1)</sup>。

1. **「NIST AI RMF Agentic Profile」（CSA 2026 年 3 月白皮书）是当前最权威的 Agentic AI 风险框架**。它在 NIST AI RMF 1.0 的 GOVERN / MAP / MEASURE / MANAGE 四函数上叠加四类新能力：①autonomy tier classification + oversight obligations（GOVERN 扩展）②systematic tool-use risk modeling + action-consequence mapping（MAP 扩展）③runtime behavioral metrics + autonomy calibration + delegation chain monitoring（MEASURE 扩展）④structured incident response + behavioral drift correction + principled agent decommissioning（MANAGE 扩展）。出处：CSA, NIST AI Risk Management Framework: Agentic Profile<sup>[[3]](#ref-3)</sup>。

1. **CSA「Agentic Trust Framework: Zero Trust for AI Agents」** 把 Zero Trust 原则系统映射到 Agent 上下文：never trust always verify、explicit verification、assume breach 三大 ZT 原则需要扩展到「Agent Identity / Action / Memory」三层。出处：CSA, Agentic Trust Framework<sup>[[4]](#ref-4)</sup>。

1. **OWASP「State of Agentic AI Security and Governance 1.0」（5/2026）+ OWASP「LLM Top 10」**：当前 Agent 安全风险的事实标准清单，覆盖 prompt injection、tool poisoning、memory poisoning、excessive agency、insecure output handling 等。出处：OWASP, State of Agentic AI Security and Governance 1.0<sup>[[5]](#ref-5)</sup>、OWASP AI Exchange<sup>[[6]](#ref-6)</sup>（#45）。

1. **「Microsoft Defender NIST-Based Security Framework for AI Agents」（1/2026）** 提供了产品化的 Agent 安全治理蓝图：把 NIST AI RMF 的 4 函数翻译成 Microsoft Defender 的检测、响应、合规能力。出处：Microsoft, Architecting Trust: A NIST-Based Security Governance Framework for AI Agents<sup>[[7]](#ref-7)</sup>。

1. **「ARC Framework」（GovTech Singapore，arXiv 2512.22211）**：「Agentic Risk & Capability」三源风险模型——components / design / capabilities。它的创新点是「**capability-centric**」视角——不分析具体 tool，而是分析 Agent 能执行的动作类（code execution / internet interaction / file modification 等），更稳定也更可治理。出处：ARC Framework<sup>[[8]](#ref-8)</sup>（#38）。

1. **「Identity Defined Security Alliance」（IDSA）给出三阶段实施路径**：Phase 1 Assessment（评估现有 IAM 成熟度、识别 AI 管理缺口、定义安全/合规要求）→ Phase 2 Planning（开发 AI-specific 访问策略、设计 workflow、规划部署）→ Phase 3 Implementation（落地策略、做 monitoring、持续优化）。出处：IDSA, IAM Implications of AI in 2025<sup>[[9]](#ref-9)</sup>（#50）。

1. **Agent 风险有 4 个「结构性新维度」**：①Irreversibility（一旦动作发起就无法撤销）②Cascading delegation（Agent 派生 Sub-Agent，责任分散）③Temporal gap（动作发起到人能观察到的时间差）④Memory persistence + cross-session poisoning。这些维度在传统 IT 风险框架中都没有对应概念。出处：CSA, NIST RMF Agentic Profile<sup>[[3]](#ref-3)</sup>。

1. **「97% 的企业领导预期未来 12 个月内会发生 AI Agent 驱动的安全/欺诈事件，但只有 6% 的安全预算分配到该风险」**——Dynamisch 2026 年初的调研。这是当前安全投入与风险暴露之间最严重的不对称。出处：Dynamisch, 6 Critical Realities<sup>[[10]](#ref-10)</sup>（#59）。

1. **「缺乏 AI 治理政策的企业平均每次数据泄露多损失 $670,000；63% 的泄露企业完全没有 AI 治理政策」**。出处：Dynamisch<sup>[[10]](#ref-10)</sup>。

## 二、重要性综述

风险治理 + IAM 是 Agentic AI 时代最容易被低估、却也最致命的支柱。原因有 3 个：

**第一，Agent 把企业内既有的 IAM 弱点放大成结构性危机**。Okta 给出非常具体的对照表：

- 传统 IAM：人类用户 + 少量服务账号、静态策略 RBAC、规则告警人工调查、人工工单 workflow、计划性 access review、粗粒度（应用/数据库级）、静态日志

- AI-Driven IAM：人类 + NHI + AI agent + ephemeral workloads、持续风险评估 ReBAC/ABAC、行为异常检测自动 ITDR、实时自服务 + policy guardrails、ISPM 持续姿态评估、细粒度（属性、关系、资源级）、上下文化事件流 + provenance tracking

「Service accounts and API keys often outnumber human users」这个事实已经在云原生企业里成立；Agent 把它推到极限——「每个用户可能并发拥有 5-10 个 Agent」，NHI 总量从「百级」跃迁到「万级」甚至「十万级」。任何不能在这个量级下做 continuous evaluation 和 automated ITDR 的 IAM 系统都将失败。

**第二，Agent 风险有 4 个传统 IT 风险框架没有的结构性新维度**。CSA NIST RMF Agentic Profile 把它讲得最清楚：

1. **Irreversibility**：Agent 可以发起不可撤销的现实世界动作——删数据、发邮件、改配置、触发金融交易。传统软件「发现错误立即回滚」的假设不再成立。

1. **Cascading delegation**：编排 Agent 派生 Sub-Agent，整个动作序列的责任在多个 Agent 间分布；当出问题时，传统的「单一所有者」追责模型失效。

1. **Temporal gap**：Agent 发起动作到任何人观察到行为异常之间存在巨大时间差——可能数小时、数天、甚至数月。Behavioral drift accumulates undetected until it crosses a critical threshold（CSA）。

1. **Memory persistence + cross-session poisoning**：Agent 跨会话保留 memory，一次被恶意输入污染（prompt injection through tool outputs）就可能在数周后才显现影响。

这些维度对应的攻击向量也是全新的：**prompt injection through tool outputs、cross-session memory persistence、tool-chain poisoning** —— 没有任何传统 SOC / SIEM / EDR 产品对此有标准能力。

**第三，监管压力同步加速到来**。EU AI Act（生效 2025-2026 分阶段实施）+ NIST AI RMF + NIST「AI Agent Standards Initiative」（2026 年 2 月启动、Q4 发布 Interoperability Profile）+ ISO/IEC 42001（AI 管理体系）+ 各国 sectoral 法规（HIPAA AI Addendum、PCI AI Annex 等）——监管节奏远快于绝大多数企业的合规能力建设节奏。CSA 把它讲得直

白：现有 NIST AI RMF 1.0 + AI 600-1（GenAI Profile）都没有覆盖 agentic 风险，必须靠 Agentic Profile 这类技术性 supplement 来弥补。

**风险治理的核心动作**有 5 组：

1. **Autonomy Tier Classification**（GOVERN）：把 Agent 按自主性等级分类（L0 完全人工 → L1 建议生成 → L2 人审批 → L3 异常报告 → L4 完全自主），不同等级对应不同的 oversight obligation。CSA + ARC Framework 都强调这一点。

1. **Tool-Use Risk Modeling + Action-Consequence Mapping**（MAP）：列出每个 Agent 能调用的 tool、每个 tool 的最坏影响（数据 / 资金 / 操作）、对应的 control（黑名单、白名单、需审批、需 2-eye）。ARC Framework 把这叫 capability-centric analysis。

1. **Runtime Behavioral Metrics + Autonomy Calibration**（MEASURE）：实时监控 Agent 行为指标——tool 调用频率、错误率、escalation 率、user satisfaction、cost variance。设定动态阈值，超阈值自动降级或人工接管。

1. **Identity Lifecycle**（IAM）：从 onboarding（注册 Agent 身份 + 颁发 credential + 绑定 owner）→ entitlement（分配 scope + 设置 expiry）→ certification（定期 review + 续期）→ deprovisioning（删除 token + 撤销访问 + 归档审计）。

1. **Incident Response + Drift Correction**（MANAGE）：建立 Agent compromise response playbook；定期检测 behavioral drift；建立 principled agent decommissioning 流程。

**OpenID 白皮书的关键贡献**是给出了「**未来 Agent 身份的关键问题清单**」：

- **Agent identity fragmentation should be avoided**：避免每个 vendor 自建 agentic identity 体系，应该用 IPSIE（Interoperability Profiling for Secure Identity in the Enterprise）这类标准。

- **User impersonation should be replaced by delegated authority**：明确分清「Agent 身份 vs 用户身份」。

- **Scalability of human oversight & user consent**：当一个用户有 10 个 Agent 各做几百次决策时，consent UX 完全崩塌——需要 policy-based consent 而非 per-action consent。

- **AI workload differentiation**：区分 Agent / Service Account / Bot 等不同 NHI 类型。

## 三、方案利弊

### 方案 A：扩展现有 IAM 平台（Okta / Microsoft Entra / Ping / SailPoint）

- **概述**：在现有 IAM 平台上启用 AI-driven IAM 模块——ReBAC、ABAC、ISPM、CAEP、SCIM 扩展支持 AI Agent。

- **适用场景**：已经在用 Okta/Microsoft 全栈的企业；监管行业需要快速合规。

- **优势**：继承既有人员/角色体系；与 SSO/MFA/PAM 集成无缝；vendor 支持成熟。

- **劣势**：Agent-specific 能力相对初级（标准未稳定）；可能需要补充专门工具。

- **出处**：Okta<sup>[[1]](#ref-1)</sup>、IDSA<sup>[[9]](#ref-9)</sup>。

### 方案 B：专门的 AI Agent 治理平台（Cyera / BigID / SecurePrivacy + Microsoft Defender for AI）

- **概述**：把 Agent 当作独立治理对象，叠加到 IAM 之上。

- **适用场景**：监管极严、Agent 用例多、需要 AI 专门 risk 视角的企业。

- **优势**：Agent-specific 能力强（discovery、risk scoring、policy enforcement）。

- **劣势**：与传统 IAM 集成需要 SCIM/SAML 桥接；多平台维护成本。

- **出处**：Microsoft Defender for AI<sup>[[7]](#ref-7)</sup>、BigID<sup>[[11]](#ref-11)</sup>。

### 方案 C：「NIST AI RMF Agentic Profile + AAGATE Reference Architecture」自建

- **概述**：以 CSA Agentic Profile + CSA AICM（AI Controls Matrix, 243 controls / 18 domains）+ AAGATE（Kubernetes-native runtime governance）为蓝图，自建治理平台。

- **适用场景**：超大规模科技企业、政府机构、需自主可控的客户。

- **优势**：完全可控、可深度定制、对齐国际标准。

- **劣势**：工程投入巨大；需要持续跟进 NIST/CSA 标准演进。

- **出处**：CSA, NIST RMF Agentic Profile<sup>[[3]](#ref-3)</sup>。

### 方案 D：MCP/A2A Gateway-Centric Agent Identity

- **概述**：以 API Gateway / MCP Gateway 为 PEP（Policy Enforcement Point），所有 Agent 调用通过 Gateway 做 identity 验证、scope 检查、policy 执行。

- **适用场景**：已经在做 API 治理（柱 2）的企业；用例标准化程度高。

- **优势**：单一 PEP 覆盖所有 Agent traffic；统一 audit trail；可与 SIEM 联动。

- **劣势**：Gateway 自身是单点；不能覆盖 Agent 内部 reasoning（只能控制对外动作）。

- **出处**：CSA, MCP Security NIST Profile<sup>[[4]](#ref-4)</sup>（#41）、Salesforce MuleSoft<sup>[[12]](#ref-12)</sup>。

### 选型建议

埃森哲典型客户：**A + B 混合（IAM 平台扩展 + AI 专门治理工具）+ D（API/MCP Gateway 做 PEP）**。方案 C 仅适合 G2G / 国防 / 超大科技。

## 四、风险

1. **「Shadow MCP / Shadow Agent」**：开发者自建 Agent 不走中央治理直接连接生产数据。BigID 把 Shadow AI 列为「最大治理盲区」。对策：unified AI access governance + ISPM 持续 discovery + Mesh/Gateway 默认 deny。出处：BigID<sup>[[11]](#ref-11)</sup>、Okta<sup>[[1]](#ref-1)</sup>。

1. **「过度权限授权」**：图省事给 Agent 服务账号超大权限，违反最小权限原则。Okta：「An agent with a 'viewer' relationship can summarize project documents, but can't export data to external APIs」要求 ReBAC/ABAC 实现真正细粒度。对策：默认 deny + 显式 grant + JIT + scope expiry。

1. **「Prompt Injection / Tool Poisoning」**：通过文档、网页、API 返回值注入恶意指令，操纵 Agent 越权操作。OWASP 把这列为 Agentic Top 10 之首。对策：input sanitization + output filtering + tool 返回值 schema validation + 不可执行外部内容指令。出处：OWASP, State of Agentic AI Security and Governance 1.0<sup>[[5]](#ref-5)</sup>。

1. **「Excessive Agency」**：Agent 在没有人审批的情况下做了高风险操作（删数据、发邮件、转账）。OWASP LLM Top 10 中的核心条目。对策：HITL via CIBA（Client-Initiated Backchannel Authentication）+ 高风险动作强制 2-eye 审批 + tool 白名单 + 动作影响评估。

1. **「Behavioral Drift Undetected」**：Agent 行为随模型更新或上下文变化逐渐漂移，几个月后才被发现，期间所有决策都有偏差。对策：runtime behavioral metrics + autonomy calibration assessment + 定期 red team。出处：CSA, NIST RMF Agentic Profile<sup>[[3]](#ref-3)</sup>。

1. **「Cross-Session Memory Poisoning」**：Agent 跨会话保留 memory，一次被污染影响多次后续会话。对策：memory 加密 + 来源追溯 + 异常检测 + 关键场景禁用持久化 memory。

1. **「Cascading Delegation Accountability Gap」**：Orchestrator Agent 派生 Sub-Agent，出问题后无法追溯到具体责任主体。对策：每个 Agent 动作 trace 必须带完整 delegation chain（caller_id + delegated_scope + reasoning trace）。

1. **「Identity Fragmentation」**：每个 vendor 提供自家 Agent identity 体系，企业里出现 10 套 Agent ID 系统。OpenID 警告：「reduce developer velocity by forcing repeated one-off integrations…compromise security by creating multiple security models」。对策：坚持 OAuth 2.1 + Token Exchange 标准；选支持 IPSIE 的 vendor。出处：OpenID<sup>[[2]](#ref-2)</sup>。

1. **「合规但不安全」陷阱**：通过了 SOC 2 / GDPR 审计但 Agent 实际行为仍然超出预期。对策：把治理动作 instrument 进 Mesh/Gateway，自动化 evidence collection；定期 red team。

## 五、适用场景

**优先重投风险治理 + IAM**：

- 金融、医疗、政府、能源等高合规高风险行业；

- Agent 用例涉及金钱、健康、安全的客户；

- 跨 SaaS / 多云的复杂 IAM 拓扑。

**可分阶段投入**：

- 内部用例为主（员工 productivity Agent）：先做基础 IAM 扩展，监控为辅；

- 中等监管行业：先做 NIST RMF Agentic Profile mapping，再上工具。

**可暂缓**：

- 离线/沙箱用例：风险可控，先用 development-only token；

- 极小规模（< 5 个 Agent）：用 spreadsheet + 手工审计可暂时维持。

## 六、最佳实践案例

### 案例 1：Microsoft Defender NIST-Based Security Framework for AI Agents

**做法**：以 NIST AI RMF 4 函数（GOVERN / MAP / MEASURE / MANAGE）为骨架，在 Microsoft Defender 上落地 Agent 安全治理；与 Microsoft Entra、Microsoft Purview、Microsoft Sentinel 联动。
**关键能力**：Agent discovery、risk scoring、policy enforcement、incident response、audit logging。
**意义**：把通用风险框架变成产品级实现；可作为 Microsoft 生态客户的标杆。
**出处**：Microsoft, Architecting Trust<sup>[[7]](#ref-7)</sup>。

### 案例 2：Palo Alto Networks NIST AI RMF 适配

**做法**：基于 NIST AI RMF 提供 enterprise-grade agentic security 套件——Prisma AIRS、Strata、Prisma Cloud 联合给出 Agent 可见性、风险评估、运行时保护。
**意义**：第一批把 NIST AI RMF 落到全栈安全产品的厂商。
**出处**：Palo Alto Networks, NIST AI RMF Implementation<sup>[[13]](#ref-13)</sup>。

### 案例 3：GovTech Singapore ARC Framework

**做法**：开源框架，三层风险模型——components / design / capabilities；提供 risk → control 映射表；适合做 Agent 上线前的结构化风险评估。
**意义**：政府级 Agent 风险评估的可复用工具，已被多家公共部门采纳。
**出处**：ARC Framework, arXiv 2512.22211<sup>[[8]](#ref-8)</sup>、GovTech ARC Framework<sup>[[14]](#ref-14)</sup>。

### 案例 4：Microsoft WWPS Public Sector Identity Agent

**场景**：公民身份验证 + 福利资格审定，多 Agent 协作（Orchestrator + Document Parsing + Validation + Eligibility）；强合规要求（SNAP 30 天、Medicaid 45/90 天）。
**做法**：Azure AI Document Intelligence + Azure Container Apps + Azure AD + Key Vault；audit & compliance logging 服务捕获完整 decision path；每个 Agent 一个容器，独立 IAM。
**意义**：公共部门 Agent 部署的可复用蓝图；身份 + 风险治理深度整合。
**出处**：Microsoft, Architectural Framework for Agentic AI in Identity & Eligibility<sup>[[15]](#ref-15)</sup>。

### 案例 5：CSA NIST AI RMF Agentic Profile + AAGATE

**蓝图**：4 函数扩展模型 + 243 control AICM + Kubernetes-native runtime governance overlay。
**适用**：超大规模科技、政府、防务客户。
**意义**：可与企业现有 NIST RMF 程序对接的标准化 supplement。
**出处**：CSA Agentic Profile<sup>[[3]](#ref-3)</sup>、CSA AICM<sup>[[4]](#ref-4)</sup>。

### 案例 6：Cyera + SecurePrivacy 数据隐私 + Agent 治理整合

**做法**：以数据为中心，先发现敏感数据 → 再监控 Agent 访问 → 最后做 policy enforcement。
**适用**：医疗、零售、消金。
**出处**：Cyera, Agentic AI Governance<sup>[[16]](#ref-16)</sup>、SecurePrivacy<sup>[[17]](#ref-17)</sup>。

---

下一节：柱 5：人才 / 组织设计

---

## 参考文献

<a id="ref-1"></a>1. [Okta, The Role of AI in IAM](https://www.okta.com/identity-101/ai-in-iam/)

<a id="ref-2"></a>2. [OpenID, AI Identity, Authentication, and Authorization Whitepaper](https://openid.net/wordpress-content/uploads/2025/10/AI-Identity-and-AuthN-AuthZ-Whitepaper.pdf)

<a id="ref-3"></a>3. [CSA, NIST AI Risk Management Framework: Agentic Profile](https://labs.cloudsecurityalliance.org/research/nist-ai-rmf-agentic-profile/)

<a id="ref-4"></a>4. [CSA, Agentic Trust Framework](https://cloudsecurityalliance.org/research/topics/ai-safety-initiative)

<a id="ref-5"></a>5. [OWASP, State of Agentic AI Security and Governance 1.0](https://genai.owasp.org/resource/state-of-agentic-ai-security-and-governance-1-0/)

<a id="ref-6"></a>6. [OWASP AI Exchange](https://owaspai.org/)

<a id="ref-7"></a>7. [Microsoft, Architecting Trust: A NIST-Based Security Governance Framework for AI Agents](https://techcommunity.microsoft.com/blog/microsoftdefendercloudblog/architecting-trust-a-nist-based-security-governance-framework-for-ai-agents/4490556)

<a id="ref-8"></a>8. [ARC Framework](https://arxiv.org/html/2512.22211v1)

<a id="ref-9"></a>9. [IDSA, IAM Implications of AI in 2025](https://www.idsalliance.org/blog/iam-implications-of-ai-in-2025/)

<a id="ref-10"></a>10. [Dynamisch, 6 Critical Realities](https://dynamisch.co/insights/blogs/agentic-ai-enterprise-implementation-guide)

<a id="ref-11"></a>11. [BigID](https://bigid.com/blog/agentic-ai-governance-trends/)

<a id="ref-12"></a>12. [Salesforce MuleSoft](https://www.salesforce.com/blog/mulesoft-omni-gateway-agentic-ai-governance/)

<a id="ref-13"></a>13. [Palo Alto Networks, NIST AI RMF Implementation](https://www.paloaltonetworks.com/blog/2026/05/agentic-ai-nist-rmf/)

<a id="ref-14"></a>14. [GovTech ARC Framework](https://medium.com/govtech-singapore/arc-framework)

<a id="ref-15"></a>15. [Microsoft, Architectural Framework for Agentic AI in Identity & Eligibility](https://techcommunity.microsoft.com/blog/publicsectorblog/architectural-framework-for-agentic-ai-in-identity-eligibility/4490333)

<a id="ref-16"></a>16. [Cyera, Agentic AI Governance](https://www.cyera.com/blog/agentic-ai-governance-frameworks)

<a id="ref-17"></a>17. [SecurePrivacy](https://secureprivacy.ai/blog/agentic-ai-governance)
