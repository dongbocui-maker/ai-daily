---
order: 10
slug: conclusion
docNum: "10 · 总结"
docColor: conclusion
title: "协同矩阵+成熟度评估+路线图"
feishuToken: IIJAdnWVNofjqwxsA9Ucu6uenAg
words: "~9K 字"
---
# 结论：一个底座 + 七大基础设施的协同 + 客户成熟度评估 + 落地路线图

> 本节综合前 8 板块（00-08），以三个交付物收束全文：①七柱协同矩阵 ②客户成熟度评估表（5 级 × 8 维度 = 40 评估点） ③埃森哲 90/180/365 天 + 24 个月落地路线图。

## 一、为什么是"一个底座 + 七柱"

Dynamisch 引述的 2026 年数据点反复指向同一个结构性事实：

- **79% 企业已经在部署 Agent，仅 11% 进入生产**——20 倍的"想做 vs 能做"鸿沟。

- **Gartner：到 2027 年底 >40% agentic AI 项目会被取消**——半数现在的投入会被砍。

- **MIT/BCG：95% 组织 AI 投资零回报**（MIT NANDA Initiative 2025）。

- **S&P Global：42% 企业放弃 AI 项目，比上年 17% 翻 2.5 倍**。

- **MIT/BCG 数据 N=2,102 跨 21 行业 116 国：47% 企业没有 AI 战略**（MIT Sloan, The Emerging Agentic Enterprise）。

把这些数字摆在一起，一个清晰的结论浮现：**Agentic AI 落地失败的根因，不是模型不够强，也不是 framework 选错，而是企业基础设施跟不上 Agent 自主行为带来的结构性需求。**

更具体地——

| 失败模式 | 缺失的柱 |
| --- | --- |
| Agent 不知道企业里有什么数据 | 底座（数据治理 + 知识管理） |
| Agent 调用接口失败、行为不一致 | 柱 2（API 治理）+ 柱 1（架构） |
| Agent 输出错了没人发现 | 柱 3（LLMOps / AgentOps） |
| Agent 做了越权操作 | 柱 4（风险治理 + IAM） |
| 员工不愿意用、不会用 | 柱 5（人才组织）+ 柱 6（变革管理） |
| Board 看不到 ROI，预算被砍 | 柱 7（FinOps / ROI） |

任何一柱缺位，都会成为整体落地的木桶短板。**这是为什么我们说"一个底座 + 七大基础设施"是 minimum viable set，不是 nice-to-have。**

## 二、七柱协同矩阵

每一柱独立都是必要条件，但**真正的杠杆来自跨柱协同**。下表列出常见的协同模式：

| 协同方向 | 协同动作 | 价值 |
| --- | --- | --- |
| **底座 ↔ 柱 1 架构** | 知识图谱 + RAG 支撑 Agent 推理 | Agent 决策"有据可循" |
| **底座 ↔ 柱 4 风险/IAM** | 数据敏感度标签自动驱动 Agent 访问策略 | 零信任落到数据级 |
| **柱 1 架构 ↔ 柱 2 API 治理** | MCP/A2A 协议 + API Gateway 统一 PEP | 单点治理多 Agent 调用 |
| **柱 2 API 治理 ↔ 柱 4 IAM** | Gateway 验证 Agent identity + scope | 防越权 + Shadow Agent |
| **柱 1 架构 ↔ 柱 3 LLMOps** | Trace 数据回流改进 prompt + 模型 routing | 持续优化 |
| **柱 3 LLMOps ↔ 柱 4 风险** | Behavioral drift 数据驱动 risk 检测 | 主动风险防御 |
| **柱 3 LLMOps ↔ 柱 7 FinOps** | Token / step 数据驱动成本归因 | TCO 可视 |
| **柱 4 风险 ↔ 柱 5 人才** | SME 参与 red team + HITL approval | 治理 + 人深度结合 |
| **柱 5 人才 ↔ 柱 6 变革** | Champion network + dual career path | 持续采用 |
| **柱 6 变革 ↔ 柱 7 FinOps** | ROI scorecard 公开化 + 内部传播 | 内部说服力 |
| **柱 7 FinOps ↔ 战略层** | Anchor in value 框架与 Board / CFO 对话 | 长期 sustainability |

### 跨柱失败的典型模式

- **「装了 Mesh，没接 IAM」**：架构有了 Mesh，但 Mesh 没接到中央 IAM，依旧 Shadow Agent 横行。

- **「LLMOps 有了，没接 FinOps」**：Trace 数据躺在 Galileo 里，没回流到云账单归因，CFO 看不到成本来源。

- **「治理框架有了，没接变革」**：CSA AICM 243 控制点写完没人执行，员工照常 bypass。

- **「人才升级了，没接平台」**：员工受训完没有平台可用，技能荒废。

## 三、客户成熟度评估表（5 级 × 8 维度 = 40 评估点）

适用场景：埃森哲 client engagement 第一阶段 assessment / discovery；客户 self-assessment；M&A 尽调 AI maturity。

**成熟度分级**：

- **L1 Initial（试点散兵）**：单点用例、个人探索、无平台无治理

- **L2 Developing（部门级）**：1-3 个部门有 Agent 应用，初步治理

- **L3 Defined（企业级标准）**：跨部门标准化、平台化、有治理框架

- **L4 Managed（持续优化）**：闭环改进、ROI 可衡量、风险量化

- **L5 Optimizing（行业引领）**：行业最佳实践、对外赋能、生态贡献

### 评估矩阵

| 维度 | L1 Initial | L2 Developing | L3 Defined | L4 Managed | L5 Optimizing |
| --- | --- | --- | --- | --- | --- |
| **底座：数据 / 知识** | 数据散落、无 metadata | 部门数据目录 | 企业 data catalog + 知识图谱 | RAG 半成品级 + 持续清理 | 数据-Agent 协同进化 |
| **柱 1：架构** | 单 Agent 单用例 | 简单多 Agent | MCP/A2A 标准化 | Agentic Mesh 全面 | 行业级开放生态 |
| **柱 2：API 治理** | 无统一 Gateway | 部分 API on Gateway | Omni Gateway / MCP Gateway 统一 | LLM/Agent 流量全治理 | API + Agent Marketplace |
| **柱 3：LLMOps / AgentOps** | 手工 review | 简单 logging | LLMOps 平台部署 | Continuous evaluation 闭环 | 自研评估模型 |
| **柱 4：风险 / IAM** | Agent 用人凭证 | Agent NHI 注册 | OAuth 2.1 + ReBAC + ISPM | NIST RMF Agentic Profile 落地 | 行业贡献安全标准 |
| **柱 5：人才 / 组织** | 个别 enthusiast | AI literacy 培训 | Dual career path + HR 系统更新 | Agentic Org 操作 | 输出方法论 |
| **柱 6：变革管理** | 临时通讯 | 试点级 training | 全员 CM 计划 + champion network | Feedback closed loop + 持续迭代 | 内外部 case study 输出 |
| **柱 7：FinOps / ROI** | LLM bill 累加看 | Per-use-case budget | TCO + 4 类 ROI 框架 | Showback/Chargeback | Value 经营层面议程 |

**评估打分方法**：每个维度按 L1=1, L2=2, ..., L5=5 打分，总分 8-40。

- 8-15：Early Stage——主攻底座 + 柱 1

- 16-23：Building Stage——补齐治理三柱（2/3/4）

- 24-31：Scaling Stage——重点投人 + ROI（柱 5/6/7）

- 32-40：Advanced / Industry-Leading——选择性深耕 + 对外赋能

**评估输出**：雷达图 + 短板诊断 + 优先级排序 + 12-24 个月路线图。这是埃森哲 engagement 第一周交付物。

## 四、埃森哲 90 / 180 / 365 天 + 24 个月落地路线图

### 第 0-90 天：Assess & Foundation

**核心动作**：

1. **客户 8 维度成熟度评估**（上表）；输出 baseline + gap report。

1. **选 1-2 个 High-Value Use Case**（PoC 级），通过 Value Hypothesis Filter：①P&L 锚点 ②12 个月 NPV ③不做的机会成本。

1. **建立 Agentic CoE**（柱 5）：埃森哲 + 客户混编，跨 IT/Business/HR/Compliance。

1. **底座 quick win**：选 1-2 个数据域做 metadata + access control + RAG 试点（柱 0）。

1. **基础治理框架**：选 NIST RMF Agentic Profile 或 CSA Agentic Trust 作为 baseline（柱 4）。

1. **沟通 & 高管对齐**：Town hall + Board sponsor sign-off + Value Hypothesis 公示（柱 6）。

**交付物**：

- 成熟度评估报告

- PoC 用例 Value Hypothesis 文档

- Agentic CoE charter

- 90/180/365 路线图（带 Go/No-Go gates）

### 第 91-180 天：Pilot & Govern

**核心动作**：

1. **PoC → Pilot 转化**：上面 1-2 个用例从沙箱 → controlled production；user 数从 10 → 100。

1. **平台奠基**：MCP/A2A gateway + 中央 LLMOps 平台 + IAM 扩展（柱 1/2/3/4）。

1. **数据底座深化**：扩展到 3-5 个数据域；建立 enterprise knowledge graph；上 RAG 评估闭环（底座）。

1. **治理操作化**：风险评估常态化 + Agent 注册流程 + HITL via CIBA + ISPM dashboard（柱 4）。

1. **培训系统化**：3 段差异化课程上线（Executive / SME / End User）；选定 champion network（柱 5/6）。

1. **FinOps 体系搭建**：TCO dashboard + Per-use-case budget + Showback（柱 7）。

**Go/No-Go Gate**（180 天）：

- 至少 1 个用例进入 production

- ROI 达到 Value Hypothesis 60% 以上

- 治理框架基线运行

- 培训完成率 70% 以上

- TCO 透明可查

### 第 181-365 天：Scale & Optimize

**核心动作**：

1. **用例规模化**：从 1-2 个扩到 5-10 个；建立用例 portfolio + intake 流程。

1. **Agentic Mesh 落地**：架构层从 quick-fix 升级到 Mesh（柱 1）。

1. **API Marketplace + MCP Marketplace**：标准化、自助式 Agent 部署（柱 2）。

1. **AgentOps 闭环**：Continuous evaluation + Behavioral drift detection + Auto-rollback（柱 3）。

1. **NIST RMF Agentic Profile 全面落地** + 与 SOC/SIEM 联动（柱 4）。

1. **Dual Career Path 上线**：HR 系统更新 + 晋升体系试运行（柱 5）。

1. **变革管理深化**：从 training-centric → community-centric；MGM/Product CoP 建立（柱 6）。

1. **ROI 4 类衡量框架**全面落地（柱 7）：每用例都有 4 类指标，每季度 review。

**Go/No-Go Gate**（365 天）：

- ≥ 5 个用例 production

- ROI 总额 > 平台投入 1.5x

- 治理事件 < 阈值

- 员工 NPS > baseline + 10

- TCO 可控（不超预算 ±15%）

### 第 366-720 天（第 13-24 个月）：Industrialize & Differentiate

**核心动作**：

1. **从用例 → 产品**：把高 ROI 用例打包成可对外销售/可跨业务部门复用的"Agent product"。

1. **Agentic Organization 转型**：组织结构正式调整（spans of control widen + middle management redefined + role transformation）（柱 5）。

1. **AI Agent Marketplace**（内部）：让业务部门 self-service 申请 Agent；CoE 转型为 enabler 而非 gatekeeper（柱 2/5）。

1. **数据 / 知识资产**：从 Agent 反哺数据；Active learning 闭环；数据 = 公司资产负债表项目（底座）。

1. **生态贡献**：行业大会 / 标准组织（OWASP/CSA/NIST/OpenID）贡献最佳实践；reposition 为行业引领者。

1. **对外销售**：把内部 Agentic 能力 productize；输出咨询服务（这是埃森哲核心商业模式落点）。

**Gate**（24 个月）：

- 10+ 用例 production；3+ 已升级为"product"

- Agent leverage 进入员工 KPI 主线

- Board 把 AI 当作核心战略议程

- 行业声誉提升（媒体、分析师认可）

- 客户/合作伙伴关系强化

## 五、给埃森哲 MD 的最后 5 条建议

1. **Value Anchoring 不可妥协**：每一个用例必须能映射到 P&L；Board 视角下，95% 零回报是悬剑。把 ROI Hypothesis 文档化、可追踪、公开化。出处：BCG。

1. **变革管理预算 = 技术预算的 1-1.5x**：购牌照 + 短训 不能让人真用起来。70% 数字化变革失败的根因是人。这是 AI Monks 反复警告的内容。出处：AI Monks。

1. **底座先行**：数据/知识不就绪，七柱都是 nice-to-have。「You cannot agent your way out of a data mess」（Dynamisch / Acceldata）。出处：Dynamisch。

1. **治理与速度不是对立面**：CSA NIST RMF Agentic Profile + OpenID delegation flows + OAuth 2.1 token exchange——都是为了让 Agent 跑得更快更稳，不是限制创新。监管即将到来；现在投资治理是降低未来摩擦。出处：CSA、OpenID。

1. **「内部先用」是埃森哲独特优势**：用 myConcierge 这种内部 Agentic 平台先在自家 70 万员工上验证，再向客户输出方法论 + 平台 + 实战案例。这是其他咨询公司难以复制的杠杆。出处：ZenML, Accenture Internal Agentic AI Platform。

---

## 六、阅读与扩展建议

本文档基于 60 个权威源材料编写，可作为：

- **Board / CFO 沟通蓝本**（重点：00 引言 + 99 结论 + 各柱「重要性综述」）

- **CIO / CTO 技术规划基础**（重点：02 架构 + 03 API 治理 + 04 LLMOps）

- **CSO / CRO 风险评估清单**（重点：05 风险 IAM + CSA / OWASP / NIST 链接）

- **CHRO / Change Mgmt 行动手册**（重点：06 人才 + 07 变革管理）

- **CFO / FinOps lead 衡量框架**（重点：08 FinOps + 99 路线图）

**延伸阅读优先级**：

1. CSA NIST AI RMF Agentic Profile — 最完整的风险治理 supplement

1. McKinsey Agentic Organization — 最系统的组织演化论

1. arXiv 2512.08769 九大铁律 — 最具操作性的工程实践

1. BCG Building Effective Enterprise Agents — 最完整的 4 章节企业 agent 框架

1. ZenML 457 LLMOps Cases — 最大公开生产案例库

1. OpenID AI Identity Whitepaper — 最权威的 Agent 身份标准

---

**致 Jason / 埃森哲团队**：本研究希望为你在客户对话中提供"既有深度又能落地"的结构化弹药。每一柱都有 5-8 个具体动作可在 90 天内启动；每一个动作都有 1-3 个真实案例可引用。最重要的——**不是哪一柱最重要，而是 8 柱不能缺一**。

— 文档结束 —
