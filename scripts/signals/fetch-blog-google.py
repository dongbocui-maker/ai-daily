#!/usr/bin/env python3
"""
Fetch Google's official AI blog (blog.google) RSS feed.

Google 自家的 AI 产品 / 模型 / 研究公告，权威性最高的官方一手信号。
每日 1-3 篇，跟 AI 日报节奏完全对齐。

Output: /tmp/ai-signals/blog-google.md
"""
import os
import sys
import time
import urllib.request
import re
import html as html_lib

OUT_DIR = "/tmp/ai-signals"
OUT_PATH = os.path.join(OUT_DIR, "blog-google.md")
# blog.google 根 RSS 已经包含全公司公告 (AI / Gemini / DeepMind / Workspace 等),
# /technology/ai/rss/ 301 跳到 /innovation-and-ai/technology/ai/rss/, 用根 feed 更稳。
URL = "https://blog.google/rss/"
PROXY = "http://127.0.0.1:7890"  # mihomo, 直连国内偶尔 SSL handshake 超时
TIMEOUT = 20
MAX_BYTES = 1_500_000
# 只保留 AI 相关条目(标题或 category 包含这些关键词)
AI_KEYWORDS = re.compile(
    r"\b(AI|artificial intelligence|Gemini|DeepMind|Bard|Vertex|Imagen|Veo|"
    r"NotebookLM|TPU|model|machine learning|LLM|chatbot|generative|agent|copilot|"
    r"AlphaFold|AlphaGo|Pixel.*AI|Search.*Generative|SGE)\b",
    re.I,
)


def fetch(url, use_proxy=False):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "ai-daily-signals/1.0 (+ai-daily.openclaw.ai)"},
    )
    if use_proxy:
        handler = urllib.request.ProxyHandler({"http": PROXY, "https": PROXY})
        opener = urllib.request.build_opener(handler)
        with opener.open(req, timeout=TIMEOUT) as resp:
            return resp.read(MAX_BYTES).decode("utf-8", errors="replace")
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return resp.read(MAX_BYTES).decode("utf-8", errors="replace")


def parse_rss(xml):
    """Parse Atom/RSS items. Return list of dicts {title, link, pub, summary, categories}."""
    items = []
    # blog.google 用的是 Atom XML
    entries = re.findall(r"<entry\b[^>]*>(.*?)</entry>", xml, flags=re.S | re.I)
    if not entries:
        # 回退 RSS 2.0
        entries = re.findall(r"<item\b[^>]*>(.*?)</item>", xml, flags=re.S | re.I)
    for ent in entries:
        def grab(tag, body=ent):
            m = re.search(
                rf"<{tag}\b[^>]*>(.*?)</{tag}>", body, flags=re.S | re.I
            )
            return m.group(1).strip() if m else ""

        title = grab("title")
        link = ""
        # Atom: <link href="..."/>
        ml = re.search(r'<link\b[^>]*href="([^"]+)"', ent, flags=re.I)
        if ml:
            link = ml.group(1)
        else:
            link = grab("link")
        pub = grab("published") or grab("pubDate") or grab("updated")
        summary = grab("summary") or grab("description") or grab("content")
        cats = re.findall(r'<category\b[^>]*term="([^"]+)"', ent, flags=re.I) or \
               re.findall(r"<category\b[^>]*>(.*?)</category>", ent, flags=re.S | re.I)
        # 清理
        title = html_lib.unescape(re.sub(r"<[^>]+>", " ", title)).strip()
        summary = html_lib.unescape(re.sub(r"<[^>]+>", " ", summary)).strip()
        summary = re.sub(r"\s+", " ", summary)[:400]
        items.append(
            {
                "title": title,
                "link": link,
                "pub": pub,
                "summary": summary,
                "categories": cats,
            }
        )
    return items


def is_ai_related(item):
    haystack = (
        item["title"] + " " + item["summary"] + " " + " ".join(item.get("categories") or [])
    )
    return bool(AI_KEYWORDS.search(haystack))


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    started = time.time()
    xml = None
    last_err = None
    # 优先走 mihomo 代理(直连国内本机到 blog.google 频繁 SSL handshake 超时),
    # 失败回退直连。
    for use_proxy in (True, False):
        try:
            xml = fetch(URL, use_proxy=use_proxy)
            via = "mihomo proxy" if use_proxy else "direct"
            print(f"[fetch-blog-google] fetched via {via}", file=sys.stderr)
            break
        except Exception as e:
            last_err = e
            print(
                f"[fetch-blog-google] attempt (proxy={use_proxy}) failed: {e}",
                file=sys.stderr,
            )
            continue
    if xml is None:
        with open(OUT_PATH, "w", encoding="utf-8") as f:
            f.write(f"# blog.google\n\n_Fetch failed (direct + mihomo): {last_err}_\n")
        sys.exit(0)

    items = parse_rss(xml)
    ai_items = [it for it in items if is_ai_related(it)]
    # 最多保留 20 条最新
    ai_items = ai_items[:20]

    lines = [
        "# Google Blog — AI (blog.google)",
        "",
        f"_Source: {URL} · Fetched {time.strftime('%Y-%m-%d %H:%M %Z')} · "
        f"{len(ai_items)}/{len(items)} AI-related items_",
        "",
        "Google 官方一手 AI 新闻(Gemini / DeepMind / Workspace AI / Pixel AI / Search SGE 等)。",
        "",
        "## Recent AI Posts",
        "",
    ]
    for i, it in enumerate(ai_items, 1):
        title = it["title"] or "(untitled)"
        link = it["link"] or ""
        pub = it["pub"]
        summary = it["summary"]
        lines.append(f"{i}. [{title}]({link})")
        if pub:
            lines.append(f"   - _published: {pub}_")
        if summary:
            lines.append(f"   - {summary}")
        lines.append("")

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    elapsed = time.time() - started
    print(
        f"[fetch-blog-google] OK ({elapsed:.1f}s) "
        f"{len(ai_items)}/{len(items)} items -> {OUT_PATH}"
    )


if __name__ == "__main__":
    main()
