# aidigest.club 精读 → Obsidian 自动同步（Mac 端）

## 总览

```
GitHub repo (cloud)
  ├── src/data/reads/*.json          ← 精读源数据
  └── obsidian-export/reads/*.md     ← GitHub Actions 自动生成

       ↓ git pull (每 30 min)

Mac: ~/repos/ai-daily/obsidian-export/reads/*.md

       ↓ rsync (每 30 min)

Vault: ~/Library/CloudStorage/OneDrive-Accenture(China)/Desktop/KB/AI 精读/

       ↓ OneDrive 自动同步

云端 + 其他设备
```

## 一次性 setup（10 分钟）

打开 Mac 终端，跑：

```bash
# 1. 装 git（如果还没有）
xcode-select --install  # 弹窗确认安装

# 2. 装 Node.js（如果还没有，rsync/launchd 已自带）
brew install node       # 需要 Homebrew

# 3. 下载并跑 setup 脚本
curl -fsSL https://raw.githubusercontent.com/dongbocui-maker/ai-daily/main/scripts/obsidian-sync-mac/setup.sh -o /tmp/setup-aidigest-obsidian.sh
bash /tmp/setup-aidigest-obsidian.sh
```

> 如果 `curl` 访问 GitHub 不稳，可以先 clone repo 然后跑 `bash ~/repos/ai-daily/scripts/obsidian-sync-mac/setup.sh`

跑完后：

- ✅ Repo clone 到 `~/repos/ai-daily`
- ✅ 17 篇精读 markdown 已同步到 `vault/AI 精读/`
- ✅ launchd job 每 30 分钟自动 pull + sync

打开 Obsidian → KB vault → 左侧文件树应该看到 **AI 精读** 目录 + 17 个 `.md` 文件。

## 设置之后

**全自动**。每次 GitHub 上有新精读上线（cron 自动 / 手动 push）：

1. GitHub Actions 自动生成 markdown（~2 分钟）
2. Mac 端 launchd 30 分钟内 pull 一次
3. rsync 同步到 vault
4. Obsidian 自动看到新文件

**你不用做任何事**。

## OneDrive 兼容性

vault 在 OneDrive 同步路径里——这套设计专门照顾了：

- ✅ Repo 在 OneDrive **外**（`~/repos/`）—— `.git/` 不会被 OneDrive 同步
- ✅ Vault 内只有真 markdown 文件（rsync 出来的，不是 symlink）—— OneDrive 能正确处理
- ✅ rsync `--delete`：repo 里删了的文件 vault 里也删，**完全镜像**

## 常用命令

```bash
# 立即手动同步一次
launchctl start com.aidigest.obsidian-sync

# 查看同步日志
tail -f ~/Library/Logs/aidigest-obsidian/sync.log
tail -f ~/Library/Logs/aidigest-obsidian/sync.err

# 停止自动同步
launchctl unload ~/Library/LaunchAgents/com.aidigest.obsidian-sync.plist

# 重新启动
launchctl load ~/Library/LaunchAgents/com.aidigest.obsidian-sync.plist
```

## 排错

**问题 1：vault 里没看到「AI 精读」目录**
```bash
ls "~/Library/CloudStorage/OneDrive-Accenture(China)/Desktop/KB/"
cat ~/Library/Logs/aidigest-obsidian/sync.err
```

**问题 2：精读没自动更新**
```bash
cd ~/repos/ai-daily && git log --oneline obsidian-export/reads/ | head -5
# 看最近的 commit 时间。如果太老，可能 GitHub Actions 没跑起来——
# 检查 https://github.com/dongbocui-maker/ai-daily/actions
```

**问题 3：OneDrive 把 markdown 同步成「冲突」副本**
- 通常因为 vault 同一目录被多个客户端写。检查是不是另一台 Mac 也跑了同步任务。
- 解决：另一台 Mac 上 `launchctl unload ~/Library/LaunchAgents/com.aidigest.obsidian-sync.plist`，只保留一台主同步。

## 想停掉这套同步

```bash
launchctl unload ~/Library/LaunchAgents/com.aidigest.obsidian-sync.plist
rm ~/Library/LaunchAgents/com.aidigest.obsidian-sync.plist
# vault 里的 markdown 保留不删（如果想删：rm -rf "$VAULT/AI 精读/"）
```
