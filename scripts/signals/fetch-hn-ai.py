#!/usr/bin/env python3
"""
Fetch top AI-related stories from Hacker News via official API.

Output: /tmp/ai-signals/hn-ai.json — list of stories with url/title/score/comments
Filter: AI keywords + score >= 100, top 30 by score.

Idempotent. Fail-safe: writes empty list on error.
"""
import json
import os
import sys
import time
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

OUT_DIR = "/tmp/ai-signals"
OUT_PATH = os.path.join(OUT_DIR, "hn-ai.json")
TOP_API = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_API = "https://hacker-news.firebaseio.com/v0/item/{}.json"
MAX_FETCH = 200          # 取前 200 个 topstories
MIN_SCORE = 80
MAX_OUTPUT = 30
TIMEOUT = 5              # 单请求超时秒
TOTAL_BUDGET = 50        # 总耗时预算秒

AI_KEYWORDS = [
    "ai", "llm", "gpt", "claude", "anthropic", "openai", "deepmind",
    "gemini", "agent", "rag", "model", "transformer", "diffusion",
    "machine learning", "neural", "deep learning", "fine-tun", "embedding",
    "lora", "vector", "rl", "reinforcement", "训练", "推理",
    "deepseek", "qwen", "llama", "mistral", "mixtral", "grok",
    "copilot", "cursor", "codex", "cody",
]


def is_ai_related(item):
    if not item or item.get("type") != "story":
        return False
    text = (item.get("title", "") + " " + item.get("url", "")).lower()
    return any(kw in text for kw in AI_KEYWORDS)


def fetch_json(url, timeout=TIMEOUT):
    req = urllib.request.Request(url, headers={"User-Agent": "ai-daily-signals/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_item(item_id):
    try:
        return fetch_json(ITEM_API.format(item_id))
    except Exception:
        return None


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    started = time.time()

    try:
        top_ids = fetch_json(TOP_API, timeout=10)
    except Exception as e:
        print(f"[hn] failed to fetch topstories: {e}", file=sys.stderr)
        with open(OUT_PATH, "w") as f:
            json.dump({"fetched_at": int(time.time()), "items": [], "error": str(e)}, f)
        return 1

    candidate_ids = top_ids[:MAX_FETCH]

    # 并发拉每条 item，预算内拉多少算多少
    items = []
    with ThreadPoolExecutor(max_workers=20) as ex:
        futures = {ex.submit(fetch_item, i): i for i in candidate_ids}
        for fut in as_completed(futures):
            if time.time() - started > TOTAL_BUDGET:
                break
            try:
                item = fut.result(timeout=2)
            except Exception:
                continue
            if item:
                items.append(item)

    # 过滤 AI 相关 + 分数门槛
    ai_items = [
        {
            "id": it.get("id"),
            "title": it.get("title", ""),
            "url": it.get("url") or f"https://news.ycombinator.com/item?id={it.get('id')}",
            "hn_url": f"https://news.ycombinator.com/item?id={it.get('id')}",
            "score": it.get("score", 0),
            "comments": it.get("descendants", 0),
            "by": it.get("by"),
            "time": it.get("time"),
        }
        for it in items
        if is_ai_related(it) and it.get("score", 0) >= MIN_SCORE
    ]

    ai_items.sort(key=lambda x: x["score"], reverse=True)
    ai_items = ai_items[:MAX_OUTPUT]

    out = {
        "fetched_at": int(time.time()),
        "fetched_at_iso": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "source": "Hacker News",
        "filter": f"AI keywords + score >= {MIN_SCORE}",
        "items": ai_items,
        "count": len(ai_items),
    }
    with open(OUT_PATH, "w") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print(f"[hn] wrote {len(ai_items)} items to {OUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
