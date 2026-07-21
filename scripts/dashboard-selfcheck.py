#!/usr/bin/env python3
"""S.H.R.I.M.P. Dashboard 自检（智能自我维护核心）。

体检 2026-07-21 引入。防三类「一直更新导致的烂尾」：
  1. DEAD LINK — crontab 引用的脚本是否都存在；systemd unit 是否 active
  2. STALE DATA — live dashboard-data.json / traffic-package.json 是否超时未更新
  3. UNPRICED  — 在用模型是否都有单价（复用 aggregate 的 UNPRICED_SEEN 逻辑，独立扫）
  4. CONFIG DRIFT — openclaw.json 里的 agent 是否都在 dashboard AGENTS 表内

有异常 → 退出码 1 + 报告写 /tmp/shrimp-selfcheck-report.txt（cron 据此推飞书）。
纯读，不改任何东西。由 cron 每日跑一次。
"""
import json, os, re, sys, glob, subprocess, datetime

REPO = '/root/.openclaw/workspace/projects/ai-daily'
DASH = '/root/.openclaw/workspace/projects/agents-dashboard'
LIVE = f'{DASH}/live/dashboard-data.json'
TRAFFIC = f'{DASH}/live/traffic-package.json'
PRICING_JSON = f'{REPO}/src/data/pricing.json'
OPENCLAW_CONFIG = '/root/.openclaw/openclaw.json'
STALE_LIVE_MIN = 180      # live 数据超 3h 没更新 = stale（cron 事件驱动，正常几十分钟一刷）
STALE_TRAFFIC_MIN = 180   # 流量包每小时同步，超 3h = 同步坏了

DASHBOARD_AGENTS = {'main', 'aima', 'mk2', 'mk46', 'claude-researcher'}

issues = []
lines = []
now = datetime.datetime.now()


def _age_min(path):
    try:
        return (now.timestamp() - os.path.getmtime(path)) / 60
    except OSError:
        return None


# ── 1. DEAD LINK: crontab 引用的脚本存在性 ──────────────────────
lines.append('[1] DEAD LINK — crontab 脚本引用')
try:
    cron = subprocess.run(['crontab', '-l'], capture_output=True, text=True, timeout=10).stdout
except Exception:
    cron = ''
# 抓 crontab 里出现的 .sh / .py 绝对路径
for m in re.finditer(r'(/root/[^\s]+\.(?:sh|py))', cron):
    p = m.group(1)
    if not os.path.exists(p):
        issues.append(f'crontab 引用的脚本不存在: {p}')
        lines.append(f'  ❌ MISSING: {p}')
if not any('❌' in l for l in lines[-5:]):
    lines.append('  ✅ 所有 crontab 脚本引用均存在')

# ── 1b. systemd units active ────────────────────────────────────
lines.append('[1b] SYSTEMD — 关键 unit 状态')
for unit in ['shrimp-dashboard-refresh.path', 'cloudflared-shrimp.service']:
    try:
        r = subprocess.run(['systemctl', 'is-active', unit], capture_output=True, text=True, timeout=10)
        state = r.stdout.strip()
    except Exception:
        state = 'unknown'
    if state not in ('active', 'activating'):
        issues.append(f'systemd unit 非 active: {unit} ({state})')
        lines.append(f'  ❌ {unit}: {state}')
    else:
        lines.append(f'  ✅ {unit}: {state}')
# serve.py 进程
try:
    ps = subprocess.run(['pgrep', '-f', 'agents-dashboard/serve.py'], capture_output=True, text=True, timeout=10)
    if not ps.stdout.strip():
        issues.append('serve.py 未运行（实时端点 data.aidigest.club 会挂）')
        lines.append('  ❌ serve.py: 未运行')
    else:
        lines.append(f'  ✅ serve.py: pid {ps.stdout.split()[0]}')
except Exception:
    lines.append('  ⚠️ serve.py: 无法检测')

# ── 2. STALE DATA ────────────────────────────────────────────────
lines.append('[2] STALE DATA — 数据新鲜度')
for label, path, limit in [('live dashboard-data', LIVE, STALE_LIVE_MIN),
                            ('traffic-package', TRAFFIC, STALE_TRAFFIC_MIN)]:
    age = _age_min(path)
    if age is None:
        issues.append(f'{label} 文件不存在: {path}')
        lines.append(f'  ❌ {label}: 文件缺失')
    elif age > limit:
        issues.append(f'{label} 已 {age:.0f}min 未更新（阈值 {limit}min），刷新链路可能坏了')
        lines.append(f'  ❌ {label}: {age:.0f}min 前（超 {limit}min）')
    else:
        lines.append(f'  ✅ {label}: {age:.0f}min 前')

# ── 3. UNPRICED — 在用模型是否都有单价 ──────────────────────────
lines.append('[3] UNPRICED — 在用模型单价覆盖')
try:
    pdoc = json.load(open(PRICING_JSON))
    priced = set(pdoc.get('models', {}).keys()) | set(pdoc.get('aliases', {}).keys())
except Exception as e:
    priced = set()
    issues.append(f'pricing.json 读取失败: {e}')
    lines.append(f'  ❌ pricing.json: {e}')
seen = {}
for aid in DASHBOARD_AGENTS:
    for f in glob.glob(f'/root/.openclaw/agents/{aid}/sessions/*.trajectory.jsonl'):
        try:
            for line in open(f):
                try: d = json.loads(line)
                except: continue
                if d.get('type') != 'model.completed': continue
                key = f"{d.get('provider')}/{d.get('modelId')}"
                tot = (d.get('data') or {}).get('usage', {}).get('total', 0) or 0
                if tot:
                    seen[key] = seen.get(key, 0) + tot
        except Exception:
            pass
unpriced = {k: v for k, v in seen.items()
            if k not in priced and k.rsplit('/', 1)[0] + '/' + k.rsplit('/', 1)[-1].lower() not in priced}
if unpriced:
    for k, v in sorted(unpriced.items(), key=lambda x: -x[1]):
        issues.append(f'在用模型无单价: {k} ({v:,} tok) → 成本算 $0，补进 pricing.json')
        lines.append(f'  ❌ {k}: {v:,} tok 无单价')
else:
    lines.append(f'  ✅ 在用 {len(seen)} 个模型全部有单价')

# ── 4. CONFIG DRIFT — config 里的 agent 是否都在 dashboard 内 ────
lines.append('[4] CONFIG DRIFT — agent 覆盖')
try:
    cfg = json.load(open(OPENCLAW_CONFIG))
    cfg_agents = {a['id'] for a in cfg.get('agents', {}).get('list', []) if a.get('id')}
    missing = cfg_agents - DASHBOARD_AGENTS
    # 只提示「新 agent 未纳入」；已知不展示的（如未来临时 agent）需人工判断
    if missing:
        lines.append(f'  ⚠️ config 有 agent 不在 dashboard: {missing}（如需展示请加入 DASHBOARD_AGENTS/AGENTS）')
    else:
        lines.append(f'  ✅ config agent 全部已纳入 dashboard')
    stale_dash = DASHBOARD_AGENTS - cfg_agents
    if stale_dash:
        issues.append(f'dashboard 展示了 config 里已不存在的 agent: {stale_dash}')
        lines.append(f'  ❌ dashboard 有已删除 agent: {stale_dash}')
except Exception as e:
    lines.append(f'  ⚠️ 无法读 openclaw.json: {e}')

# ── 汇总 ─────────────────────────────────────────────────────────
header = [f'=== S.H.R.I.M.P. Dashboard 自检 · {now.strftime("%Y-%m-%d %H:%M")} ===', '']
tail = ['']
if issues:
    tail.append(f'🔴 {len(issues)} 项异常需处理:')
    for i in issues:
        tail.append(f'  • {i}')
else:
    tail.append('✅ 全部正常，dashboard 自我维护健康。')

report = '\n'.join(header + lines + tail)
print(report)
open('/tmp/shrimp-selfcheck-report.txt', 'w').write(report)
sys.exit(1 if issues else 0)
