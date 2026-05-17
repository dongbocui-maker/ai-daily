#!/usr/bin/env python3
"""
AI 日报 daily JSON schema 校验脚本

校验规则（基于 MEMORY.md 「AI 日报站点根因修复必须考虑长期可扩展性」铁律）：
1. 顶层字段：date / title / sections / closing（audit 可选）
2. sections 数量 ≤ 4，每个 section.items ≥ 3 条
3. 每个 item 必须有 5 字段：title / body / insight / source / url
4. body ≥ 100 字
5. closing 必须是 3-10 段的字符串数组，每段 ≥ 50 字（防止 5/18 那种 678 单字符 bug）
6. title 必须存在且非空

用法：
    python3 scripts/validate-daily-schema.py                    # 校验最新日期
    python3 scripts/validate-daily-schema.py 2026-05-18         # 校验指定日期
    python3 scripts/validate-daily-schema.py --all              # 校验所有
"""
import json
import sys
import os
from glob import glob
from datetime import datetime

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DAILY_DIR = os.path.join(REPO_ROOT, 'src', 'data', 'daily')


def validate(filepath):
    """返回 (is_valid, problems)"""
    problems = []
    try:
        d = json.load(open(filepath))
    except Exception as e:
        return False, [f'JSON 解析失败: {e}']

    # 1. 顶层字段
    required_top = ['date', 'title', 'sections', 'closing']
    for f in required_top:
        if f not in d:
            problems.append(f'缺顶层字段: {f}')

    # 2. title 非空
    if not d.get('title') or not d['title'].strip():
        problems.append(f'title 字段为空: {d.get("title")!r}')

    # 3. sections 数量
    sections = d.get('sections', [])
    if not isinstance(sections, list):
        problems.append(f'sections 不是数组')
    elif len(sections) > 4:
        problems.append(f'sections 数量 {len(sections)} > 4（疑似重复污染）')
    elif len(sections) < 3:
        problems.append(f'sections 数量 {len(sections)} < 3（板块不全）')

    # 4. 每个 section 内部
    for i, s in enumerate(sections):
        if 'key' not in s:
            problems.append(f'sections[{i}] 缺 key')
        if 'items' not in s or not isinstance(s['items'], list):
            problems.append(f'sections[{i}] 缺 items 或不是数组')
            continue
        if len(s['items']) < 3:
            problems.append(f'sections[{i}].{s.get("key","?")} items 仅 {len(s["items"])} 条 < 3')
        # 5. 每个 item
        for j, it in enumerate(s['items']):
            for k in ['title', 'body', 'insight', 'source', 'url']:
                if k not in it or not it[k]:
                    problems.append(f'sections[{i}].{s.get("key","?")} items[{j}] 缺: {k}')
            if 'body' in it and isinstance(it['body'], str) and len(it['body']) < 100:
                problems.append(f'sections[{i}].{s.get("key","?")} items[{j}] body 仅 {len(it["body"])} 字 < 100')

    # 6. closing 段数与字数
    closing = d.get('closing', [])
    if not isinstance(closing, list):
        problems.append(f'closing 不是数组')
    elif len(closing) > 10:
        problems.append(f'closing 段数 {len(closing)} > 10（疑似单字符序列化污染——参考 5/18 事故）')
    elif len(closing) < 3:
        problems.append(f'closing 段数 {len(closing)} < 3（总结不全）')
    else:
        for i, c in enumerate(closing):
            if not isinstance(c, str):
                problems.append(f'closing[{i}] 不是字符串')
            elif len(c) < 50:
                problems.append(f'closing[{i}] 仅 {len(c)} 字 < 50（疑似异常拆分）')

    return len(problems) == 0, problems


def main():
    args = sys.argv[1:]
    if '--all' in args:
        files = sorted(glob(os.path.join(DAILY_DIR, '*.json')))
    elif args and not args[0].startswith('--'):
        files = [os.path.join(DAILY_DIR, args[0] + '.json')]
    else:
        # 默认最新一份
        files = sorted(glob(os.path.join(DAILY_DIR, '*.json')))
        files = files[-1:] if files else []

    if not files:
        print('未找到 daily JSON 文件', file=sys.stderr)
        sys.exit(1)

    total = 0
    failed = 0
    for f in files:
        total += 1
        name = os.path.basename(f).replace('.json', '')
        ok, problems = validate(f)
        if ok:
            print(f'✅ {name}: PASS')
        else:
            failed += 1
            print(f'❌ {name}: FAIL ({len(problems)} 个问题)')
            for p in problems:
                print(f'    - {p}')

    print()
    print(f'总计 {total} 份，PASS {total - failed} 份，FAIL {failed} 份')
    sys.exit(0 if failed == 0 else 1)


if __name__ == '__main__':
    main()
