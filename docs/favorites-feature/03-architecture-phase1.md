# 阶段 1 架构：在现有网站上加收藏功能

_决定于 2026-04-29，与 Jason 反复讨论后定稿。_

## 分阶段策略

**阶段 1（现在）**：GitHub Pages 网站不变，加收藏功能
**阶段 2（未来，视使用情况而定）**：迁移到 Azure VM，架构升级

**理由**：
- 一次只动一个变量，降低风险
- 阶段 1 上线后收反馈，再决定是否值得做阶段 2
- 避免过度设计，避免在没人用之前过度投资

---

## 阶段 1 架构

```
┌─────────────────────────────────────────┐
│  GitHub Pages: aidigest.club            │
│  (Astro 静态站，几乎不变)                 │
│  + 加少量前端 JS 处理收藏交互            │
└──────────┬──────────────────────────────┘
           │ fetch /api/* (跨域)
           │ fetch /auth/* (跨域)
           ▼
┌─────────────────────────────────────────┐
│  Cloudflare Workers                      │
│  (TypeScript + Hono)                    │
│  - /auth/feishu/start    OAuth 起点     │
│  - /auth/feishu/callback OAuth 回调     │
│  - /auth/me              当前用户       │
│  - /auth/logout          退出登录       │
│  - /api/favorites        收藏 CRUD      │
└──────────┬──────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────┐
│  Cloudflare D1 (SQLite)                 │
│  - users 表                              │
│  - favorites 表                          │
│  - sessions 表                           │
└─────────────────────────────────────────┘
```

---

## 关键技术选型

### 后端：Cloudflare Workers + Hono

- **语言**：TypeScript（与项目其余部分一致）
- **框架**：Hono（轻量、专为 Workers/Serverless 设计）
- **运行时**：Cloudflare Workers（V8 isolates，全球边缘部署）
- **免费额度**：100k 请求/天，对你阶段 1 完全够用

### 数据库：Cloudflare D1

- **底层**：SQLite
- **优势**：与未来 VM 上的 SQLite 兼容，迁移零成本
- **免费额度**：5 GB 存储、500 万行读/天、10 万行写/天
- **管理**：通过 wrangler CLI 跑 migrations 和查询

### 域名规划

**问题**：网站在 GitHub Pages（aidigest.club），API 在 Cloudflare Workers（默认 *.workers.dev 域名），跨域问题。

**方案**：
1. **方案 a（推荐）**：把 API 绑到自定义子域 `api.aidigest.club`
   - 在 Cloudflare DNS 加一条 CNAME 指向 Worker
   - 前端 fetch `https://api.aidigest.club/api/favorites`
   - 配置 CORS 允许 `https://aidigest.club`
2. **方案 b**：直接用 `*.workers.dev` 域名
   - 简单但不够正式
   - 万一被 GFW 干扰更难处理

### 跨域 (CORS) 配置

由于网站在 `aidigest.club`，API 在 `api.aidigest.club`，需要：

- Workers 响应 CORS headers：
  - `Access-Control-Allow-Origin: https://aidigest.club`
  - `Access-Control-Allow-Credentials: true`
- 前端 fetch 用 `credentials: 'include'`
- Cookie 设置 `SameSite=None; Secure`（跨域必须）

---

## 数据库 Schema (D1)

### users 表

```sql
CREATE TABLE users (
  open_id       TEXT PRIMARY KEY,
  name          TEXT NOT NULL,
  avatar_url    TEXT,
  created_at    INTEGER NOT NULL,  -- unix timestamp ms
  last_login_at INTEGER NOT NULL
);
```

### favorites 表

```sql
CREATE TABLE favorites (
  id          TEXT PRIMARY KEY,    -- uuid
  user_id     TEXT NOT NULL,        -- 飞书 open_id
  daily_date  TEXT NOT NULL,        -- "2026-04-29"
  item_id     TEXT NOT NULL,        -- 资讯稳定 ID
  visibility  TEXT NOT NULL DEFAULT 'private',
  note        TEXT,                 -- 预留，v1 留空
  tags        TEXT,                 -- 预留，JSON 数组字符串
  created_at  INTEGER NOT NULL,
  updated_at  INTEGER NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(open_id),
  UNIQUE (user_id, daily_date, item_id)
);

CREATE INDEX idx_favorites_user
  ON favorites(user_id, created_at DESC);
```

### sessions 表

```sql
CREATE TABLE sessions (
  id          TEXT PRIMARY KEY,    -- uuid (cookie 中存的 session_id)
  user_id     TEXT NOT NULL,
  created_at  INTEGER NOT NULL,
  expires_at  INTEGER NOT NULL,    -- unix timestamp ms
  FOREIGN KEY (user_id) REFERENCES users(open_id)
);

CREATE INDEX idx_sessions_user ON sessions(user_id);
CREATE INDEX idx_sessions_expires ON sessions(expires_at);
```

---

## API 接口设计（草案，议题 4 详细确认）

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/auth/feishu/start` | 跳转飞书 OAuth |
| GET | `/auth/feishu/callback` | 飞书回调，换 token 创建 session |
| GET | `/auth/me` | 返回当前用户信息（未登录返回 401） |
| POST | `/auth/logout` | 销毁 session |
| POST | `/api/favorites` | 添加收藏 `{daily_date, item_id}` |
| DELETE | `/api/favorites/:id` | 删除收藏 |
| GET | `/api/favorites` | 列出当前用户的收藏，支持分页 |

---

## 阶段 2 迁移路径（提前规划）

阶段 2 把这套搬到 Azure VM 时：

| 当前（阶段 1） | 未来（阶段 2） | 迁移成本 |
|---|---|---|
| Cloudflare Workers | Node.js + Hono on VM | 业务代码几乎不动 |
| D1 (SQLite) | VM 上的 SQLite | `wrangler d1 export` → 导入 VM 文件 |
| GitHub Pages 静态站 | Caddy 服务静态文件 | 把 dist/ 同步到 VM |
| api.aidigest.club CNAME | 改 DNS 指向 VM IP | 几分钟 |

**关键**：阶段 1 的代码几乎全部能复用到阶段 2，**这就是选 Workers + D1 的核心理由**。

---

## 待办（按议题排）

- [x] 议题 1：UI/UX 设计 → `01-ui-ux.md`
- [x] 议题 2：数据模型 → `02-data-model.md`
- [x] 议题 3：阶段 1 架构选型 → 本文档
- [ ] 议题 4：飞书 App 配置 + OAuth 流程详细设计
- [ ] 议题 5：前端集成方案（Astro 站如何加交互）
- [ ] 议题 6：部署 + CI/CD（Workers 怎么发布、D1 怎么 migrate）
- [ ] 议题 7：sync.ts 修改加 item_id（数据模型前置工作）
