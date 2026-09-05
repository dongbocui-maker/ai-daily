# Agents Dashboard 风格规范（J.A.R.V.I.S. OS HUD Style Guide）

> 提取日期：2026-08-07 ｜ 来源：`projects/ai-daily/src/pages/agents/index.astro`（线上 https://aidigest.club/agents/）
> 用途：完整视觉风格参考，可复用到其他 dashboard / HUD 类产出
> 设计基调：**Iron Man HUD / JARVIS OS**——暗色科技感、电光青蓝辉光、金色点缀、Orbitron 显示字体（Jason 审美偏好权威实现）

---

## 一、设计语言总纲

- **世界观**：整个页面是「J.A.R.V.I.S. OS」——Agent 是「战甲（Suit）」，模型端点是「能源节点」，cron 是「任务序列（Mission Queue）」，服务器是「LIGHTHOUSE NODE」
- **三主色体系**：金色（品牌/标题/主强调）+ 电光青蓝（数据/科技辉光）+ 红色（Iron Man 红，告警/危险）
- **辉光无处不在**：几乎所有彩色元素都带同色 `text-shadow` / `box-shadow` 辉光，营造全息投影感
- **命名双语**：板块标题「EN term · 中文」并置（如 `CRON QUEUE · 定时任务`、`FALLBACK SYSTEMS · 降级链路`）
- **UI chrome 无 emoji**：图标一律用 SVG / 几何图形 / Unicode 符号（◈ ⦁ ◉），不用 emoji

## 二、色彩 Tokens

```css
:root{
  --red:#E62429;        /* Iron Man 红：告警、危险、logo 强调 */
  --red-dim:#7a1418;    /* 暗红：边框、次级危险 */
  --gold:#FFC400;       /* 金色：标题、主强调、primary 节点 */
  --gold-dim:#8a6a00;   /* 暗金：分隔线渐变、次级 */
  --arc:#3FC9FF;        /* 电光青蓝（Arc Reactor 蓝）：数据、链接、科技元素 */
  --arc-glow:#00E5FF;   /* 青蓝辉光：脉冲、激活态 */
  --bg:#070A0F;         /* 页面底：近黑深蓝 */
  --panel:#0E1118;      /* 面板底 */
  --panel2:#141927;     /* 面板渐变第二色 */
  --line:#1f2a3d;       /* 边框/分隔线：深蓝灰 */
  --txt:#cdd6e3;        /* 正文：浅蓝灰 */
  --dim:#6b7689;        /* 次级文字/标签 */
  --green:#34d399;      /* 健康/成功 */
}
```

辅助色（局部使用）：
- TTS 紫 `#c98bff`（独立徽章）
- 成功绿变体 `#39d98a`（状态点）
- 错误红文字 `#ff8080` / `#ff7474`

**配色语义规则**：
- 金色 = 标题、PRIMARY、今日高亮、Orchestrator
- 青蓝 = 数值、Worker、在用链路、交互 hover
- 红色 = 告警、fallback 节点、CONFIDENTIAL 标记
- 绿色 = 健康状态点、OK 状态
- 灰 dim = 标签、单位、次级信息

## 三、字体系统

```html
<link href="/agents/fonts/hud-fonts.css" rel="stylesheet" />
<!-- 本地 woff2 自托管（Google Fonts 副本），国内可达 -->
```

| 字体 | 用途 | 典型规格 |
|---|---|---|
| **Orbitron**（900/800/700） | 所有「显示层」：logo、板块标题、数值、代号、按钮 | 标题 14px + letter-spacing 3px；大数值 24px；logo 26px 900 |
| **JetBrains Mono** | 正文、表格、标签、代码感文本 | 正文 11-12px；标签 9-10px |

**排版规则**：
- 全局 `letter-spacing:.3px`；标题类拉大到 1-3px；小标签 uppercase + 1-2px 字距
- 数值一律 Orbitron，单位用小号 JetBrains Mono dim 色内嵌（`.u`）
- 标题带金色辉光：`text-shadow:0 0 16px rgba(255,196,0,.4)`

## 四、页面氛围层（Atmosphere）

### 4.1 背景

```css
body{
  background:var(--bg);
  background-image:
    radial-gradient(circle at 15% 10%, rgba(230,36,41,.10), transparent 40%),   /* 左上红晕 */
    radial-gradient(circle at 85% 90%, rgba(63,201,255,.08), transparent 45%),  /* 右下青晕 */
    repeating-linear-gradient(0deg, rgba(255,255,255,.012) 0 1px, transparent 1px 3px); /* 细横纹 */
}
```

### 4.2 扫描线动画（全屏覆盖）

```css
.scan{position:fixed;inset:0;pointer-events:none;
  background:repeating-linear-gradient(0deg,rgba(63,201,255,.025) 0 2px,transparent 2px 5px);
  animation:scan 8s linear infinite}
@keyframes scan{to{background-position:0 100px}}
```

### 4.3 HUD 四角框

固定在视口四角的金色 L 形角标（40px、2px 边、opacity .5），移动端缩至 24px。

### 4.4 页眉/页脚

- 页眉：左 logo「J.A.R.V.I.S. OS」（红金撞色 + 辉光）+ 副标题小字；右侧青蓝「◉ ONLINE」脉冲状态 + 时间戳
- 页脚：`⌜ J.A.R.V.I.S. OS v0.1 ⌟ · DATA SNAPSHOT <时间> · CONFIDENTIAL(红) · POWERED BY JARVIS`

## 五、核心组件样式

### 5.1 统计卡（.stat）

- 面板渐变底 `linear-gradient(135deg,var(--panel),var(--panel2))` + 1px line 边 + 6px 圆角
- **左侧 3px 色条**（`::before`）区分类型：红/金/青
- 结构：小标签（10px dim uppercase 2px 字距）→ 大数值（Orbitron 24px，色随类型）→ 副文本（10px dim）
- 桌面 4 列 grid，移动端 1 列

### 5.2 板块标题（h2.sec）

```css
h2.sec{font-family:'Orbitron';font-weight:700;font-size:14px;color:var(--gold);
  letter-spacing:3px;display:flex;align-items:center;gap:10px}
h2.sec::after{content:'';flex:1;height:1px;
  background:linear-gradient(90deg,var(--gold-dim),transparent)}  /* 右侧渐隐金线 */
```

### 5.3 战甲卡（.suit，Agent 卡片）

- 渐变面板底 + 状态边框：online 青蓝 40% 边 + 辉光；idle 金 25% 边；offline 整卡 opacity .62
- **背景水印**：右侧 Iron Man 线稿 PNG（`opacity .09-.20` 随状态），`z-index:0` 垫底
- 卡头：**Arc Reactor 圆形反应堆**（46px SVG，见 5.4）+ 代号（Orbitron 金）+ 名称（16px 白粗体）+ 角色（9px dim 2px 字距）+ 右侧状态徽章
- 内容：2 列 grid 的 label/value 单元（label 9px dim uppercase / value Orbitron 15px 白）
- **能量条**：8px 高，红→金渐变填充 + 金辉光
- 底部虚线分隔的模型 mini 列表（10px，模型名青色）

### 5.4 Arc Reactor（核心视觉符号）

- 圆形 SVG：外圈金属环 + 内部旋转环（`ring-rot`）+ 发光核心（`core`）
- 状态动画：
  - online：核心 `glowSteady` 2.6s 稳定辉光 + 环 14s 匀速旋转，青色边框 + 内外辉光
  - idle：核心 `breathe` 1.8s 呼吸 + 环 26s 慢转，灰边
  - offline：核心 opacity .05，金属环变暗
- 登录门用 128px 大号版（倒三角内核 + 18s 旋转 + 三角脉冲）
- Knowledge Pyramid 的 agent 切换器用 29px mini 版

### 5.5 表格（.panel + table）

- 面板：`var(--panel)` 底 + line 边 + 8px 圆角 + 18px padding
- th：金色 9px uppercase 1px 字距，底部 1px line
- td：11px，行分隔线半透明；数值列右对齐 + Orbitron
- hover 行高亮 `rgba(63,201,255,.05)`
- 状态点（.tdot）：7px 圆点，ok 绿辉光 / err 红辉光+脉冲 / idle 灰

### 5.6 Fallback 链路（.chain）

```css
.chain .node{display:inline-block;padding:3px 10px;border-radius:3px}
.chain .primary{background:rgba(255,196,0,.12);border:1px solid var(--gold);color:var(--gold)}  /* 主模型：金 */
.chain .fb{background:rgba(230,36,41,.08);border:1px solid var(--red-dim);color:#d88}           /* fallback：暗红 */
.chain .arr{color:var(--dim);margin:0 6px}   /* → 箭头 */
```
- active model 高亮：黄色节点标识当前实跑模型（数据驱动，来自 active_model 匹配链路 index）

### 5.7 服务器状态条（LIGHTHOUSE NODE .node）

- 横向 strip：内嵌扫描纹（`::before` repeating-gradient）+ 四角渐变描边（`::after` border-image）
- 头行：Orbitron 青蓝 tag + 绿色 beacon 呼吸点 + dim 元信息
- 指标格（5 列 grid）：CPU/内存/磁盘/网络/流量包，每格 = 小标签 + Orbitron 数值 + **斜切段条**（`skewX(-22deg)` 的 9px 小块，点亮时同色辉光）——这是本风格的标志性「能量格」元件
- 色彩分档：arc 青 / gold 金 / green 绿；超标段用 warn 金边 / crit 红边

### 5.8 Event Ticker 跑马灯（SIGNAL）

- 36px 高横条，左侧固定「◈ SIGNAL」金色 Orbitron 标签（渐变遮罩压住滚动内容）
- 内容无限横向滚动（CSS animation，hover 暂停），条目间 ⦁ 分隔
- 事件 tag 分类配色：qc 青 / deploy 金 / fallback 红 / alert 红+脉冲

### 5.9 拓扑图（AGENT TOPOLOGY）

- 三层结构：Tier1 Orchestrator（金边）→ Tier2 Workers（青边）→ Tier3 LLM 端点（绿边 healthy）
- 节点卡：196px 渐变底圆角卡，hover 上浮 2px；代号 Orbitron + 名称 + 虚线分隔的角色行 + 状态点
- **连线**：SVG 绝对定位层画贝塞尔线——在用链路实线（青辉光）、备用点线（半透明）；点击 agent 节点切换高亮链路
- LLM 节点内：模型简写大字（Orbitron 15px）+ 右上 provider tag + 虚线下端点列表（绿点 ONLINE / 金点 STANDBY）
- TTS 独立紫色小徽章贴 Tier3 右上
- DIRECT 标签：胶囊形浮标贴节点顶部（青边 + 辉光）

### 5.10 Knowledge Pyramid（金字塔卡）

- 三层梯形（`clip-path: polygon`）：顶层金 / 中层青 / 底层绿，各带同色顶边和渐变填充
- 两侧竖排轴标签（writing-mode:vertical-rl）
- 右侧图例行卡 + 右上角状态 chip（超标变红）
- 底部原则 chips：胶囊形（`border-radius:999px`）+ 图标色分级

### 5.11 HUD Quick Nav（浮动导航舱）

- 右侧垂直悬浮胶囊：毛玻璃 `backdrop-filter:blur(6px)` + 青边辉光
- 圆形图标按钮：SVG 线稿图标 + hover 弹出青蓝渐变标签（右侧箭头小三角）
- 激活态：金色 + 外圈虚线旋转环（`hnrot` 动画）
- **scrub 扫选**：按住拖动时 Dock 式距离衰减（hot 1.4x / 相邻 1.12x / 其余 .85x）
- 窄屏收成右下角 44px 圆形 FAB（旋转外环 SVG），点开向上展开

### 5.12 Login Gate（访问门）

- 全屏居中卡：`min(460px, calc(100vw - 36px))`，深蓝渐变底 + 青边 + 多层辉光阴影 + 对角金色 L 角标
- 128px Arc Reactor（倒三角核心 + 旋转外环）
- 终端风提示框：`#05080d` 底 + 青字 + 金色高亮 + 闪烁光标（7px 方块 `steps(1)` blink）
- PIN 输入：大字距（7px）monospace，focus 时青边 + 双层辉光
- 按钮：青蓝渐变底 + 深色字 + Orbitron 900 + hover 上浮

### 5.13 趋势图（近 7 天）

- 纯 CSS flex 柱状图 + SVG 曲线叠加层（金色折线 + 辉光 drop-shadow，JS 按柱顶真实坐标绘制）
- 柱：青蓝渐变 + 青边 + 辉光；今日柱金色系
- hover tooltip（.bd-tip）：深底青边浮层 + 底部小三角，模型分解行（名/token/费用三列）

## 六、动画清单

| 动画 | 用途 | 参数 |
|---|---|---|
| `scan` | 全屏扫描线下移 | 8s linear infinite |
| `blink` | ONLINE 脉冲/光标 | 2s（50% opacity .4）；光标 1s steps(1) |
| `glowSteady` | reactor online 核心 | 2.6s ease-in-out |
| `breathe` | reactor idle 呼吸 | 1.8s（45-55% 亮） |
| `spin` | reactor 环旋转 | online 14s / idle 26s / 登录 18s linear |
| `mqpulse` | 错误状态点闪烁 | 1.4s（50% opacity .3） |
| `nodePulse` | 服务器 beacon | 2s（50% opacity .45） |
| `eventScroll` | 跑马灯 | 时长 JS 按内容宽度计算（CSS 变量 --scroll-dur） |
| `pulseTag` | alert tag 呼吸 | 1.5s |
| `hnrot` | 导航激活虚线环 | 6s linear（scrub 态 3s） |
| `loginTriPulse` | 登录三角脉冲 | 2.1s |

**交互过渡**：卡片 hover 上浮 `translateY(-2px)`、行 hover 青蓝 5% 底、按钮 hover 增强辉光——过渡时长统一 .12s-.25s。

## 七、响应式策略

- 断点：768px 主断点（+420px 超窄、820px/560px 导航舱、860px 金字塔）
- 桌面多列 grid → 移动全部单列；表格面板内横滚（`overflow-x:auto`）不撑宽页面
- 拓扑图窄屏：完整节点卡 → 紧凑徽章（`.arch-mini`/`.ep-mini` 切换 display），连线保留变细
- 隐藏 tooltip 在移动端用 `overflow-x:clip` 裁掉防撑宽
- HUD 四角、字号、间距按比例缩小；Quick Nav 变 FAB

## 八、工程注意事项

1. **字体自托管**：Orbitron + JetBrains Mono woff2 放 `public/agents/fonts/`，不依赖 Google Fonts CDN（国内可达性）
2. **超大 `<style is:global>` 与 Astro**：本页 frontmatter 禁止顶层 import JSON（esbuild 会把 style 误当 JS 解析报 `Unexpected "."`），必须用 dynamic `await import()`
3. **数据驱动 + 硬编码兜底**：链路/拓扑数据 build 时从 `agent-chains.json` 注入（single source of truth = openclaw.json），JS 里保留硬编码 literal 仅作 JSON 损坏时兜底
4. **z-index 层级**：scan 99 > overlay 50 > hudnav 48 > 卡片内容 2 > 水印 0
5. **noindex**：`<meta name="robots" content="noindex,nofollow">`（私有监控页）
6. 状态样式一律「边框色 + 辉光 + 动画」三件套表达，不靠单一颜色（可及性）

## 九、快速复用模板（最小 HUD 页骨架）

```html
<!doctype html>
<html lang="zh-CN">
<head>
<link href="fonts/hud-fonts.css" rel="stylesheet">
<style>
:root{--red:#E62429;--gold:#FFC400;--arc:#3FC9FF;--arc-glow:#00E5FF;
  --bg:#070A0F;--panel:#0E1118;--panel2:#141927;--line:#1f2a3d;
  --txt:#cdd6e3;--dim:#6b7689;--green:#34d399}
*{margin:0;padding:0;box-sizing:border-box}
body{background:var(--bg);color:var(--txt);font-family:'JetBrains Mono',monospace;
  background-image:radial-gradient(circle at 15% 10%,rgba(230,36,41,.10),transparent 40%),
    radial-gradient(circle at 85% 90%,rgba(63,201,255,.08),transparent 45%);
  min-height:100vh;padding:24px;letter-spacing:.3px}
.scan{position:fixed;inset:0;pointer-events:none;z-index:99;
  background:repeating-linear-gradient(0deg,rgba(63,201,255,.025) 0 2px,transparent 2px 5px);
  animation:scan 8s linear infinite}
@keyframes scan{to{background-position:0 100px}}
h1{font-family:'Orbitron';font-weight:900;color:var(--gold);
  text-shadow:0 0 16px rgba(255,196,0,.4);letter-spacing:2px}
h2{font-family:'Orbitron';font-weight:700;font-size:14px;color:var(--gold);
  letter-spacing:3px;display:flex;align-items:center;gap:10px;margin:8px 0 16px}
h2::after{content:'';flex:1;height:1px;background:linear-gradient(90deg,#8a6a00,transparent)}
.panel{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:18px}
.stat{background:linear-gradient(135deg,var(--panel),var(--panel2));
  border:1px solid var(--line);border-radius:6px;padding:16px 18px;position:relative;overflow:hidden}
.stat::before{content:'';position:absolute;top:0;left:0;width:3px;height:100%;background:var(--arc)}
.stat .k{font-size:10px;color:var(--dim);letter-spacing:2px;text-transform:uppercase}
.stat .v{font-family:'Orbitron';font-weight:700;font-size:24px;margin-top:8px;color:var(--arc)}
</style>
</head>
<body>
<div class="scan"></div>
<h1>MY SYSTEM <small style="color:var(--dim)">· 中文副标</small></h1>
<h2>SECTION TITLE · 板块名</h2>
<div class="stat"><div class="k">METRIC LABEL</div><div class="v">42<span style="font-size:13px;color:var(--dim)">ms</span></div></div>
</body>
</html>
```

---

## 附：完整源文件索引

| 内容 | 路径 |
|---|---|
| 完整页面（1628 行，CSS 全内联） | `projects/ai-daily/src/pages/agents/index.astro` |
| 自托管字体 | `projects/ai-daily/public/agents/fonts/` |
| Iron Man 线稿水印 | `projects/ai-daily/public/agents/ironman-lineart.png` |
| 链路数据生成器 | `projects/ai-daily/scripts/gen-agent-chains.py` |
| Dashboard 配置归档 | `memory/archive/agents-dashboard-config.md` |
| 线上页面 | https://aidigest.club/agents/ （访问码保护） |
