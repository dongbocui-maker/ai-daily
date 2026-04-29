# 收藏功能 数据模型

_决定于 2026-04-29，与 Jason 反复讨论后定稿。_

## 核心原则

- **收藏粒度：单条资讯**（不是整篇日报）
- **数据存储：纯引用**（不存快照，源数据永不删除作为承诺）
- **隐私范围：完全私密**（v1 仅自己可见）
- **可扩展性：预留字段**（备注、标签、可见性等未来需要时直接启用）

---

## 决策记录

### A. 收藏粒度：单条资讯

- 用户点 ⭐ 收藏的是某条具体资讯（例如 "DeepSeek-V4 重磅发布"）
- "我的收藏"页面以单条资讯为单元展示，可跨日期混合
- 不提供"收藏整天日报"功能

### B. 备注/标签：纯收藏（v1）

- v1 仅支持点 ⭐ 收藏，不可写备注、不可打标签
- **schema 预留 `note` 和 `tags` 字段**，未来需要时直接启用，无需改表

### C. 数据生命周期：纯引用 + 永不删除

**核心承诺**：每天的日报 JSON 文件**只追加修订、永不删除**，作为收藏功能的稳定基础。

- 收藏表只存 `(user_id, daily_date, item_id)`，不复制资讯内容
- 显示"我的收藏"时，实时去查对应日期的 JSON
- sync 脚本如修订内容，收藏自动跟随更新（用户看到的是最新版本）
- 旧资讯永远存在于源数据中，引用永远有效

**约束**：sync 脚本不能删除任何 item，只能新增 / 修改。

### D. 隐私范围：完全私密

- 用户的收藏只有用户本人可见
- 系统不向其他用户展示"谁收藏了什么"
- **schema 预留 `visibility` 字段**，未来如需"团队精选"、"公开收藏"等功能，直接启用，无需改表

---

## 数据 Schema

### `favorites` 表

| 字段 | 类型 | 说明 |
|---|---|---|
| id | uuid | 主键 |
| user_id | string | 飞书 open_id |
| daily_date | string (YYYY-MM-DD) | 资讯所在日报的日期 |
| item_id | string | 资讯的稳定 ID（见下方"item_id 生成规则"） |
| visibility | string | "private"（v1 全部为 private，预留扩展） |
| note | text | 用户备注（v1 留空，预留扩展） |
| tags | string[] | 用户标签（v1 留空，预留扩展） |
| created_at | timestamp | 收藏时间 |
| updated_at | timestamp | 最后更新时间 |

**唯一约束**：`(user_id, daily_date, item_id)` 不允许重复（同一用户对同一资讯只能收藏一次）

**索引**：
- `user_id`（查"我的收藏"主路径）
- `(user_id, created_at DESC)`（按收藏时间排序）

### `users` 表

| 字段 | 类型 | 说明 |
|---|---|---|
| open_id | string | 主键，来自飞书 OAuth |
| name | string | 飞书姓名 |
| avatar_url | string | 飞书头像 URL |
| created_at | timestamp | 首次登录时间 |
| last_login_at | timestamp | 最近登录时间 |

---

## 前置工作：item_id 生成

### 现状

`src/data/daily/*.json` 中的 item 仅有 `title`、`body`、`insight`、`source`、`url`，**没有稳定 ID**。

### 解决方案

修改 `scripts/sync.ts`：在写 JSON 前，给每个 item 生成 `id` 字段。

**生成规则**（候选）：

**方案 1：基于 url 哈希**
```ts
item.id = sha1(item.url).slice(0, 12);
```
- 优点：url 变了 ID 才变（稳定）
- 缺点：同一资讯如果 url 变了（如换 CDN）ID 就变

**方案 2：基于 title + date 哈希**
```ts
item.id = sha1(date + '|' + item.title).slice(0, 12);
```
- 优点：url 变了 ID 不变
- 缺点：title 被 sanitize 改写后 ID 会变

**方案 3：基于 url 优先 + title 兜底**
```ts
item.id = sha1(item.url || (date + '|' + item.title)).slice(0, 12);
```
- 多数情况用 url（稳）
- url 为空时用 title 兜底
- **推荐**

### 一次性回填

需要一次性脚本把已有的 4 天 JSON（04-26 ~ 04-29）回填 ID，确保历史数据也能被收藏。

---

## 待办（议题 2 后续工作，非现在做）

- [ ] 在 `scripts/sync.ts` 中实现 item_id 生成逻辑
- [ ] 写一次性脚本回填历史 JSON 的 item_id
- [ ] 提交 sync 脚本变更
- [ ] 选定数据库（议题 3 决策后）
- [ ] 写 schema migration（v1 只建 favorites + users 两张表）
