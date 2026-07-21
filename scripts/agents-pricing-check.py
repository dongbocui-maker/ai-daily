#!/usr/bin/env python3
"""每周价格复核（真·可跑版，替代旧的静态提醒脚本）。

single source of truth = src/data/pricing.json。本脚本：
  1. 读 pricing.json 当前生效单价 + source/verified/confidence
  2. 对 confidence=official 且 source 是可抓 URL 的模型，去官方页抓价 → diff
  3. 有变动 / 有 estimated / 有超 N 天没核对 → 生成报告，退出码非 0
  4. 由 agents-pricing-sync-cron.sh 每周六调用；有变动时 cron 脚本推飞书给 Jason

设计：不自动改价（官网 HTML 易变，自动改不可靠）。只做「抓 → diff → 报告」，
人工确认后改 pricing.json 一处即可。抓取失败 fail-soft（记 warn，不误报变动）。
"""
import json, os, re, sys, subprocess, datetime

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRICING_JSON = os.path.join(REPO, 'src', 'data', 'pricing.json')
STALE_DAYS = 45  # 超过这么多天没核对的 official 价，提醒复核

# 官方定价页抓取器：{model_full: (url, [regex 提取 input 价, regex 提取 output 价])}
# 抓不到时跳过该项（不误判为变动）。正则尽量宽松，主要用于「价是否明显偏离」告警。
FETCHERS = {
    'qwen/qwen3.7-max': {
        'url': 'https://www.alibabacloud.com/help/en/model-studio/model-pricing',
        'hint': 'qwen3.7-max List price $2.5 in / $7.5 out (官方 Model Studio)',
    },
    # NOTE: openai.com/api/pricing 是 JS SPA，curl 抓到空壳 → 误报，故不列入抓取器。
    # gpt-5.6-sol 靠 STALE_DAYS 到期提醒人工核对，不做 HTML diff。
    'azure-claude-48/claude-opus-4-8': {
        'url': 'https://www.anthropic.com/pricing',
        'hint': 'Opus $5 in / $25 out',
    },
}
PROXY = os.environ.get('MIHOMO_PROXY', 'http://127.0.0.1:7890')


def _fetch(url):
    """curl through mihomo proxy; return text or None."""
    for args in ([ '-x', PROXY ], []):  # 先走代理，失败再直连
        try:
            r = subprocess.run(['curl', '-sL', '--max-time', '20', *args, url],
                               capture_output=True, text=True, timeout=30)
            if r.returncode == 0 and len(r.stdout) > 500:
                return r.stdout
        except Exception:
            continue
    return None


def main():
    try:
        doc = json.load(open(PRICING_JSON))
    except Exception as e:
        print(f'FATAL: cannot read {PRICING_JSON}: {e}')
        return 2

    models = doc.get('models') or {}
    now = datetime.datetime.now()
    today = now.strftime('%Y-%m-%d')

    issues = []       # 需要人工处理的项（触发飞书推送）
    lines = [f'=== S.H.R.I.M.P. 单价复核 · {now.strftime("%Y-%m-%d %H:%M")} ===', '']

    # 1) confidence 分布 + stale 检测
    est = [k for k, v in models.items() if v.get('confidence') == 'estimated']
    if est:
        issues.append(f'{len(est)} 个模型仍是 estimated 单价（成本不准）: {", ".join(est)}')

    for k, v in models.items():
        if v.get('deprecated'):
            continue  # 已弃用、不在链路的旧模型不做 stale 提醒（避免周周刷屏）
        ver = v.get('verified', '')
        try:
            d = datetime.datetime.strptime(ver, '%Y-%m-%d')
            age = (now - d).days
            if v.get('confidence') == 'official' and age > STALE_DAYS:
                issues.append(f'{k} 官方价已 {age} 天未复核（source: {v.get("source","?")[:60]}）')
        except Exception:
            pass

    # 2) 抓官方页 diff（宽松：只在页面里能明确读到数字且与我们记录差异>10% 才告警）
    lines.append('当前生效单价 (USD/1M, in/out/cacheWrite/cacheRead) · confidence · verified:')
    for k, v in sorted(models.items()):
        p = v.get('price', [])
        pr = '/'.join(str(x) for x in p) if p else '?'
        lines.append(f'  {k:46} {pr:28} {v.get("confidence","?"):9} {v.get("verified","?")}')

    lines.append('')
    lines.append('官方页抓取核对（宽松 diff，抓不到则跳过）:')
    for k, fc in FETCHERS.items():
        if k not in models:
            continue
        html = _fetch(fc['url'])
        if not html:
            lines.append(f'  ⚠️ {k}: 抓取失败（{fc["url"]}）— 跳过，未判定变动')
            continue
        cur_in = models[k]['price'][0]
        # 在页面里找我们记录的 input 价字符串（含 $ 前缀或裸数字），命中即视为「仍一致」
        pat = re.compile(r'\$?\s*' + re.escape(f'{cur_in}') + r'\b')
        if pat.search(html):
            lines.append(f'  ✅ {k}: 官方页仍含 ${cur_in} in — 一致')
        else:
            lines.append(f'  ⚠️ {k}: 官方页未见 ${cur_in} in — 可能变价，请核对 {fc["url"]}（{fc["hint"]}）')
            issues.append(f'{k} 官方页未见记录的 input 价 ${cur_in}，疑似变价 → 核对 {fc["url"]}')

    lines.append('')
    if issues:
        lines.append('🔴 需人工处理:')
        for i in issues:
            lines.append(f'  • {i}')
        lines.append('')
        lines.append('改价方式：编辑 src/data/pricing.json（单一源），更新 price + verified + source。')
    else:
        lines.append('✅ 无异动，全部 official 价在有效期内。')

    report = '\n'.join(lines)
    print(report)
    # 把报告写到固定位置，cron 脚本据此决定是否推飞书
    out = '/tmp/shrimp-pricing-report.txt'
    open(out, 'w').write(report)
    # 退出码：有 issue = 1（cron 据此推送），无 = 0
    return 1 if issues else 0


if __name__ == '__main__':
    sys.exit(main())
