# AI 日报精读 JSON Schema + QC Acceptance Criteria

> 用于 MK46 QC Auditor 审查精读 JSON 的标准
> 此 schema 是项目实际使用的版本，与 Astro 渲染层一致
> 历史 23 篇精读 JSON 全部符合本 schema
> 立项日期：2026-05-25

## 文件命名规则

```
src/data/reads/YYYY-MM-DD-<slug>.json
```

- 日期前缀（`YYYY-MM-DD-`）是创建日期，不是 `publishDate`
- `<slug>` 是 kebab-case，全英文小写
- 例：`2026-05-25-anthropic-project-vend-2.json`

## 必需字段（mandatory）

| 字段 | 类型 | 说明 | 示例 |
|---|---|---|---|
| `slug` | string | kebab-case，**不含日期前缀** | `"anthropic-project-vend-2"` |
| `savedDate` | string | 收录到本站的日期，ISO 日期 | `"2026-05-25"` |
| `publishDate` | string | 原文发布日期，ISO 日期 | `"2025-12-18"` |
| `titleZh` | string | 中文精读标题，应能体现核心论点 | `"Anthropic Project Vend 2..."` |
| `titleEn` | string | 英文原标题 | `"Project Vend 2"` |
| `author` | string | 作者/团队名 | `"Anthropic Alignment Team"` |
| `authorTitle` | string | 作者头衔/背景，**给读者快速建立可信度** | `"Anthropic 对齐团队，..."` |
| `originalUrl` | string | 原文 URL | `"https://www.anthropic.com/research/project-vend-2"` |
| `source` | string | 来源站点简称（不是对象）| `"anthropic.com"` |
| `tags` | array of strings | 主题标签 | `["AI", "Agent", "Safety"]` |
| `summary` | string | 一句话核心，**真正的一句话，≤60 字**（2026-07-27 Jason 拍板） | `"Anthropic 用 Claudius 验证…"` |
| `keyPoints` | array of strings | 核心要点列表，**恰好 3 条**（只提炼最核心的三个观点），每条**带粗体小标题**，正文一句话（每条全长 ≤100 字），2026-07-27 Jason 拍板 | `["**模型工厂才是护城河**：一句话…"]` |
| `insight` | string | 启示与思考，**一句话，≤80 字**（2026-07-27 Jason 拍板） | `"模型能力商品化后，真正稀缺的是…"` |
| `summaryZh` | string | 中文完整概要（Markdown 格式），**≥2000 字** | `"## 一、Project Vend 是什么..."` |
| `quotes` | array of `{en, zh}` objects | 原文金句中英对照，**≥5 条** | `[{"en": "...", "zh": "..."}]` |

## 可选字段（optional）

| 字段 | 类型 | 何时存在 |
|---|---|---|
| `audio` | object `{url, duration_seconds}` | 已生成播客时填，未生成不填（**不要写空对象**，会导致渲染 NaN）|

## 内容质量标准（QC 审查重点）

### 1. 事实可追溯

- 每个具体数字 / 名字 / 引用必须能在原文中找到
- 如果只是 producer 自己的推断，必须明确标注（如"我的判断"/"我认为"/"对照 X 文献"）
- **禁止**：引用具体报告时给一个泛指页面 URL（如 `microsoft.com/en-us/research`）—— 这是 invented citation
- **禁止**：把 A 项目说成 B 项目同类（如把 Glasswing 攻防项目说成 Agent 失败案例）—— 这是 mischaracterization

### 2. 翻译保真度

- 原文有限定语（"some, not all" / "may" / "tends to" 等）翻译时必须保留
- 不机翻、不缩译重要 nuance
- 数字 / 比例 / 时间精确

### 3. 文风

- 中文表达流畅，无机翻痕迹
- summaryZh 是**概要**（描述事实+流程），insight 是**解读**（说明对读者意味着什么）—— 二者不应大量重复
- keyPoints 每条用 `**粗体小标题**：内容` 格式；恰好 3 条，每条一句话（≤100 字）
- summary 必须是**真正的一句话**（≤60 字），不是段落式摘要（2026-07-27 Jason 拍板）
- insight 也提炼成**一句话**（≤80 字），只留最核心启发

### 4. JSON 格式

- 必须是 valid JSON，可被 `python3 -c "import json; json.load(open(...))"` 解析
- UTF-8 编码
- 字符串中的引号 / 反斜杠正确转义
- **不要**字段间多余空白行
- **不要**字段值末尾有 trailing whitespace
- Markdown 内容中**避免**句子中间出现 `\n\n`（会撕裂段落）

### 5. 引用规范

- quotes 数组：每条至少有 `en` 和 `zh` 两个字段（中英对照）
- 引用的 URL 必须真实可达，且**指向具体内容**（不是泛指主页）

## QC 审查 verdict 标准

| 严重度 | 触发条件 |
|---|---|
| `critical` | mandatory 字段缺失 / JSON 不合法 / 事实级幻觉 / 数字编造 |
| `high` | 显著翻译失误 / mischaracterization / quotes 数量不足 / 必填字段类型错 |
| `medium` | invented citation / 限定语丢失 / 中英对照缺一 |
| `low` | 格式细节 / 个别用词 / 排版小问题 |

**verdict 决策**：
- 任何 `critical` → `REJECT`
- 多个 `high` 且影响主旨 → `REJECT`
- 仅 `medium`/`low` 且不影响理解 → `APPROVE_WITH_WARNINGS`
- 全部满足 → `APPROVE`
- 标准模糊 / 缺信息 → `ESCALATE` 给 Orchestrator

## 给 MK46 的审稿请求模板

```
# QC Audit Request

## audit_id
audit-<date>-<slug>

## audited_artifact
File path: /root/.openclaw/workspace/projects/ai-daily/src/data/reads/<filename>

## producer
Agent: <main / mk2>
Date: <date>
Task: 写一篇 <topic> 的中文精读 JSON 用于上线 aidigest.club/reads/

## acceptance criteria
按 /root/.openclaw/workspace/projects/ai-daily/docs/reads-schema-acceptance.md 中"必需字段"+"内容质量标准" 全量审查

## Expected output
Single JSON verdict object as defined in your SOUL.md
Plus self-archive JSONL append per AGENTS.md
```

## 历史变更

- 2026-05-25 立此 schema 文档，对照 23 篇历史精读 JSON 与项目 Astro 渲染层一致
