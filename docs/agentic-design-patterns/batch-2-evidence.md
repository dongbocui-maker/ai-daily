# 批次二引文证据台账（Pattern 8-14）

- 核验方法：`/tmp/verify_quote.py`——将引文与全文均做空白正规化（连续空白折叠为单空格，剔除零宽字符；不改动任何词句），在全文中做**完整子串匹配**，输出匹配的原文行号范围与出现次数。全部引文按整段核验，不以首 N 词命中代替。
- 源文件：
  - `2025全文` = `/root/.openclaw/workspace/obsidian-export/books/agentic-design-patterns-2025.txt`
  - `2026全文` = `/root/.openclaw/workspace/obsidian-export/books/ai-design-2026.txt`
  - 章节文件（`chapters/chNN.txt`）仅用于阅读定位，所有引文核验一律回全文。
- 判定标记：✅ = FOUND FULL PASSAGE（整段完整匹配，仅空白正规化）。

## Pattern 8 · Memory Management（ch08，2025全文 Chapter 8 区段）

| # | 草稿位置 | 引文（首词…尾词） | 源文件 | 全文行号 | 结果 |
|---|---|---|---|---|---|
| 8-1 | 模式定义 | "In agent systems, memory refers … improve over time." | 2025全文 | 5062-5065 | ✅ 整段匹配，出现 1 次 |
| 8-2 | 模式定义 | "However, this context is still ephemeral … lasting knowledge base." | 2025全文 | 5079-5083 | ✅ 整段匹配，出现 1 次 |
| 8-3 | 模式定义 | "In vector databases, information is converted … semantic search." | 2025全文 | 5088-5091 | ✅ 整段匹配，出现 1 次 |
| 8-4 | 三种长期记忆 | "Semantic Memory: Remembering Facts: … domain knowledge." | 2025全文 | 5709-5710 | ✅ 整段匹配，出现 1 次 |
| 8-5 | 三种长期记忆 | "Procedural Memory: Remembering Rules: … system prompt." | 2025全文 | 5724-5726 | ✅ 整段匹配，出现 1 次 |
| 8-6 | 关键工程细节 | "Note that direct modification of the \`session.state\` … timestamps." | 2025全文 | 5470-5474 | ✅ 整段匹配，出现 1 次 |
| 8-7 | 关键工程细节 | "Memory Bank, a managed service … key facts and user preferences." | 2025全文 | 5824-5826 | ✅ 整段匹配，出现 1 次 |
| 8-8 | Rule of Thumb | "Use this pattern when an agent needs to do more than answer a single question. … newly acquired information."（含 "Rule of thumb:" 前缀一并核验） | 2025全文 | 5887-5892 | ✅ 整段匹配，出现 1 次 |
| 8-9 | 🆕 2026 补充 | "The InMemorySessionService gives the Agent a temporary, short-term memory (like RAM). … wiped clean when the script stops." | 2026全文 | 12366-12368 | ✅ 整段匹配，出现 1 次（Appendix G） |

- 中文提炼边界说明：8-1/8-2/8-3/8-6/8-7/8-9 的中文提炼均只覆盖对应引文本身；情景记忆（Episodic）条目为转述（原文 2025全文 5716-5722），未作为引文块呈现故不入引文台账，但已回原文确认转述与原文一致（few-shot example prompting 表述来自原文）。
- 🆕 2026 补充定位：《AI Design》Appendix G "Developing Agents with Google ADK"，2026全文 12366-12368 行；该书无更深记忆架构内容，草稿中已如实说明。
- 2026 现状对照段：标记为编辑判断，无 2026 书引文，不涉及核验。

## Pattern 9 · Learning and Adaptation（ch09，2025全文 Chapter 9 区段）

| # | 草稿位置 | 引文（首词…尾词） | 源文件 | 全文行号 | 结果 |
|---|---|---|---|---|---|
| 9-1 | 模式定义 | "Agents learn and adapt by changing … smarter over time." | 2025全文 | 5982-5984 | ✅ 整段匹配，出现 1 次 |
| 9-2 | PPO 与 DPO | "In essence, DPO simplifies alignment … more efficient and robust." | 2025全文 | 6070-6073 | ✅ 整段匹配，出现 1 次 |
| 9-3 | SICA 案例 | "This contrasts with traditional approaches … various coding challenges." | 2025全文 | 6114-6117 | ✅ 整段匹配，出现 1 次 |
| 9-4 | SICA 案例 | "An asynchronous overseer, another LLM, … halt execution if necessary." | 2025全文 | 6164-6166 | ✅ 整段匹配，出现 1 次 |
| 9-5 | Rule of Thumb | "Rule of thumb: Use this pattern when building agents … novel situations autonomously." | 2025全文 | 6317-6320 | ✅ 整段匹配，出现 1 次 |
| 9-6 | 🆕 2026 补充 | "This is the cutting-edge idea behind Reinforcement Learning from AI Feedback (RLAIF). … a smaller \"student\" AI model." | 2026全文 | 6809-6812 | ✅ 整段匹配，出现 1 次（Chapter 14） |
| 9-7 | 🆕 2026 补充 | "Before the AI even starts its real training, we hand the instructor AI a constitution … when making decisions." | 2026全文 | 6824-6825 | ✅ 整段匹配，出现 1 次（Chapter 14） |

- 转述内容核验说明：六条学习路径清单（RL/监督/无监督/few-shot/在线/记忆学习）为原文 bullet 列表的忠实转述（2025全文 5987-6008 行区段）；PPO 两步 RLHF 流程与"hack the reward model"风险为原文转述（6040-6055 行区段）；AlphaEvolve 成果数字（0.7%/23%/32.5%/48 次标量乘法/50+ 开放问题 75%/20%）逐项对照原文 Chapter 9 AlphaEvolve 小节确认一致；SICA 工具进化链（Smart Editor→Diff-Enhanced→AST Symbol Locator 等）与 Docker 隔离、可观测界面描述对照原文确认。SICA 标注为公开研究（arXiv:2504.15228，原书 References 5）而非商业部署。
- 🆕 2026 补充定位：《AI Design》Chapter 14 "AI Teaching AI: The Future with RLAIF"（2026全文 6784 行起）；RLHF vs RLAIF 对比（"slow, expensive, but human judgment" vs "fast, scalable, but AI judgment"）见 6840-6843 行。
- 2026 现状对照段：标记为编辑判断。

## Pattern 10 · Model Context Protocol（ch10，2025全文 Chapter 10 区段）

| # | 草稿位置 | 引文（首词…尾词） | 源文件 | 全文行号 | 结果 |
|---|---|---|---|---|---|
| 10-1 | 模式定义 | "It's an open standard designed to standardize … interact with various systems." | 2025全文 | 6414-6418 | ✅ 整段匹配，出现 1 次 |
| 10-2 | 两条警告 | "However, MCP is a contract for an \"agentic interface,\" … suboptimal for an agent." | 2025全文 | 6427-6430 | ✅ 整段匹配，出现 1 次 |
| 10-3 | 两条警告 | "This highlights that agents do not magically replace deterministic workflows … to succeed." | 2025全文 | 6434-6436 | ✅ 整段匹配，出现 1 次 |
| 10-4 | 两条警告 | "An API is only useful if its data format is agent-friendly … cannot parse PDF content." | 2025全文 | 6443-6446 | ✅ 整段匹配，出现 1 次 |
| 10-5 | MCP vs 函数调用 | "In short, function calling provides direct access … a universal standard like MCP is essential." | 2025全文 | 6527-6531 | ✅ 整段匹配，出现 1 次 |
| 10-6 | 安全与部署 | "Security: Exposing tools and data via any protocol … permitted to perform." | 2025全文 | 6549-6552 | ✅ 整段匹配，出现 1 次 |
| 10-7 | Rule of Thumb | "Rule of thumb: Use the Model Context Protocol (MCP) when building complex … may be sufficient."（含前缀核验，长引文 532 字符） | 2025全文 | 6997-7003 | ✅ 整段匹配，出现 1 次 |
| 10-8 | 🆕 2026 补充 | "Now, thanks to MCP (standardized by Anthropic) … they all just work." | 2026全文 | 12393-12395 | ✅ 整段匹配，出现 1 次（Appendix G） |
| 10-9 | 🆕 2026 补充 | "They can't tackle big jobs without working together: A2A handles the teamwork, and MCP handles the tools." | 2026全文 | 12430-12431 | ✅ 整段匹配，出现 1 次（Appendix G） |

- 转述内容核验说明：五维对比表（Standardization/Scope/Architecture/Discovery/Reusability）为原文表格的忠实压缩转述（2025全文 Chapter 10 "MCP vs. Tool Function Calling" 表格区段）；工单系统例子、resource/tool/prompt 三分、本地/远程部署与 STDIO/HTTP/SSE 传输层描述均对照原文 "Additional considerations for MCP" 小节确认；联邦模式表述（"federated model...wrapping them in an MCP-compliant interface...without requiring costly rewrites"）对照原文 6510-6520 行区段确认为忠实转述。
- 🆕 2026 补充定位：《AI Design》Appendix G: Developing Agents with Google ADK（2026全文 12136 行起）的 "MCP and A2A" 小节（2026全文 12385-12431 行）；Manager/Finance Agent 协作示例见 12414-12429 行（注意原文 12420 行将 MCP 误展开为 "Model-Controller-Pattern"，系原书笔误，草稿未沿用该展开）。
- 2026 现状对照段：标记为编辑判断（MCP 供应链风险为编辑提示，非原书内容）。

## Pattern 11 · Goal Setting and Monitoring（ch11，2025全文 Chapter 11 区段）

| # | 草稿位置 | 引文（首词…尾词） | 源文件 | 全文行号 | 结果 |
|---|---|---|---|---|---|
| 11-1 | 模式定义 | "It's about giving agents specific objectives … objectives have been met." | 2025全文 | 7067-7069 | ✅ 整段匹配，出现 1 次 |
| 11-2 | 示例批判 | "An LLM may not fully grasp the intended meaning of a goal … going in the wrong direction." | 2025全文 | 7469-7473 | ✅ 整段匹配，出现 1 次 |
| 11-3 | 示例批判 | "Ultimately, LLMs do not produce flawless code by magic … running forever." | 2025全文 | 7475-7477 | ✅ 整段匹配，出现 1 次 |
| 11-4 | 修正方向 | "In this multi-agent system, the Code Reviewer … significantly improves objective evaluation." | 2025全文 | 7516-7518 | ✅ 整段匹配，出现 1 次 |
| 11-5 | Rule of Thumb | "Rule of thumb: Use this pattern when an AI agent must autonomously execute … without constant human intervention." | 2025全文 | 7545-7547 | ✅ 整段匹配，出现 1 次 |
| 11-6 | SMART 准则 | "Goals should be specific, measurable, achievable, relevant, and time-bound (SMART)." | 2025全文 | 7565-7566 | ✅ 整段匹配，出现 1 次 |

- 转述内容核验说明：旅行规划类比、六个应用场景（客服/学习/项目管理/交易/自动驾驶/内容审核）的"目标+监控信号+兜底动作"结构、示例代码流程（生成→自评→True/False→迭代上限 5 轮）、作者五角色 crew（Peer Programmer/Code Reviewer/Documenter/Test Writer/Prompt Refiner）均对照原文 Chapter 11 确认为忠实转述。示例已在草稿中标注为"书中假设场景，非真实部署"（原书自述 "exemplary illustration and not production-ready code"）。
- 🆕 2026 补充：已查证《AI Design》全书（含 Bonus Ch18 与各 Appendix），无目标设定与监控对应增量，草稿如实注明"无增量、不硬凑"。
- 2026 现状对照段：标记为编辑判断。

## Pattern 12 · Exception Handling and Recovery（ch12，2025全文 Chapter 12 区段）

| # | 草稿位置 | 引文（首词…尾词） | 源文件 | 全文行号 | 结果 |
|---|---|---|---|---|---|
| 12-1 | 模式定义 | "The Exception Handling and Recovery pattern addresses the need … strategies to mitigate them." | 2025全文 | 7631-7633 | ✅ 整段匹配，出现 1 次 |
| 12-2 | 模式定义 | "Additionally, the pattern emphasizes recovery mechanisms … stable operation." | 2025全文 | 7637-7639 | ✅ 整段匹配，出现 1 次 |
| 12-3 | 与反思联动 | "This pattern may sometimes be used with reflection. … to resolve the error." | 2025全文 | 7624-7627 | ✅ 整段匹配，出现 1 次 |
| 12-4 | 错误检测面 | "This could manifest as invalid or malformed tool outputs … deviate from expected formats." | 2025全文 | 7652-7655 | ✅ 整段匹配，出现 1 次 |
| 12-5 | 状态回滚 | "It could involve reversing recent changes or transactions … vital for preventing recurrence." | 2025全文 | 7672-7674 | ✅ 整段匹配，出现 1 次 |
| 12-6 | Rule of Thumb | "Rule of thumb: Use this pattern for any AI agent deployed in a dynamic … a key requirement." | 2025全文 | 7813-7815 | ✅ 整段匹配，出现 1 次 |

- 核验备注：初稿曾选一段跨 PDF 分页（页码字符"1"插入段中，2025全文 7632-7636 行）的引文，整段匹配失败——**未以前缀命中充当验证**，改选两段不跨页引文（12-1/12-2）替代，语义覆盖相同内容。
- 转述内容核验说明：检测/处理/恢复三阶段框架、五类处理手段、ADK SequentialAgent 三级降级示例（primary_handler→fallback_handler→response_agent，经 state["primary_location_failed"] 传递失败信号）均对照原文 Chapter 12 确认为忠实转述；示例标注为书中示例非真实部署。
- 🆕 2026 补充：已查证《AI Design》，无对应增量，草稿如实注明。
- 2026 现状对照段：标记为编辑判断。

## Pattern 13 · Human-in-the-Loop（ch13，2025全文 Chapter 13 区段）

| # | 草稿位置 | 引文（首词…尾词） | 源文件 | 全文行号 | 结果 |
|---|---|---|---|---|---|
| 13-1 | 模式定义 | "In such scenarios, full autonomy—where AI systems function independently … remain indispensable." | 2025全文 | 7880-7884 | ✅ 整段匹配，出现 1 次 |
| 13-2 | 升级策略 | "Escalation Policies are established protocols … beyond the agent's capability." | 2025全文 | 7930-7932 | ✅ 整段匹配，出现 1 次 |
| 13-3 | 三大硬约束 | "Despite its benefits, the HITL pattern has significant caveats … cannot manage millions of tasks" | 2025全文 | 7941-7943 | ✅ 整段匹配，出现 1 次 |
| 13-4 | 三大硬约束 | "Furthermore, the effectiveness of this pattern is heavily dependent … correct guidance to fix them." | 2025全文 | 7947-7950 | ✅ 整段匹配，出现 1 次 |
| 13-5 | 三大硬约束 | "Lastly, implementing HITL raises significant privacy concerns … layer of process complexity." | 2025全文 | 7952-7955 | ✅ 整段匹配，出现 1 次 |
| 13-6 | Human-on-the-loop | "\"Human-on-the-loop\" is a variation of this pattern … to ensure compliance." | 2025全文 | 8005-8006 | ✅ 整段匹配，出现 1 次 |
| 13-7 | Rule of Thumb | "Rule of thumb: Use this pattern when deploying AI in domains where errors have significant … customer support escalations."（取前两句，句边界完整） | 2025全文 | 8159-8163 | ✅ 整段匹配，出现 1 次 |
| 13-8 | 🆕 2026 补充 | "The fundamental problem in AI coding is trust. … major source of frustration." | 2026全文 | 13596-13598 | ✅ 整段匹配，出现 1 次（Appendix I） |
| 13-9 | 🆕 2026 补充 | "Artifacts are analogous to a math student showing their work. … led to the solution." | 2026全文 | 13599-13601 | ✅ 整段匹配，出现 1 次（Appendix I） |

- 核验备注：Caveats 整段（"...HITL for accuracy."）跨 PDF 分页（页码"2"插入段中），整段匹配失败——未以前缀命中充当验证，拆为三段不跨页引文（13-3/13-4/13-5）分别核验，未损失原意。13-7 的 Rule of thumb 原文共三句，草稿引前两句（省略第三句关于训练数据/生成内容 refinement 的句子），在句号处截断，属完整句边界省略，非中途截断。
- 转述内容核验说明：六种实现形态（Oversight/Intervention/Feedback/Decision Augmentation/Collaboration/Escalation）、交易系统与呼叫中心两个 on-the-loop 例子（含 70%/30%、5%、10% 数字）、ADK 三工具示例（troubleshoot_issue/create_ticket/escalate_to_human）均对照原文 Chapter 13 确认为忠实转述；示例标注为书中示例非真实部署。
- 🆕 2026 补充定位：《AI Design》Appendix I "Guide to Google Antigravity" Part 3（2026全文 13595-13627 行，Artifacts 三形态：可编辑 Plan/Screenshots/Video Replay）；另引 Chapter 10 幻觉治理语境下的 HITL 表述（5512-5514 行，草稿中为带行号的转述而非引文块）。
- 2026 现状对照段：标记为编辑判断。

## Pattern 14 · Knowledge Retrieval / RAG（ch14，2025全文 Chapter 14 区段）

| # | 草稿位置 | 引文（首词…尾词） | 源文件 | 全文行号 | 结果 |
|---|---|---|---|---|---|
| 14-1 | 模式定义 | "RAG enables LLMs to access and integrate external … factual basis of their outputs." | 2025全文 | 8222-8224 | ✅ 整段匹配，出现 1 次 |
| 14-2 | 结构性短板 | "A primary issue arises when the information needed … incomplete or inaccurate answer." | 2025全文 | 8356-8360 | ✅ 整段匹配，出现 1 次 |
| 14-3 | 结构性短板 | "Consequently, this knowledge requires periodic reconciliation … tokens used in the final prompt." | 2025全文 | 8369-8372 | ✅ 整段匹配，出现 1 次 |
| 14-4 | GraphRAG | "A key advantage is its ability to synthesize answers … common failing of traditional RAG." | 2025全文 | 8390-8392 | ✅ 整段匹配，出现 1 次 |
| 14-5 | GraphRAG | "The primary drawback, however, is the significant complexity … high-quality knowledge graph." | 2025全文 | 8396-8398 | ✅ 整段匹配，出现 1 次 |
| 14-6 | Agentic RAG | "Instead of just retrieving and augmenting, an \"agent\" … illustrated by the following scenarios." | 2025全文 | 8409-8413 | ✅ 整段匹配，出现 1 次 |
| 14-7 | Agentic RAG 代价 | "Furthermore, the agent itself can become a new source of error … quality of the final response." | 2025全文 | 8460-8463 | ✅ 整段匹配，出现 1 次 |
| 14-8 | Rule of Thumb | "Rule of thumb: Use this pattern when you need an LLM to answer questions … fact-based responses with citations." | 2025全文 | 8761-8765 | ✅ 整段匹配，出现 1 次 |
| 14-9 | 🆕 2026 补充 | "Look Outside for Data (RAG or Retrieval Augmented Generation): … often called \"hallucinations\")." | 2026全文 | 5507-5511 | ✅ 整段匹配，出现 1 次（Chapter 10） |

- 转述内容核验说明：Embeddings/文本相似度/语义距离/Chunking/向量数据库五个核心概念（含 cat/kitten/car 坐标例、furry feline companion 例、HNSW、BM25 与混合搜索、Pinecone/Weaviate/Chroma/Milvus/Qdrant/pgvector/FAISS/ScaNN 工具名单）对照原文 Chapter 14 概念区段确认为忠实转述；Agentic RAG 四场景（2020 博客 vs 2025 政策、€50,000 vs €65,000、竞品对比四子查询、周更知识库 + web 搜索补漏）对照原文确认并在草稿中标注"书中假设场景"；GraphRAG 适用场景（金融分析/基因与疾病）对照原文确认。
- 🆕 2026 补充定位：《AI Design》Chapter 10 "The 'Making Stuff Up' Problem" 幻觉治理清单（2026全文 5501-5520 行），四项手段排序（RAG→HITL→置信度警示→更好的训练数据）为原文结构的忠实转述。
- 2026 现状对照段：标记为编辑判断。
