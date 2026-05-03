#!/usr/bin/env python3
"""parse-lmarena.py — 从 lmarena HTML 提取 RSC payload，生成 snapshot

用法：python3 parse-lmarena.py <input-html> <output-json> <snapshot-date>

输入：lmarena.ai/leaderboard 的 HTML（含 inline RSC payload）
输出：snapshot JSON（含 Top 50 模型 + 27 维度 + 优势赛道 + 简述）
"""
import sys
import re
import json
from pathlib import Path

# ============== 配置 ==============
CATEGORY_LABELS = {
    'overall': '综合', 'exclude-ties': '排除平局',
    'hard-prompts': '难题', 'hard-prompts-english': '英文难题',
    'longer-query': '长查询', 'multi-turn': '多轮对话',
    'multi-turn-context': '多轮上下文', 'instruction-following': '指令遵循',
    'creative-writing': '创意写作', 'expert': '专家级',
    'coding': '代码', 'math': '数学',
    'english': '英文', 'non-english': '非英文', 'chinese': '中文',
    'korean': '韩文', 'japanese': '日文', 'french': '法文',
    'german': '德文', 'spanish': '西文', 'russian': '俄文', 'polish': '波兰文',
    'industry-life-and-physical-and-social-science': '科学行业',
    'industry-software-and-it-services': '软件IT行业',
    'industry-writing-and-literature-and-language': '文学写作行业',
    'industry-medicine-and-healthcare': '医疗行业',
    'industry-business-and-management-and-financial-operations': '商业金融行业',
    'industry-mathematical': '数学行业',
    'industry-legal-and-government': '法律政府行业',
    'industry-entertainment-and-sports-and-media': '娱乐媒体行业',
}

CATEGORY_PRIORITY = {
    'hard-prompts': 0, 'coding': 0, 'math': 0, 'creative-writing': 0,
    'instruction-following': 0, 'multi-turn': 0, 'multi-turn-context': 0,
    'expert': 0, 'longer-query': 0, 'hard-prompts-english': 0,
    'english': 1, 'non-english': 1, 'chinese': 1,
    'industry-software-and-it-services': 2,
    'industry-medicine-and-healthcare': 2,
    'industry-business-and-management-and-financial-operations': 2,
    'industry-legal-and-government': 2,
    'industry-mathematical': 2,
    'industry-life-and-physical-and-social-science': 2,
    'industry-writing-and-literature-and-language': 2,
    'industry-entertainment-and-sports-and-media': 2,
    'korean': 3, 'japanese': 3, 'french': 3, 'german': 3,
    'spanish': 3, 'russian': 3, 'polish': 3,
}

NON_HIGHLIGHT = ['overall', 'exclude-ties']
TOP_N = 50


def extract_models(html_text):
    """从 HTML 中提取所有模型对象"""
    pattern = re.compile(r'\{\\"name\\":\\"([^\\"]+)\\",\\"organization\\":\\"([^\\"]+)\\"([^{}]+?)\}')
    seen = set()
    models = []
    for name, org, rest in pattern.findall(html_text):
        if name in seen:
            continue
        seen.add(name)
        m = {'name': name, 'organization': org}
        for k, v in re.findall(r'\\"([a-z-]+)\\":(\d+)', rest):
            m[k] = int(v)
        if 'overall' in m:
            models.append(m)
    return models


def gen_highlight(model):
    """A+B 混合：Top 10 优先 + 自身亮点补足；核心维度优先于行业/小语种"""
    items = []
    for cat, rank in model.items():
        if cat in ('name', 'organization'):
            continue
        if cat in NON_HIGHLIGHT:
            continue
        if not isinstance(rank, int):
            continue
        priority = CATEGORY_PRIORITY.get(cat, 9)
        items.append((cat, rank, priority))
    items.sort(key=lambda x: (x[2], x[1]))

    top10 = [(c, r) for c, r, _ in items if r <= 10]
    others = [(c, r) for c, r, _ in items if r > 10]

    highlight = []
    for cat, rank in top10[:3]:
        highlight.append({
            'category': cat,
            'label': CATEGORY_LABELS.get(cat, cat),
            'rank': rank,
            'isTop10': True,
        })
    if len(highlight) < 3:
        for cat, rank in others[:(3 - len(highlight))]:
            highlight.append({
                'category': cat,
                'label': CATEGORY_LABELS.get(cat, cat),
                'rank': rank,
                'isTop10': False,
            })
    return highlight


def gen_summary(highlight, overall_rank):
    """根据 highlight 生成中文简述"""
    if not highlight:
        return f'综合 #{overall_rank}'
    top10_items = [h for h in highlight if h['isTop10']]
    other_items = [h for h in highlight if not h['isTop10']]
    parts = []
    if top10_items:
        parts.append(' · '.join(f'{h["label"]} #{h["rank"]}' for h in top10_items))
    if other_items:
        parts.append('相对擅长 ' + ' · '.join(f'{h["label"]} #{h["rank"]}' for h in other_items))
    return ' | '.join(parts)


def build_snapshot(models, snapshot_date, is_baseline=False):
    """构建 snapshot 结构"""
    models_sorted = sorted(models, key=lambda x: x.get('overall', 9999))
    top = models_sorted[:TOP_N]

    out_models = []
    for m in top:
        scores = {k: v for k, v in m.items()
                  if k not in ('name', 'organization') and isinstance(v, int)}
        record = {'name': m['name'], 'organization': m['organization']}
        record.update(scores)
        highlight = gen_highlight(record)
        out_models.append({
            'rank': m['overall'],
            'name': m['name'],
            'org': m['organization'],
            'scores': scores,
            'highlight': highlight,
            'summary': gen_summary(highlight, m['overall']),
        })

    return {
        'snapshotDate': snapshot_date,
        'isBaseline': is_baseline,
        'totalModelsObserved': len(models),
        'totalModelsShown': len(out_models),
        'categoryLabels': CATEGORY_LABELS,
        'sourceUrl': 'https://lmarena.ai/leaderboard',
        'models': out_models,
    }


def main():
    if len(sys.argv) != 4:
        print('Usage: parse-lmarena.py <input-html> <output-json> <snapshot-date>',
              file=sys.stderr)
        sys.exit(1)

    input_html = sys.argv[1]
    output_json = sys.argv[2]
    snapshot_date = sys.argv[3]

    text = Path(input_html).read_text(encoding='utf-8')
    models = extract_models(text)
    if len(models) < 100:
        print(f'❌ 解析出的模型数过少（{len(models)}），可能页面结构变化',
              file=sys.stderr)
        sys.exit(2)

    # 检查是否是首次（没有上月 snapshot）
    snapshots_dir = Path(output_json).parent
    existing = sorted(f for f in snapshots_dir.glob('*.json') if f.stem != snapshot_date)
    is_baseline = len(existing) == 0

    snapshot = build_snapshot(models, snapshot_date, is_baseline=is_baseline)
    Path(output_json).write_text(
        json.dumps(snapshot, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'✅ {output_json} ({snapshot["totalModelsShown"]} models, baseline={is_baseline})')


if __name__ == '__main__':
    main()
