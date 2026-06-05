#!/usr/bin/env python3
import json, glob, time, os
from collections import defaultdict
from datetime import datetime, timezone, timedelta

# 单价表 USD / 1M tokens  (input, output, cacheWrite, cacheRead)
PRICING = {
    ('azure-claude-48','claude-opus-4-8'): (5.00,25.00,6.25,0.50),
    ('azure-claude','claude-opus-4-7'):    (5.00,25.00,6.25,0.50),
    ('azure-openai-responses','gpt-5.5'):  (1.25,10.00,1.25,0.125),
    ('deepseek','deepseek-v4-pro'):        (0.435,0.87,0.435,0.003625),
    ('deepseek','DeepSeek-V4-Pro'):        (0.435,0.87,0.435,0.003625),
}
def price(prov,model):
    return PRICING.get((prov,model)) or PRICING.get((prov,(model or '').lower())) or (0,0,0,0)

AGENTS = {
    'main':{'name':'钢铁虾','mark':'MARK I','role':'ORCHESTRATOR','emoji':'🦐'},
    'aima':{'name':'银月','mark':'P.E.P.P.E.R.','role':'PERSONAL ASSISTANT','emoji':'🌶️'},
    'mk2': {'name':'MK2','mark':'MARK II','role':'ENGINEER','emoji':'🦐'},
    'mk46':{'name':'Mark 46','mark':'MARK XLVI','role':'QC AUDITOR','emoji':'🛡'},
}
CN_TZ = timezone(timedelta(hours=8))
now = datetime.now(CN_TZ)
today = now.strftime('%Y-%m-%d')
# 近 7 天日期（含今天）的 YYYY-MM-DD 列表，用于趋势图 + last7d 累计
last7_days = [(now - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]
last7_set = set(last7_days)

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

for aid,meta in AGENTS.items():
    by_model = defaultdict(lambda:{'input':0,'output':0,'cacheRead':0,'cacheWrite':0,'total':0,'calls':0,'cost':0.0,'save':0.0})
    last_ts = None
    today_tok = 0; today_cost = 0.0; today_save = 0.0
    today_cr = 0; today_in = 0  # 当天缓存命中率用：cacheRead / (input+cacheRead+cacheWrite)
    last7d_tok = 0; last7d_cost = 0.0
    for f in glob.glob(f'/root/.openclaw/agents/{aid}/sessions/*.trajectory.jsonl'):
        try:
            for line in open(f):
                try: d=json.loads(line)
                except: continue
                if d.get('type')!='model.completed': continue
                prov=d.get('provider'); model=d.get('modelId')
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
                if ts and (last_ts is None or ts>last_ts): last_ts=ts
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
        'total_tok':a_tok,'today_tok':today_tok,'today_cost':round(today_cost,2),
        'last7d_tok':last7d_tok,'last7d_cost':round(last7d_cost,2),
        'cost':round(a_cost,2),'save':round(a_save,2),
        'calls':a_calls,'cache_eff':round(eff,1),'today_cache_eff':round(today_eff,1),
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
     'models':sorted([{'name':k,**{kk:(round(vv,2) if kk=='cost' else vv) for kk,vv in v.items()}} for k,v in model_totals.items()],key=lambda x:-x['tok'])}
# 输出到两处：
#  1) 站点 build 用的静态 fallback JSON
#  2) 实时服务(serve.py @8787)读的 live/ 路径
import os as _os
_targets = [
    '/root/.openclaw/workspace/projects/ai-daily/public/agents/data/dashboard-data.json',
    '/root/.openclaw/workspace/projects/agents-dashboard/live/dashboard-data.json',
]
for _t in _targets:
    _os.makedirs(_os.path.dirname(_t), exist_ok=True)
    json.dump(out, open(_t,'w'), ensure_ascii=False, indent=2)
print('OK grand tok=%(tok)s cost=$%(cost)s save=$%(save)s'%out['grand'])
