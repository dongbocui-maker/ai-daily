#!/usr/bin/env python3
"""每周价格复核：对照当前内置单价表，提示是否需更新。
当前单价硬编码在 agents-dashboard-aggregate.py 的 PRICING dict。
本脚本输出一份对照报告，由 cron 每周一跑，价格异动时提醒钢铁虾人工核对后改 PRICING。
注：各家官网 HTML 结构多变，这里只做"基准价快照 + 人工复核提醒"，不做脆弱的自动解析改写。
"""
import json, datetime

# 当前生效单价（须与 agents-dashboard-aggregate.py 的 PRICING 保持一致）USD/1M (in,out,cacheWrite,cacheRead)
CURRENT = {
    'azure-claude-48/claude-opus-4-8':    (5.00, 25.00, 6.25, 0.50),
    'azure-claude/claude-opus-4-7':       (5.00, 25.00, 6.25, 0.50),
    'azure-openai-responses/gpt-5.5':     (1.25, 10.00, 1.25, 0.125),
    'deepseek/DeepSeek-V4-Pro':           (0.435, 0.87, 0.435, 0.003625),
}

# 官方价来源（人工复核时打开核对）
SOURCES = {
    'Anthropic (Opus)':  'https://www.anthropic.com/pricing  |  cache: write=1.25×in, read=0.1×in',
    'DeepSeek':          'https://api-docs.deepseek.com/quick_start/pricing',
    'Azure OpenAI (GPT)':'https://azure.microsoft.com/en-us/pricing/details/azure-openai/',
}

now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
print(f"=== S.H.R.I.M.P. 单价复核 · {now} ===\n")
print("当前生效单价 (USD / 1M tokens) — in / out / cacheWrite / cacheRead:")
for k,(i,o,cw,cr) in CURRENT.items():
    print(f"  {k:38} {i:>7} / {o:>7} / {cw:>7} / {cr:>9}")
print("\n官方源（请逐一打开核对，若有变动，改 scripts/agents-dashboard-aggregate.py 的 PRICING）:")
for name,url in SOURCES.items():
    print(f"  • {name}: {url}")
print("\n⚠️ 若 Accenture EA 有折扣价，Anthropic/Azure 实际账单更低 —— 当前按官网标价(保守上限)。")
print("提示：本脚本仅做复核提醒，不自动改价（官网 HTML 易变，自动解析不可靠）。")
