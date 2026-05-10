#!/usr/bin/env python3
"""
对子代理产出的全量稿做去重过滤。

输入：JSON 形式的当日候选条目 + /tmp/ai-signals/recent-published.json
输出：去重后的 JSON + 被去除条目清单 + 触发原因

子代理调用方式（通过 exec 工具）：
  python3 dedup-filter.py --input /tmp/today-draft.json --output /tmp/today-filtered.json

输入 JSON 格式：
  {
    "items": [
      {"section": "AI 热点新闻", "title": "...", "url": "...", "source": "...", "body": "..."},
      ...
    ]
  }

判定规则：
  规则 A（硬过滤）：URL 精确匹配最近 7 天 → 删除（只允许有"明确进展"的后续报道，但需要标题带【进展】或【后续】）
  规则 B（软过滤）：标题 normalize 后字符相似度 ≥ 0.85 → 删除
  规则 C（事件级）：keywords 与历史条目交集 ≥ 3 个 + 全部 keywords ≥ 2 共现 → 标注 "需 LLM 复核"，写到 needs_review

退出码：
  0 - 处理完成（无论是否有删除）
  1 - 输入文件错误
  2 - recent-published 不存在或损坏
"""

import argparse
import json
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

RECENT_PATH = Path("/tmp/ai-signals/recent-published.json")
TITLE_SIMILARITY_THRESHOLD = 0.85
KEYWORD_OVERLAP_THRESHOLD = 3


def normalize_title(title: str) -> str:
    s = re.sub(r"^[^\w\u4e00-\u9fff]+[^|]*\|\s*", "", title.strip())
    return s.strip()


def title_similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, normalize_title(a), normalize_title(b)).ratio()


def has_progress_marker(title: str) -> bool:
    """标题里是否明确标注了【进展】【后续】【更新】等字样。"""
    markers = ["【进展】", "【后续】", "【更新】", "【续】", "【深化】", "[进展]", "[后续]", "[更新]"]
    return any(m in title for m in markers)


def extract_keywords(title: str) -> list[str]:
    """复用 build-recent-published.py 的关键词提取逻辑。"""
    title = normalize_title(title)
    keywords = []
    orgs = [
        "Anthropic", "OpenAI", "Google", "Microsoft", "Meta", "Apple", "NVIDIA",
        "Amazon", "AWS", "Cloudflare", "Stripe", "DeepSeek", "Claude", "GPT", "Gemini",
        "SpaceX", "Tesla", "xAI", "Bain", "Blackstone", "Goldman", "SoftBank",
        "Hellman", "Friedman", "字节", "豆包", "阿里", "通义", "百度", "文心",
        "腾讯", "混元", "智谱", "GLM", "月之暗面", "MiniMax", "百川", "零一万物",
        "讯飞", "Manus", "Stanford", "MIT", "HAI", "Tinder", "Match", "Salesforce",
        "Match Group", "Telus", "Moody", "Simon Willison", "Karpathy",
        "陶哲轩", "信通院", "Gartner", "IDC", "麦肯锡", "Accenture", "埃森哲",
        "Deloitte", "PwC", "BCG", "Reuters", "Bloomberg", "FT", "TechCrunch",
        "The Verge", "WSJ", "Wired", "Cognition", "Devin", "Cursor", "Vercel",
        "Replit", "GitHub", "Hugging Face", "Mistral", "Cohere", "Perplexity",
        "Character", "Inflection", "Adept", "Magic", "Codex", "Copilot",
        "SWE-Bench", "Colossus",
    ]
    for org in orgs:
        if org.lower() in title.lower():
            keywords.append(org)
    money = re.findall(r"\d+(?:\.\d+)?\s*(?:亿|万亿|million|billion|M|B)\s*(?:美元|美刀|USD|元|RMB)?", title)
    keywords.extend(money)
    verb_patterns = [
        "收购", "合资", "投资", "融资", "发布", "推出", "停服", "起诉", "和解",
        "acquisition", "merger", "joint venture", "funding", "valuation",
        "launch", "release", "lawsuit", "settlement", "partnership",
    ]
    for v in verb_patterns:
        if v.lower() in title.lower():
            keywords.append(v)
    return keywords


def load_recent_published():
    if not RECENT_PATH.exists():
        return None
    try:
        return json.loads(RECENT_PATH.read_text())
    except Exception as e:
        print(f"[dedup] recent-published 损坏: {e}", file=sys.stderr)
        return None


def check_item(item: dict, recent: dict) -> dict | None:
    """
    检查一个候选条目是否需要删除。
    返回 None 表示保留；返回 dict 表示有删除/警告原因。
    """
    title = item.get("title", "")
    url = item.get("url", "")
    keywords = extract_keywords(title)

    # 规则 A：URL 精确匹配
    by_url = recent.get("by_url", {})
    if url and url in by_url:
        if has_progress_marker(title):
            return {"verdict": "warn", "rule": "A-url-with-progress",
                    "reason": f"URL 已发于 {by_url[url]['date']}，但标题带【进展】标识，允许保留",
                    "previous": by_url[url]}
        return {"verdict": "drop", "rule": "A-url-exact",
                "reason": f"URL 已发于 {by_url[url]['date']}",
                "previous": by_url[url]}

    # 规则 B：标题相似度
    best_match = None
    best_sim = 0.0
    for prev in recent.get("items", []):
        sim = title_similarity(title, prev.get("title", ""))
        if sim > best_sim:
            best_sim = sim
            best_match = prev
    if best_sim >= TITLE_SIMILARITY_THRESHOLD:
        if has_progress_marker(title):
            return {"verdict": "warn", "rule": "B-title-similar-with-progress",
                    "reason": f"标题与 {best_match['date']} 条目相似度 {best_sim:.2f}，但带【进展】标识",
                    "previous": best_match, "similarity": best_sim}
        return {"verdict": "drop", "rule": "B-title-similar",
                "reason": f"标题与 {best_match['date']} 条目相似度 {best_sim:.2f} ≥ {TITLE_SIMILARITY_THRESHOLD}",
                "previous": best_match, "similarity": best_sim}

    # 规则 C：关键词级事件聚类（标注但不直接删除，让 LLM 复核）
    suspect_matches = []
    for prev in recent.get("items", []):
        prev_keywords = set(prev.get("keywords", []))
        cur_keywords = set(keywords)
        overlap = prev_keywords & cur_keywords
        if len(overlap) >= KEYWORD_OVERLAP_THRESHOLD:
            suspect_matches.append({
                "date": prev["date"],
                "title": prev["title"],
                "section": prev["section"],
                "shared_keywords": sorted(overlap),
            })
    if suspect_matches:
        if has_progress_marker(title):
            return None  # 带进展标识 + 关键词重合 → 直接放行
        return {"verdict": "review", "rule": "C-keywords-overlap",
                "reason": f"关键词与历史条目重叠 ≥ {KEYWORD_OVERLAP_THRESHOLD} 个，疑似同事件",
                "suspects": suspect_matches}

    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="子代理产出的全量稿 JSON")
    parser.add_argument("--output", required=True, help="去重后输出路径")
    parser.add_argument("--report", help="去重报告输出路径（可选）")
    args = parser.parse_args()

    in_path = Path(args.input)
    out_path = Path(args.output)
    report_path = Path(args.report) if args.report else out_path.with_suffix(".dedup-report.json")

    if not in_path.exists():
        print(f"[dedup] 输入不存在: {in_path}", file=sys.stderr)
        return 1

    try:
        draft = json.loads(in_path.read_text())
    except Exception as e:
        print(f"[dedup] 输入 JSON 解析失败: {e}", file=sys.stderr)
        return 1

    recent = load_recent_published()
    if recent is None:
        print("[dedup] 无 recent-published.json，跳过去重（直接复制输入到输出）", file=sys.stderr)
        out_path.write_text(in_path.read_text())
        report_path.write_text(json.dumps({"skipped": True, "reason": "no recent-published"}, ensure_ascii=False, indent=2))
        return 2

    kept = []
    dropped = []
    needs_review = []
    warnings = []

    for item in draft.get("items", []):
        verdict = check_item(item, recent)
        if verdict is None:
            kept.append(item)
            continue
        v = verdict["verdict"]
        if v == "drop":
            dropped.append({"item": item, "verdict": verdict})
        elif v == "warn":
            kept.append(item)
            warnings.append({"item": item, "verdict": verdict})
        elif v == "review":
            kept.append(item)  # 默认保留，让 LLM 决定是否替换
            needs_review.append({"item": item, "verdict": verdict})

    output = {
        "items": kept,
        "stats": {
            "input_count": len(draft.get("items", [])),
            "kept": len(kept),
            "dropped": len(dropped),
            "warnings": len(warnings),
            "needs_review": len(needs_review),
        },
    }

    out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2))

    report = {
        "stats": output["stats"],
        "dropped": dropped,
        "warnings": warnings,
        "needs_review": needs_review,
    }
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2))

    print(f"[dedup] 输入 {output['stats']['input_count']} 条")
    print(f"[dedup] 保留 {output['stats']['kept']} / 删除 {output['stats']['dropped']} / 警告 {output['stats']['warnings']} / 待复核 {output['stats']['needs_review']}")
    print(f"[dedup] 输出: {out_path}")
    print(f"[dedup] 报告: {report_path}")

    if dropped:
        print("\n[dedup] 删除的条目:")
        for d in dropped:
            print(f"  - 【{d['item'].get('section', '')}】{d['item'].get('title', '')[:80]}")
            print(f"    {d['verdict']['reason']}")

    if needs_review:
        print("\n[dedup] 待 LLM 复核（疑似同事件）:")
        for r in needs_review:
            print(f"  - 【{r['item'].get('section', '')}】{r['item'].get('title', '')[:80]}")
            print(f"    与历史 {len(r['verdict']['suspects'])} 条疑似重合，关键词: {r['verdict']['suspects'][0]['shared_keywords']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
