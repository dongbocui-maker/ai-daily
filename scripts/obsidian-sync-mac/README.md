# aidigest.club 精读 → Obsidian 按需同步（纯 F 方案）

## 总览

```
┌─────────────────────────────────────────────────┐
│ GitHub (cloud, 自动)                             │
│  - 新精读 JSON 上传                                │
│  - GitHub Actions 自动生成 markdown               │
└──────────────────┬──────────────────────────────┘
                   ↓
                   ↓ ←─── 你按 Cmd+Shift+R 才触发
                   ↓
┌─────────────────────────────────────────────────┐
│ Mac: ~/repos/ai-daily/                          │
│  - git pull → 拿最新 markdown                    │
│  - rsync → 镜像到 vault                          │
└──────────────────┬──────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────┐
│ Vault: KB/AI 精读/*.md                          │
│  - OneDrive 自动同步到云端                         │
│  - 其他设备的 Obsidian 自动看到                    │
└─────────────────────────────────────────────────┘
```

**特点**：
- ✅ 完全按需触发——你按快捷键才同步
- ✅ 零后台任务（没装 launchd / cron）
- ✅ Mac 干净，看得见管得着
- ✅ 一次同步 ~2 秒

---

## 一次性 setup（5 分钟）

### 第一部分：终端跑 setup 脚本

```bash
# 1. 装 Node.js（如果还没装，brew 自带 git）
brew install node

# 2. 下载并跑 setup
curl -fsSL https://raw.githubusercontent.com/dongbocui-maker/ai-daily/main/scripts/obsidian-sync-mac/setup.sh -o /tmp/setup.sh
bash /tmp/setup.sh
```

setup 脚本会：
1. clone repo 到 `~/repos/ai-daily`
2. 首次同步 17 篇精读到 `vault/AI 精读/`
3. 打印 Obsidian 插件配置步骤

> ⚠️ 如果 `curl` 访问 GitHub 不稳，先 git clone：
> ```
> mkdir -p ~/repos && cd ~/repos
> git clone https://github.com/dongbocui-maker/ai-daily.git
> bash ~/repos/ai-daily/scripts/obsidian-sync-mac/setup.sh
> ```

### 第二部分：Obsidian 内装 Shell Commands 插件

1. **Settings**（左下齿轮）
2. **Community plugins** → Turn on（第一次用）
3. **Browse** → 搜 **"Shell commands"**（作者 Taitava）
4. **Install** → **Enable**

### 第三部分：配置同步按钮

1. **Settings → Shell commands**（左侧栏新出现的项）
2. 点 **"New shell command"**
3. **Command** 框粘贴：

   ```
   /Users/jason.dongbo.cui/repos/ai-daily/scripts/obsidian-sync-mac/manual-sync.sh
   ```

4. 点这条命令展开详细配置，设置：
   - **Alias**：`🔄 同步 AI 精读`
   - **Output channel**：`Notification balloons`（弹通知告诉你结果）
   - **Confirm before execution**：关闭

### 第四部分：绑快捷键（强推荐）

1. **Settings → Hotkeys**
2. 搜 "**同步 AI 精读**"（或 `Shell commands: Execute...`）
3. 点 + 号 → 按 **Cmd+Shift+R**（R for Reads）
4. 保存

---

## 日常使用

**想看新精读时**：

打开 Obsidian → 按 `Cmd+Shift+R` → 右下角弹通知：

```
✅ 同步完成
📥 新增 2 篇精读：
  - 2026-05-18-new-reading-1
  - 2026-05-18-new-reading-2
```

或

```
✅ 已经是最新 — 没有新精读
```

2 秒搞定。

**没新内容时按了也没事**——脚本会告诉你"已经是最新"。

---

## 高级用法

### 命令面板触发（不绑快捷键也能用）

打开 Obsidian → `Cmd+P` → 输入"同步 AI 精读" → 回车

### 左侧栏图标按钮

Shell Commands 插件设置里给命令加 **Icon**，会出现在 Obsidian 左侧栏，点一下就跑。

### 终端手动跑

不开 Obsidian 也能同步：

```bash
bash ~/repos/ai-daily/scripts/obsidian-sync-mac/manual-sync.sh
```

输出告诉你拉了哪些新精读。

---

## 排错

**问题 1：按快捷键没反应**

检查 Shell Commands 是否 enabled：Settings → Community plugins → Shell commands → 开关亮起

检查脚本能不能跑：终端跑 `bash ~/repos/ai-daily/scripts/obsidian-sync-mac/manual-sync.sh`

**问题 2：通知弹了但 vault 里没看到新文件**

```bash
# 看 repo 是不是真的拉到了
cd ~/repos/ai-daily && git log --oneline obsidian-export/reads/ | head -5

# 看 vault 目录
ls "~/Library/CloudStorage/OneDrive-Accenture(China)/Desktop/KB/AI 精读/"

# 强制同步一次
bash ~/repos/ai-daily/scripts/obsidian-sync-mac/manual-sync.sh
```

**问题 3：GitHub 不通**

国内访问 GitHub 偶尔超时。重试就好。如果常出，配 git proxy：

```bash
git config --global http.proxy http://127.0.0.1:7890
# 或用其他代理
```

---

## 想停用 / 删除

```bash
# 1. Obsidian 里删 Shell command
# Settings → Shell commands → 找到那条 → 删除

# 2. 删快捷键
# Settings → Hotkeys → 找到 Shell commands 命令 → 移除

# 3. 删 repo（可选）
rm -rf ~/repos/ai-daily

# 4. 删 vault 里的精读（可选）
rm -rf "~/Library/CloudStorage/OneDrive-Accenture(China)/Desktop/KB/AI 精读/"
```

---

## 文件位置参考

| 文件 | 路径 |
|---|---|
| Git repo | `~/repos/ai-daily/` |
| Setup 脚本 | `~/repos/ai-daily/scripts/obsidian-sync-mac/setup.sh` |
| 同步脚本 | `~/repos/ai-daily/scripts/obsidian-sync-mac/manual-sync.sh` |
| 精读 markdown 源 | `~/repos/ai-daily/obsidian-export/reads/*.md` |
| Vault 精读目录 | `~/Library/.../KB/AI 精读/*.md` |
