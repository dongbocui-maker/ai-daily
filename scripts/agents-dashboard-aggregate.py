#!/usr/bin/env python3
import json, glob, time, os, re, subprocess
from collections import defaultdict
from datetime import datetime, timezone, timedelta

# ===== CAPABILITY MATRIX: 自动扫描各 agent workspace 的 SKILL.md frontmatter =====
# 动态：装/卸 skill 后重跑本脚本即自动反映。无需手维护。
# 输出 out['capabilities'] = {domains:[...], total, shared, ws_scoped, ndomains, generated_at}
_CAP_WS = {
    'main':  '/root/.openclaw/workspace/skills',
    'mk2':   '/root/.openclaw/workspace-mk2/skills',
    'mk46':  '/root/.openclaw/workspace-mk46/skills',
    'aima':  '/root/.openclaw/workspace-aima/skills',
    'claude-researcher': '/root/.openclaw/workspace-mk51/skills',
}
_CAP_AGENT_LABEL = {'main':'MAIN','mk2':'MK2','mk46':'MK46','aima':'AIMA','claude-researcher':'MK51'}
# bundled/extension skills（全 agent 共享）扫描根；通配 openclaw 安装目录
_CAP_BUNDLED_GLOBS = [
    '/root/.local/share/pnpm/global/*/.pnpm/openclaw@*/node_modules/openclaw/skills',
    '/root/.local/share/pnpm/global/*/.pnpm/openclaw@*/node_modules/openclaw/dist/extensions/*/skills',
]
# 能力域顺序（全大写英文）
_CAP_ORDER = ['DOCS & KB','WEB & RESEARCH','COMMS','OPS & AUTO','MEDIA & DESIGN','UTILITY']

def _cap_parse_frontmatter(path):
    try:
        txt = open(path, encoding='utf-8', errors='ignore').read()
    except Exception:
        return None
    m = re.match(r'^---\s*\n(.*?)\n---', txt, re.S)
    fm = m.group(1) if m else ''
    def grab(k):
        mm = re.search(rf'^{k}:\s*(.+)$', fm, re.M)
        return mm.group(1).strip() if mm else ''
    name = grab('name'); desc = grab('description'); emoji=''; cat=''
    meta = grab('metadata')
    if meta:
        try:
            j=json.loads(meta); oc=j.get('openclaw',{})
            emoji=oc.get('emoji',''); cat=oc.get('category','')
        except Exception:
            pass
    return {'name':name,'desc':(desc or '')[:90],'emoji':emoji,'cat':cat}

def _cap_scan(root):
    out={}
    if not os.path.isdir(root):
        return out
    for d in sorted(os.listdir(root)):
        sk = os.path.join(root,d,'SKILL.md')
        if os.path.isfile(sk):
            info=_cap_parse_frontmatter(sk)
            if info:
                out[info['name'] or d]=info
    return out

def _cap_domain(name, info):
    n=(name+' '+(info.get('cat') or '')+' '+(info.get('desc') or '')).lower()
    if any(k in n for k in ['feishu','wiki','tencent-doc','docs','notion','obsidian','bear','apple-notes','dws','knowledge']): return 'DOCS & KB'
    if any(k in n for k in ['web','tavily','research','browser','search','blogwatch','xurl']): return 'WEB & RESEARCH'
    if any(k in n for k in ['discord','slack','message','imsg','bluebubble','voice-call','wacli','himalaya','mail']): return 'COMMS'
    if any(k in n for k in ['cron','healthcheck','governance','acp','tmux','node-connect','mcporter','taskflow','clawhub','skill-creator','lighthouse','oracle','session']): return 'OPS & AUTO'
    if any(k in n for k in ['ppt','brand','diagram','excalidraw','frontend','design','sag','tts','whisper','video','gif','song','spotify','canvas','camsnap','peekaboo','nano-pdf']): return 'MEDIA & DESIGN'
    return 'UTILITY'

def build_capabilities():
    agent_skills={a:_cap_scan(p) for a,p in _CAP_WS.items()}
    bundled={}
    for pat in _CAP_BUNDLED_GLOBS:
        for root in glob.glob(pat):
            bundled.update(_cap_scan(root))
    skills={}
    for a, s in agent_skills.items():
        for name, info in s.items():
            skills.setdefault(name, {'info':info,'agents':set(),'bundled':False})
            skills[name]['agents'].add(a)
    for name, info in bundled.items():
        skills.setdefault(name, {'info':info,'agents':set(),'bundled':False})
        skills[name]['bundled']=True
    groups={}
    for name, d in skills.items():
        groups.setdefault(_cap_domain(name, d['info']), []).append((name,d))
    domains=[]
    for g in _CAP_ORDER:
        items=sorted(groups.get(g,[]), key=lambda x:x[0])
        if not items: continue
        def srlow(name,d):
            info=d['info']
            return {'name':name.upper(),'desc':(info.get('desc') or '').upper(),
                    'emoji':info.get('emoji') or '▣',
                    'shared':d['bundled'],
                    'agents':sorted(_CAP_AGENT_LABEL.get(a,a.upper()) for a in d['agents'])}
        ws=[srlow(n,d) for n,d in items if not d['bundled']]
        bd=[srow for srow in (srlow(n,d) for n,d in items if d['bundled'])]
        domains.append({'domain':g,'total':len(items),'ws':len(ws),'shared':len(bd),
                        'ws_skills':ws,'shared_skills':bd})
    total=len(skills); shared=sum(1 for d in skills.values() if d['bundled'])
    return {'domains':domains,'total':total,'shared':shared,'ws_scoped':total-shared,
            'ndomains':len(domains)}

# 单价表 USD / 1M tokens  (input, output, cacheWrite, cacheRead)
PRICING = {
    ('azure-claude-48','claude-opus-4-8'): (5.00,25.00,6.25,0.50),
    ('aigw-claude-48-main','claude-opus-4-8'): (5.00,25.00,6.25,0.50),
    ('aigw-claude-48-main','claude-fable-5'):   (10.00,50.00,12.50,1.00),
    ('azure-claude','claude-opus-4-7'):    (5.00,25.00,6.25,0.50),
    ('azure-openai-responses','gpt-5.5'):  (1.25,10.00,1.25,0.125),
    ('anthropic','claude-sonnet-4-6'):      (3.00,15.00,3.75,0.30),
    ('deepseek','deepseek-v4-pro'):        (0.435,0.87,0.435,0.003625),
    ('deepseek','DeepSeek-V4-Pro'):        (0.435,0.87,0.435,0.003625),
    # qwen3.7-max @ DashScope，价格为估算（公开源称 ~$1.25/M in），待 pricing-sync 核对
    ('qwen','qwen3.7-max'):                (1.25,5.00,1.25,0.125),
}
def price(prov,model):
    return PRICING.get((prov,model)) or PRICING.get((prov,(model or '').lower())) or (0,0,0,0)

# 模型标识规范化：同一模型不同大小写写法（如 deepseek-v4-pro / DeepSeek-V4-Pro）
# 归并到统一展示名，避免 POWER CONSUMPTION 表与 per-agent ⚡行出现重复行。
# key 用全小写匹配，value 是标准展示名。
MODEL_CANON = {
    'deepseek-v4-pro': 'DeepSeek-V4-Pro',
}
def canon_model(model):
    if not model: return model
    return MODEL_CANON.get(model.lower(), model)

AGENTS = {
    'main':{'name':'钢铁虾','mark':'MARK I','role':'ORCHESTRATOR','emoji':'🦐','ac':'#e8b923','lit':'#7fdfff'},
    'aima':{'name':'银月','mark':'P.E.P.P.E.R.','role':'PERSONAL ASSISTANT','emoji':'🌶️','ac':'#e89bb8','lit':'#ffd0e6'},
    'mk2': {'name':'MK2','mark':'MARK II','role':'ENGINEER','emoji':'🦐','ac':'#cfdbe6','lit':'#9fe8ff'},
    'mk46':{'name':'Mark 46','mark':'MARK XLVI','role':'QC AUDITOR','emoji':'🛡','ac':'#caa6ff','lit':'#e0c4ff'},
    'claude-researcher':{'name':'MK51 哨兵','mark':'MARK LI','role':'SENTINEL RESEARCHER','emoji':'🛰️','ac':'#4fd4ff','lit':'#b8f3ff'},
}

# Signal/Fallback 规则：从 OpenClaw 配置读取各 Agent primary model。
# active_model 只要偏离 primary，就视为 fallback；无论自动 fallback 还是手动 session model override，
# 下一次 model.completed 被聚合后都会被捕捉并写入 Signal。
# 注意：Claude CLI runtime 不一定写 model.completed trajectory；需从 session store 补当前 runtime/model，
# 否则 dashboard 会把切换前最后一次 provider fallback 误当成当前 active model。
OPENCLAW_CONFIG = '/root/.openclaw/openclaw.json'
SIGNAL_NAMES = {
    'main': 'MAIN AGENT',
    'aima': 'SILVERMOON AGENT',
    'mk2': 'MK2 AGENT',
    'mk46': 'MK46 AGENT',
    'claude-researcher': 'MK51 SENTINEL',
}
MODEL_LABELS = {
    'azure-claude-48/claude-opus-4-8': 'AZURE CLAUDE 4.8',
    'aigw-claude-48-main/claude-opus-4-8': 'OPUS-4.8',
    'aigw-claude-48-main/claude-fable-5': 'AIGW FABLE 5',
    'azure-claude/claude-opus-4-7': 'AZURE CLAUDE 4.7',
    'azure-openai-responses/gpt-5.5': 'GPT-5.5',
    'deepseek/DeepSeek-V4-Pro': 'DEEPSEEK V4 PRO',
    'qwen/qwen3.7-max': 'QWEN3.7 MAX',
    'anthropic/claude-sonnet-4-6': 'SONNET 4.6',
}
EVENT_TARGETS = [
    '/root/.openclaw/workspace/projects/agents-dashboard/events.json',
    '/root/.openclaw/workspace/projects/ai-daily/public/agents/data/events.json',
    '/root/.openclaw/workspace/projects/agents-dashboard/live/events.json',
]
FALLBACK_STATE_PATH = '/root/.openclaw/workspace/projects/agents-dashboard/fallback-state.json'
MAX_SIGNAL_EVENTS = 50

def _load_json(path, default):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return default

def _agent_config_map():
    cfg = _load_json(OPENCLAW_CONFIG, {})
    return {item.get('id'): item for item in ((cfg.get('agents') or {}).get('list') or []) if item.get('id')}

def _primary_models_from_config():
    cfg = _load_json(OPENCLAW_CONFIG, {})
    defaults = ((cfg.get('agents') or {}).get('defaults') or {}).get('model') or {}
    default_primary = defaults.get('primary')
    primaries = {}
    for aid, item in _agent_config_map().items():
        if aid not in AGENTS:
            continue
        model_cfg = item.get('model') or {}
        primaries[aid] = model_cfg.get('primary') or default_primary
    for aid in AGENTS:
        primaries.setdefault(aid, default_primary)
    return primaries

def _session_ms_to_iso(ms):
    try:
        return datetime.fromtimestamp(float(ms)/1000, timezone.utc).isoformat().replace('+00:00','Z')
    except Exception:
        return None

def _canonical_active_from_session(aid):
    """Return (active_model, last_ts) from latest session store entry.

    Claude CLI sessions expose provider/model in sessions.json even when no model.completed
    usage record is written. For dashboard fallback detection we normalize Claude CLI models
    back to their canonical OpenClaw model ref (anthropic/...), matching config.primary.
    """
    sp = f'/root/.openclaw/agents/{aid}/sessions/sessions.json'
    data = _load_json(sp, {})
    best = None
    for key, s in (data or {}).items():
        if not isinstance(s, dict):
            continue
        upd = s.get('updatedAt') or s.get('lastUpdatedAt') or 0
        if best is None or upd > best[0]:
            best = (upd, s)
    if not best:
        return None, None
    upd, s = best
    provider = s.get('modelProvider') or s.get('providerOverride')
    model = s.get('model') or s.get('modelOverride')
    if not provider or not model:
        return None, None
    model = canon_model(model)
    if provider == 'claude-cli' and str(model).startswith('claude-'):
        active = f'anthropic/{model}'
    else:
        active = f'{provider}/{model}'
    return active, _session_ms_to_iso(upd)

def _event_ts_cn(ts):
    if ts:
        try:
            return datetime.fromisoformat(ts.replace('Z','+00:00')).astimezone(CN_TZ).strftime('%Y-%m-%dT%H:%M+08:00')
        except Exception:
            pass
    return now.strftime('%Y-%m-%dT%H:%M+08:00')

def _model_label(model):
    return MODEL_LABELS.get(model, model).upper()

def refresh_fallback_events(agents):
    """Persist Signal events from actual route changes.

    Captures:
    - primary -> fallback
    - fallback -> different fallback
    - fallback -> primary recovery
    - current fallback still active but missing from events (backfill)
    """
    primary_models = _primary_models_from_config()
    state = _load_json(FALLBACK_STATE_PATH, {})
    base = _load_json(EVENT_TARGETS[1], {'updated': now.strftime('%Y-%m-%dT%H:%M+08:00'), 'events': []})
    base_events = base.get('events', []) or []
    existing_fallback = [e for e in base_events if str(e.get('tag','')).upper() == 'FALLBACK']
    new_events = []

    def push(ts, level, msg, detail=''):
        msg = msg.upper()
        if any(e.get('msg') == msg for e in new_events + existing_fallback):
            return
        new_events.append({'ts': ts, 'level': level, 'tag': 'FALLBACK', 'msg': msg, 'detail': detail[:200] if detail else ''})

    for aid, agent in agents.items():
        current = agent.get('active_model')
        primary = primary_models.get(aid)
        if not current or not primary:
            continue
        st = state.get(aid) or {}
        prev = st.get('active_model')
        stored_primary = st.get('primary_model')
        prev_primary = st.get('prev_primary')
        primary_since = st.get('primary_since')
        name = SIGNAL_NAMES.get(aid, aid.upper())
        ts = _event_ts_cn(agent.get('last_ts'))
        # 配置变更检测：primary 被改时记下变更时刻与旧 primary，
        # 变更前的调用按旧基准评判，避免换模型日产生大量伪 FALLBACK 告警 (AUDIT-2026-06-11 后续)
        if stored_primary and stored_primary != primary:
            prev_primary = stored_primary
            primary_since = now.strftime('%Y-%m-%dT%H:%M:%S+08:00')
            push(primary_since, 'info', f'{name} PRIMARY CHANGED - {_model_label(stored_primary)} -> {_model_label(primary)}')
        # 调用发生时刻生效的 primary：早于变更时刻的调用用旧 primary 评判
        eff_primary = primary
        if primary_since and prev_primary:
            try:
                call_dt = datetime.fromisoformat(str(agent.get('last_ts','')).replace('Z','+00:00'))
                since_dt = datetime.fromisoformat(primary_since)
                if call_dt < since_dt:
                    eff_primary = prev_primary
            except Exception:
                pass
        if current != eff_primary:
            if prev and prev != current and prev != eff_primary:
                push(ts, 'warn', f'{name} FALLBACK ROUTE CHANGED - {_model_label(prev)} -> {_model_label(current)}')
            else:
                push(ts, 'warn', f'{name} FALLBACK ACTIVE - {_model_label(eff_primary)} ROUTED TO {_model_label(current)}')
        elif prev and prev != eff_primary:
            push(ts, 'info', f'{name} FALLBACK CLEARED - ROUTED BACK TO PRIMARY {_model_label(current)}')
        state[aid] = {
            'active_model': current,
            'primary_model': primary,
            'prev_primary': prev_primary,
            'primary_since': primary_since,
            'updated': now.strftime('%Y-%m-%dT%H:%M:%S+08:00')
        }

    # Signal 保留所有事件，排序规则：FALLBACK 优先，其它事件按优先级与时间往后排；同一 tag+msg 去重。
    merged = new_events + base_events
    priority = {'FALLBACK': 0, 'ALERT': 1, 'QC': 2, 'DEPLOY': 3}
    seen = set(); deduped = []
    def sort_key(e):
        tag = str(e.get('tag','')).upper()
        ts = str(e.get('ts',''))
        try:
            ts_rank = -datetime.fromisoformat(ts.replace('Z','+00:00')).timestamp()
        except Exception:
            ts_rank = 0
        return (priority.get(tag, 9), ts_rank)
    for e in sorted(merged, key=sort_key):
        msg = e.get('msg','').strip().upper()
        tag = str(e.get('tag','')).upper()
        if not msg:
            continue
        key = (tag, msg)
        if key in seen:
            continue
        seen.add(key)
        e['tag'] = tag
        e['msg'] = msg
        deduped.append(e)
    event_list = deduped[:MAX_SIGNAL_EVENTS]
    events_changed = json.dumps(base.get('events', []), sort_keys=True) != json.dumps(event_list, sort_keys=True)
    out_events = {
        'updated': now.strftime('%Y-%m-%dT%H:%M+08:00') if events_changed else base.get('updated', now.strftime('%Y-%m-%dT%H:%M+08:00')),
        'events': event_list,
    }
    if events_changed or any(not os.path.exists(path) for path in EVENT_TARGETS):
        for path in EVENT_TARGETS:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            json.dump(out_events, open(path, 'w'), ensure_ascii=True, indent=2)
    old_state = _load_json(FALLBACK_STATE_PATH, {})
    if old_state != state:
        os.makedirs(os.path.dirname(FALLBACK_STATE_PATH), exist_ok=True)
        json.dump(state, open(FALLBACK_STATE_PATH, 'w'), ensure_ascii=True, indent=2)
    return len(new_events), len(out_events['events'])
CN_TZ = timezone(timedelta(hours=8))
now = datetime.now(CN_TZ)
today = now.strftime('%Y-%m-%d')
# 近 7 天日期（含今天）的 YYYY-MM-DD 列表，用于趋势图 + last7d 累计
last7_days = [(now - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]
last7_set = set(last7_days)

# ===== MISSION QUEUE · cron 采集（只取 main/mk2，脱敏，不含任务 prompt）=====
# 允许展示的 agent（银月 aima 等个人任务不展示）
CRON_AGENTS = {'main', 'mk2'}
# 核心每日任务（站点命脉，前端加 ★ 高亮）
CRON_CORE = {'ai-daily-report', 'follow builders digest'}

def _cron_human(expr, kind):
    """cron 表达式 -> 人话频率（常见模式，其余原样返回）"""
    if kind == 'at':
        return '单次'
    if not expr:
        return ''
    parts = expr.split()
    if len(parts) != 5:
        return expr
    mi, ho, dom, mon, dow = parts
    hhmm = ''
    if mi.isdigit() and ho.isdigit():
        hhmm = f'{int(ho):02d}:{int(mi):02d}'
    week = {'0':'日','1':'一','2':'二','3':'三','4':'四','5':'五','6':'六','7':'日'}
    if dom == '*' and mon == '*' and dow == '*':
        return f'每天 {hhmm}'.strip()
    if dom == '*' and mon == '*' and dow in week:
        return f'每周{week[dow]} {hhmm}'.strip()
    if dom == '*' and mon == '*' and ',' in dow:
        days = '/'.join(week.get(d, d) for d in dow.split(','))
        return f'每周{days} {hhmm}'.strip()
    if mon != '*' and dom.isdigit():
        return f'季度首日 {hhmm}'.strip() if mon == '1,4,7,10' else f'{mon}月{dom}日 {hhmm}'.strip()
    return expr

def _prev_crons():
    """读上一次写入的 fallback JSON 里的 crons，作为采集失败时的兑底（A 方案）。"""
    for p in ('/root/.openclaw/workspace/projects/ai-daily/public/agents/data/dashboard-fallback.json',
              '/root/.openclaw/workspace/projects/agents-dashboard/live/dashboard-data.json'):
        try:
            prev = json.load(open(p))
            cs = prev.get('crons')
            if isinstance(cs, list) and cs:
                return cs
        except Exception:
            continue
    return []

def collect_crons():
    """调 openclaw cron list --json，返回脱敏后的 cron 列表（仅 main/mk2）。
    只取元字段：id/name/agent/schedule/state；绝不输出 payload.message。
    写入绝对时间戳 next_run_ms 供前端实时算倒计时。
    A 方案：采集失败（CLI 不可用/超时/解析错）时保留上一次数据，不覆盖成空。"""
    bin_candidates = ['/root/.local/share/pnpm/openclaw', 'openclaw']
    raw = None
    last_err = ''
    for b in bin_candidates:
        try:
            res = subprocess.run([b, 'cron', 'list', '--json'],
                                 capture_output=True, text=True, timeout=30)
            raw = res.stdout
            if raw and raw.strip():
                break
            last_err = (res.stderr or '').strip()[:200]
        except Exception as e:
            last_err = f'{type(e).__name__}: {e}'[:200]
            continue
    if not raw:
        # 不静默吞：记一条诊断便于线上排错，同时保留上次数据（A 方案）
        print(f'[mission-queue] cron collect failed, keeping previous: {last_err or "empty output"}')
        return _prev_crons()
    try:
        data = json.loads(raw)
    except Exception:
        return _prev_crons()
    jobs = data.get('jobs', data) if isinstance(data, dict) else data
    out_crons = []
    for j in jobs:
        aid = j.get('agentId')
        if aid not in CRON_AGENTS:
            continue
        sc = j.get('schedule') or {}
        st = j.get('state') or {}
        name = j.get('name') or j.get('id', '')
        kind = sc.get('kind', 'cron')
        expr = sc.get('expr', '')
        last_status = st.get('lastStatus') or st.get('lastRunStatus')
        if last_status:
            last_status = str(last_status).lower()
        out_crons.append({
            'id': j.get('id'),
            'name': name,
            'agent': aid,
            'enabled': bool(j.get('enabled', True)),
            'expr': expr if kind != 'at' else 'at',
            'human': _cron_human(expr, kind),
            'kind': kind,
            'next_run_ms': st.get('nextRunAtMs'),
            'last_run_ms': st.get('lastRunAtMs'),
            'last_status': last_status,           # ok / error / skipped / None
            'core': name.strip().lower() in CRON_CORE,
        })
    # 排序：核心置顶 -> 按下次运行时间升序
    out_crons.sort(key=lambda c: (not c['core'], c['next_run_ms'] or 9e18))
    # A 方案补充：CLI 返回了但 main/mk2 一条都没匹配到（异常），也保留上一次
    if not out_crons:
        return _prev_crons()
    return out_crons

def ts_to_cn_date(ts):
    """trajectory ts 是 UTC ISO，转北京日期"""
    try:
        dt = datetime.fromisoformat(ts.replace('Z','+00:00')).astimezone(CN_TZ)
        return dt.strftime('%Y-%m-%d')
    except: return None

agents_out = {}
model_totals = defaultdict(lambda:{'tok':0,'cost':0.0,'calls':0})
grand = {'tok':0,'cost':0.0,'calls':0,'save':0.0,
         'today_tok':0,'today_cost':0.0,'today_calls':0,'today_save':0.0,
         'last7d_tok':0,'last7d_cost':0.0,'last7d_calls':0}
# 全局趋势：按北京日期聚合 token+cost
daily_trend = defaultdict(lambda:{'tok':0,'cost':0.0})
# per-agent 每日明细：{date: {aid: {'tok':,'cost':}}}
daily_agent = defaultdict(lambda: defaultdict(lambda:{'tok':0,'cost':0.0}))

agent_cfg = _agent_config_map()

for aid,meta in AGENTS.items():
    by_model = defaultdict(lambda:{'input':0,'output':0,'cacheRead':0,'cacheWrite':0,'total':0,'calls':0,'cost':0.0,'save':0.0})
    last_ts = None
    last_model = None
    today_tok = 0; today_cost = 0.0; today_save = 0.0
    today_cr = 0; today_in = 0  # 当天缓存命中率用：cacheRead / (input+cacheRead+cacheWrite)
    last7d_tok = 0; last7d_cost = 0.0
    for f in glob.glob(f'/root/.openclaw/agents/{aid}/sessions/*.trajectory.jsonl'):
        try:
            for line in open(f):
                try: d=json.loads(line)
                except: continue
                if d.get('type')!='model.completed': continue
                prov=d.get('provider'); model=canon_model(d.get('modelId'))
                u=(d.get('data') or {}).get('usage') or {}
                if not u: continue
                inp=u.get('input',0) or 0; out=u.get('output',0) or 0
                cr=u.get('cacheRead',0) or 0; cw=u.get('cacheWrite',0) or 0
                tot=u.get('total',0) or (inp+out+cr+cw)
                pi,po,pcw,pcr = price(prov,model)
                cost = inp/1e6*pi + out/1e6*po + cw/1e6*pcw + cr/1e6*pcr
                # 节省额：若 cacheRead 按 full input 价算的差额
                save = cr/1e6*(pi-pcr)
                key=f'{prov}/{model}'
                m=by_model[key]
                m['input']+=inp; m['output']+=out; m['cacheRead']+=cr; m['cacheWrite']+=cw
                m['total']+=tot; m['calls']+=1; m['cost']+=cost; m['save']+=save
                ts=d.get('ts')
                if ts and (last_ts is None or ts>last_ts):
                    last_ts=ts
                    last_model=key
                cn_date = ts_to_cn_date(ts) if ts else None
                if cn_date==today:
                    today_tok+=tot; today_cost+=cost; today_save+=save
                    today_cr+=cr; today_in+=(inp+cr+cw)
                if cn_date in last7_set:
                    last7d_tok+=tot; last7d_cost+=cost
                    daily_trend[cn_date]['tok']+=tot; daily_trend[cn_date]['cost']+=cost
                    daily_agent[cn_date][aid]['tok']+=tot; daily_agent[cn_date][aid]['cost']+=cost
        except: pass
    a_tok=sum(m['total'] for m in by_model.values())
    a_cost=sum(m['cost'] for m in by_model.values())
    a_calls=sum(m['calls'] for m in by_model.values())
    a_save=sum(m['save'] for m in by_model.values())
    cr_sum=sum(m['cacheRead'] for m in by_model.values())
    in_sum=sum(m['input']+m['cacheRead']+m['cacheWrite'] for m in by_model.values())
    eff = (cr_sum/in_sum*100) if in_sum else 0

    # Claude CLI runtime 当前模型补偿：CLI 调用目前不稳定写入 model.completed trajectory，
    # 以 sessions.json 的最新 modelProvider/model 作为 active_model 与活跃时间源。
    runtime_id = (((agent_cfg.get(aid) or {}).get('agentRuntime') or {}).get('id'))
    if runtime_id == 'claude-cli':
        sess_model, sess_ts = _canonical_active_from_session(aid)
        if sess_model and sess_ts and (not last_ts or sess_ts > last_ts):
            last_model = sess_model
            last_ts = sess_ts

    # 健康：last_ts 距今
    status='OFFLINE'; mins=None
    if last_ts:
        try:
            lt=datetime.fromisoformat(last_ts.replace('Z','+00:00'))
            mins=(datetime.now(timezone.utc)-lt).total_seconds()/60
            status='ONLINE' if mins<60 else ('IDLE' if mins<1440 else 'OFFLINE')
        except: pass
    for k,m in by_model.items():
        model_totals[k]['tok']+=m['total']; model_totals[k]['cost']+=m['cost']; model_totals[k]['calls']+=m['calls']
    grand['tok']+=a_tok; grand['cost']+=a_cost; grand['calls']+=a_calls; grand['save']+=a_save
    grand['today_tok']+=today_tok; grand['today_cost']+=today_cost; grand['today_save']+=today_save
    grand['last7d_tok']+=last7d_tok; grand['last7d_cost']+=last7d_cost
    today_eff = (today_cr/today_in*100) if today_in else 0
    agents_out[aid]={**meta,'status':status,'idle_min':round(mins) if mins is not None else None,
        'last_ts':last_ts,
        'total_tok':a_tok,'today_tok':today_tok,'today_cost':round(today_cost,2),
        'last7d_tok':last7d_tok,'last7d_cost':round(last7d_cost,2),
        'cost':round(a_cost,2),'save':round(a_save,2),
        'calls':a_calls,'active_model':last_model,'cache_eff':round(eff,1),'today_cache_eff':round(today_eff,1),
        'models':sorted([{'name':k,'tok':v['total'],'cost':round(v['cost'],2),'calls':v['calls']} for k,v in by_model.items()],key=lambda x:-x['tok'])}

trend = [{'date':d,'tok':daily_trend[d]['tok'],'cost':round(daily_trend[d]['cost'],2),
          'by_agent':{aid:{'name':AGENTS[aid]['name'],'mark':AGENTS[aid]['mark'],'emoji':AGENTS[aid]['emoji'],
                           'tok':daily_agent[d][aid]['tok'],'cost':round(daily_agent[d][aid]['cost'],2)}
                      for aid in AGENTS if daily_agent[d][aid]['tok']>0}}
         for d in last7_days]
out={'generated_at':now.strftime('%Y-%m-%d %H:%M:%S +08'),'today':today,
     'grand':{'tok':grand['tok'],'cost':round(grand['cost'],2),'calls':grand['calls'],'save':round(grand['save'],2),
              'today_tok':grand['today_tok'],'today_cost':round(grand['today_cost'],2),'today_save':round(grand['today_save'],2),
              'last7d_tok':grand['last7d_tok'],'last7d_cost':round(grand['last7d_cost'],2)},
     'trend':trend,
     'agents':agents_out,
     'capabilities':build_capabilities(),
     'crons':collect_crons(),
     'models':sorted([{'name':k,**{kk:(round(vv,2) if kk=='cost' else vv) for kk,vv in v.items()}} for k,v in model_totals.items()],key=lambda x:-x['tok'])}
new_fallback_events, total_signal_events = refresh_fallback_events(agents_out)
# 输出到两处：
#  1) ai-daily 仓库内 git 跟踪的 fallback 快照（tunnel 挂了时站点兜底，由 deploy 脚本低频 commit）
#  2) 实时服务(serve.py @8787)读的 live/ 路径（经 Cloudflare Tunnel data.aidigest.club 实时服务，不入 git）
# 注：旧的 public/agents/data/dashboard-data.json 已 gitignore 弃用（AUDIT-2026-06-11 M2），改写 fallback。
import os as _os
_targets = [
    '/root/.openclaw/workspace/projects/ai-daily/public/agents/data/dashboard-fallback.json',
    '/root/.openclaw/workspace/projects/agents-dashboard/live/dashboard-data.json',
]
for _t in _targets:
    _os.makedirs(_os.path.dirname(_t), exist_ok=True)
    json.dump(out, open(_t,'w'), ensure_ascii=False, indent=2)
print('OK grand tok=%s cost=$%s save=$%s signal=%s(+%s)'%(out['grand']['tok'],out['grand']['cost'],out['grand']['save'],total_signal_events,new_fallback_events))
