# 学习中心 · 内容添加规范

> 此文档定义「学习中心」（`/learn/`）板块新增内容的统一格式与流程。
> 已上传内容（如 Anthropic Academy）保留原状，**不强制按此规范回溯**。
> 自 2026-05-04 起新增内容**统一按此规范来**。

---

## 一、入口卡片配置（`src/data/learn.json`）

入口页 `/learn/` 列表的所有卡片由 `src/data/learn.json` 数据驱动。

### Schema

```jsonc
{
  "$schema_version": "1.0",
  "items": [
    {
      "slug": "<URL 友好的英文短名，全小写连字符>",
      "tag": "<板块/分类标签，6 字以内>",
      "title": "<卡片主标题，建议 ≤ 20 字>",
      "desc": "<2-3 句简介，描述课程内容、规模、特点>",
      "meta": ["<元信息 1>", "<元信息 2>", ...],
      "href": "<目标页面路径或外链 URL>",
      "external": false
    }
  ]
}
```

### 字段定义

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `slug` | string | ✅ | URL 短名，全小写英文 + 连字符。例：`anthropic-academy`、`mit-deep-learning-2026` |
| `tag` | string | ✅ | 分类标签。常用：`学习计划`、`课程笔记`、`技术资料`、`视频笔记`、`深度阅读` |
| `title` | string | ✅ | 卡片主标题。简洁直白，避免冗长 |
| `desc` | string | ✅ | 2-3 句简介。说明内容、规模、特点。建议 60-120 字 |
| `meta` | string[] | ✅ | 元信息数组。常用项：日期、时长、来源、章节数 |
| `href` | string | ✅ | 内部页面以 `/` 开头（如 `/learn/xxx/`）；外链填完整 URL |
| `external` | boolean | ❌ | 是否外链。默认 `false`。`true` 时不会拼接站点 base path |

### 示例

```json
{
  "slug": "anthropic-prompt-engineering",
  "tag": "课程笔记",
  "title": "Anthropic Prompt Engineering",
  "desc": "Anthropic 官方的提示词工程系统课程笔记。涵盖角色设定、Few-shot、CoT、Tool use 五大主题。",
  "meta": ["🗓 2026-06", "~12 章节", "Source: Anthropic"],
  "href": "/learn/anthropic-prompt-engineering/",
  "external": false
}
```

外链示例：

```json
{
  "slug": "karpathy-zero-to-hero",
  "tag": "视频课程",
  "title": "Neural Networks: Zero to Hero",
  "desc": "Karpathy 的神经网络从零到精通系列。从 micrograd 到 GPT 实现，9 集深度教学。",
  "meta": ["🎥 YouTube", "~12 hrs"],
  "href": "https://www.youtube.com/playlist?list=PLAqhIrjkxbuWI23v9cThsA9GvCAUhRvKZ",
  "external": true
}
```

---

## 二、课程详情页（如果是站内页）

### 路径

- 静态 HTML：`public/learn/<slug>/index.html`
  - 适合：单页深度内容、自定义样式、独立排版（如 Anthropic Academy 这种）
  - 部署后访问：`<站点>/learn/<slug>/`

- Astro 页面：`src/pages/learn/<slug>.astro` 或 `src/pages/learn/<slug>/index.astro`
  - 适合：和站点其他部分共享布局、需要 SSG 数据注入
  - 部署后访问：`<站点>/learn/<slug>/`

**当前默认推荐**：静态 HTML（`public/` 目录），更灵活、不受 Astro layout 限制。

### 页面内必备元素

无论用哪种方式，详情页内**建议**包含：

1. **顶部标题**：和入口卡片 `title` 一致或更详细
2. **元信息**：日期、时长、来源链接、原作者
3. **主体内容**
4. **底部导航**：返回 `/learn/` 链接

### 样式建议

- 字体：`system-ui` 系列，避免引入第三方字体
- 配色：保持站点主色调（accent-purple 紫色 + accent-ink 深色）一致
- 响应式：确保移动端可读
- 暗色模式：可选

---

## 三、添加新课程的工作流

### Step 1: 准备详情页内容

把课程内容做成 HTML（或 Astro 组件），放在：
```
public/learn/<slug>/index.html
```

### Step 2: 在 learn.json 添加入口

编辑 `src/data/learn.json`，在 `items` 数组里追加一项（按上面 schema）。

### Step 3: 本地验证（可选）

```bash
cd /root/.openclaw/workspace/projects/ai-daily
npx astro build
# 看 build 是否成功
# 看 dist/learn/index.html 卡片是否正确出现
```

### Step 4: Commit + Push

```bash
git add src/data/learn.json public/learn/<slug>/
git commit -m "feat(learn): 新增 <课程名>"
git push origin main
```

GitHub Actions 自动 build 上线，3-5 分钟生效。

---

## 四、设计准则

### ✅ 应该做

- **小而精**：每张卡片信息密度高、不啰嗦
- **`tag` 用现有的**：避免每次发明新分类，让标签系统稳定
- **`desc` 突出"值得看"的理由**：而不是单纯陈述课程结构
- **`meta` 给具体数字**：日期、时长、章节数——让人一眼看出规模

### ❌ 避免

- 不要在 `title` 里加日期 / 期号（meta 里放）
- 不要在 `desc` 里写营销语（"绝对不容错过！"）
- 不要 tag 滥造（如「2026 春节学习」「五一计划」这种时效性强的标签）
- 不要堆砌 meta（>4 项就太碎）

---

## 五、未来扩展（待定）

如果将来出现以下需求，可考虑扩展 schema：

- **多类型支持**：在 schema 里加 `type` 字段（`study-plan` / `course-notes` / `video-series` / `data-dashboard`），用不同卡片样式
- **进度追踪**：加 `progress` 字段（`completed` / `in-progress` / `planned`）
- **难度分级**：加 `level` 字段（`beginner` / `intermediate` / `advanced`）
- **标签多选**：`tag` 改 `tags: string[]`，支持多分类筛选
- **分页 / 搜索**：当 items > 20 时考虑

**原则**：**等真的需要时再加，不预先复杂化。**

---

## 六、版本历史

- **v1.0**（2026-05-04）：初版，定义基本字段与添加流程
