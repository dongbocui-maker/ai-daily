#!/usr/bin/env python3
"""
读取 src/data/daily/ 最近 7 天的 JSON，提取已发布条目的标题、URL、事件指纹，
输出 /tmp/ai-signals/recent-published.json，给子代理选题前去重用。

用法：在 run-all.sh 里调用。失败不阻塞（输出空文件占位）。
"""

import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

REPO_ROOT = Path("/root/.openclaw/workspace/projects/ai-daily")
DAILY_DIR = REPO_ROOT / "src" / "data" / "daily"
OUT_PATH = Path("/tmp/ai-signals/recent-published.json")

# 看过去 7 天（不含今天，因为今天还没发）
WINDOW_DAYS = 7


def normalize_title(title: str) -> str:
    """
    去掉前导 emoji + 类型标签（如 "🤝 收并购 | "），只保留主标题文字。
    """
    # 去前导 emoji 和类型标签：匹配 "<emoji> <type> | " 这种模式
    s = re.sub(r"^[^\w\u4e00-\u9fff]+[^|]*\|\s*", "", title.strip())
    return s.strip()


def extract_event_keywords(title: str) -> list[str]:
    """
    从标题里抽出关键事件词：公司/组织名 + 数字 + 关键动词词组。
    用于事件级聚类（同事件不同标题写法）。
    """
    title = normalize_title(title)
    keywords = []

    # 1. 公司/组织名（白名单）
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

    # 2. 大数字（带亿/billion/million 等单位）
    money = re.findall(r"\d+(?:\.\d+)?\s*(?:亿|万亿|million|billion|M|B)\s*(?:美元|美刀|USD|元|RMB)?", title)
    keywords.extend(money)

    # 3. 关键事件动词（中英）
    verb_patterns = [
        "收购", "合资", "投资", "融资", "发布", "推出", "停服", "起诉", "和解",
        "acquisition", "merger", "joint venture", "funding", "valuation",
        "launch", "release", "lawsuit", "settlement", "partnership",
    ]
    for v in verb_patterns:
        if v.lower() in title.lower():
            keywords.append(v)

    return keywords


def main():
    if not DAILY_DIR.exists():
        print(f"[recent-published] DAILY_DIR 不存在: {DAILY_DIR}", file=sys.stderr)
        OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        OUT_PATH.write_text(json.dumps({"items": [], "by_url": {}, "error": "no daily dir"}, ensure_ascii=False, indent=2))
        return 0

    today = date.today()
    items = []  # 每条：{date, section, title, normalized_title, url, source, keywords}
    by_url = {}  # url -> {date, title, section}

    for delta in range(1, WINDOW_DAYS + 1):
        d = today - timedelta(days=delta)
        path = DAILY_DIR / f"{d.isoformat()}.json"
        if not path.exists():
            continue
        try:
            data = json.loads(path.read_text())
        except Exception as e:
            print(f"[recent-published] 跳过 {path.name}: {e}", file=sys.stderr)
            continue

        for sec in data.get("sections", []):
            label = sec.get("label", "")
            for it in sec.get("items", []):
                title = it.get("title", "")
                url = it.get("url", "")
                source = it.get("source", "")
                normalized = normalize_title(title)
                keywords = extract_event_keywords(title)

                entry = {
                    "date": d.isoformat(),
                    "section": label,
                    "title": title,
                    "normalized_title": normalized,
                    "url": url,
                    "source": source,
                    "keywords": keywords,
                }
                items.append(entry)
                if url:
                    by_url[url] = {
                        "date": d.isoformat(),
                        "title": title,
                        "section": label,
                    }

    output = {
        "generated_at": today.isoformat(),
        "window_days": WINDOW_DAYS,
        "total_items": len(items),
        "total_unique_urls": len(by_url),
        "items": items,
        "by_url": by_url,
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(output, ensure_ascii=False, indent=2))

    # 同时输出一个轻量版给 LLM 直接读：只保留 title + url + date
    light_path = OUT_PATH.parent / "recent-published-light.txt"
    lines = ["# 过去 7 天已发布条目（去重黑名单）", ""]
    lines.append(f"共 {len(items)} 条 / {len(by_url)} 个唯一 URL\n")
    by_date: dict[str, list] = {}
    for it in items:
        by_date.setdefault(it["date"], []).append(it)
    for d in sorted(by_date.keys(), reverse=True):
        lines.append(f"\n## {d}")
        for it in by_date[d]:
            url_part = f"  ({it['url']})" if it.get("url") else ""
            lines.append(f"- 【{it['section']}】{it['title']}{url_part}")
    light_path.write_text("\n".join(lines))

    print(f"[recent-published] OK: {len(items)} items / {len(by_url)} URLs / window {WINDOW_DAYS}d")
    print(f"[recent-published] wrote {OUT_PATH}")
    print(f"[recent-published] wrote {light_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
