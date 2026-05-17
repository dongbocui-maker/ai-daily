#!/usr/bin/env bash
# setup.sh - Mac 端一次性 setup 脚本
# 把 ai-daily repo clone 到 ~/repos/，配 launchd 定时同步精读到 Obsidian vault
#
# 用法：
#   bash setup.sh
#
# 设置完成后：
#   - ~/repos/ai-daily 是 git working tree（git pull 拉新精读）
#   - launchd job 每 30 分钟自动 git pull + rsync 到 vault
#   - vault 在 OneDrive 同步路径里，OneDrive 自动同步到云端

set -euo pipefail

# ============ 配置区（用户可改） ============

REPO_URL="https://github.com/dongbocui-maker/ai-daily.git"
REPO_DIR="$HOME/repos/ai-daily"
VAULT_DIR="$HOME/Library/CloudStorage/OneDrive-Accenture(China)/Desktop/KB"
TARGET_SUBDIR="AI 精读"  # vault 内的子目录名
SYNC_INTERVAL_SEC=1800  # 30 分钟
PLIST_NAME="com.aidigest.obsidian-sync"
PLIST_PATH="$HOME/Library/LaunchAgents/${PLIST_NAME}.plist"
LOG_DIR="$HOME/Library/Logs/aidigest-obsidian"

# ============ 主流程 ============

echo "🚀 aidigest.club → Obsidian 同步 setup"
echo ""

# 1. 检查 vault 存在
if [ ! -d "$VAULT_DIR" ]; then
  echo "❌ Vault 路径不存在: $VAULT_DIR"
  echo "   请确认 OneDrive 已同步 + 路径正确"
  exit 1
fi
echo "✅ Vault 路径: $VAULT_DIR"

# 2. clone repo
if [ -d "$REPO_DIR/.git" ]; then
  echo "✅ Repo 已存在: $REPO_DIR（跳过 clone）"
  cd "$REPO_DIR"
  git fetch origin
  git checkout main
  git pull
else
  mkdir -p "$(dirname "$REPO_DIR")"
  echo "📥 Clone 中..."
  git clone "$REPO_URL" "$REPO_DIR"
fi

# 3. 第一次跑转换器（确保 obsidian-export/ 有内容）
cd "$REPO_DIR"
if [ ! -d "obsidian-export/reads" ] || [ -z "$(ls -A obsidian-export/reads 2>/dev/null)" ]; then
  echo "🔄 生成 markdown..."
  node scripts/reads-to-obsidian.mjs || {
    echo "⚠️  本地转换失败（可能 node 没装）——没关系，GitHub Actions 会自动跑"
    echo "   等下次 push 后 ~5 分钟，markdown 会自动出现在 repo 里"
  }
fi

# 4. 准备 vault 目标目录
TARGET_FULL="$VAULT_DIR/$TARGET_SUBDIR"
mkdir -p "$TARGET_FULL"
echo "✅ Vault 目标目录: $TARGET_FULL"

# 5. 第一次 rsync
if [ -d "$REPO_DIR/obsidian-export/reads" ]; then
  echo "📋 首次同步 markdown 到 vault..."
  rsync -av --delete "$REPO_DIR/obsidian-export/reads/" "$TARGET_FULL/"
fi

# 6. 写 launchd plist
mkdir -p "$LOG_DIR"
mkdir -p "$HOME/Library/LaunchAgents"

cat > "$PLIST_PATH" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>${PLIST_NAME}</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>-c</string>
        <string>cd "${REPO_DIR}" &amp;&amp; /usr/bin/git pull --quiet &amp;&amp; /usr/bin/rsync -a --delete "${REPO_DIR}/obsidian-export/reads/" "${TARGET_FULL}/"</string>
    </array>
    <key>StartInterval</key>
    <integer>${SYNC_INTERVAL_SEC}</integer>
    <key>RunAtLoad</key>
    <true/>
    <key>StandardOutPath</key>
    <string>${LOG_DIR}/sync.log</string>
    <key>StandardErrorPath</key>
    <string>${LOG_DIR}/sync.err</string>
</dict>
</plist>
EOF

# 7. 加载 launchd job
launchctl unload "$PLIST_PATH" 2>/dev/null || true
launchctl load "$PLIST_PATH"

echo ""
echo "✅ Setup 完成！"
echo ""
echo "📊 状态："
echo "   Repo:    $REPO_DIR"
echo "   Vault:   $TARGET_FULL"
echo "   日志:    $LOG_DIR/sync.log"
echo "   间隔:    ${SYNC_INTERVAL_SEC}s（30 分钟）"
echo ""
echo "🎉 现在 Obsidian 打开 KB vault，应该能在「AI 精读」目录看到 17 篇精读"
echo ""
echo "🔧 手动同步一次：launchctl start ${PLIST_NAME}"
echo "🛑 停止：       launchctl unload $PLIST_PATH"
echo "📋 查看日志：    tail -f $LOG_DIR/sync.log"
