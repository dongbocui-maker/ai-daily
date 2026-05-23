#!/usr/bin/env python3
"""
Fetch The AI Valley (theaivalley.com).

直连 403 (Cloudflare anti-bot),走 mihomo 代理 (127.0.0.1:7890) 才能拿到 200。
站点没有公开 RSS (302 跳到 404 页),只能抓首页 HTML。

Output: /tmp/ai-signals/theaivalley.md
"""
import os
import sys
import time
import urllib.request
import re
import html as html_lib

OUT_DIR = "/tmp/ai-signals"
OUT_PATH = os.path.join(OUT_DIR, "theaivalley.md")
HOME_URL = "https://www.theaivalley.com/"
PROXY = "http://127.0.0.1:7890"
TIMEOUT = 20
MAX_BYTES = 2_000_000
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"


def fetch_via_proxy(url, proxy=PROXY):
    # 用 urllib + ProxyHandler 走 mihomo
    handler = urllib.request.ProxyHandler({"http": proxy, "https": proxy})
    opener = urllib.request.build_opener(handler)
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": UA,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        },
    )
    with opener.open(req, timeout=TIMEOUT) as resp:
        return resp.read(MAX_BYTES).decode("utf-8", errors="replace")


def extract_articles(html, base="https://www.theaivalley.com"):
    """The AI Valley 文章 URL 通常形如 /p/<slug> 或 /<slug> 这种 newsletter 风格。
    我们抓所有 <a href> 看哪些像文章。"""
    candidates = re.findall(
        r'<a[^>]+href="(/p/[a-z0-9][a-z0-9-]+|https://www\.theaivalley\.com/p/[a-z0-9][a-z0-9-]+)"[^>]*>(.*?)</a>',
        html,
        flags=re.S | re.I,
    )
    seen = set()
    articles = []
    for url, raw_title in candidates:
        if url.startswith("/"):
            url = base + url
        if url in seen:
            continue
        title = html_lib.unescape(re.sub(r"<[^>]+>", " ", raw_title)).strip()
        title = re.sub(r"\s+", " ", title)
        if not title or len(title) < 8 or len(title) > 300:
            continue
        if title.lower() in {"read more", "subscribe", "sign up", "view all", "share"}:
            continue
        seen.add(url)
        articles.append({"title": title, "url": url})
    return articles


def extract_text_snippet(html, max_chars=3000):
    """剥 HTML 标签拿正文文本片段,给子代理评估时参考。"""
    # 删 script/style
    html = re.sub(r"<script.*?</script>", "", html, flags=re.S | re.I)
    html = re.sub(r"<style.*?</style>", "", html, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", html)
    text = html_lib.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:max_chars]


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    started = time.time()
    try:
        html = fetch_via_proxy(HOME_URL)
    except Exception as e:
        with open(OUT_PATH, "w", encoding="utf-8") as f:
            f.write(
                f"# The AI Valley\n\n_Fetch failed (via mihomo {PROXY}): {e}_\n"
            )
        print(f"[fetch-theaivalley] FAILED: {e}", file=sys.stderr)
        sys.exit(0)

    articles = extract_articles(html)[:25]
    snippet = extract_text_snippet(html, max_chars=3000)

    lines = [
        "# The AI Valley (theaivalley.com)",
        "",
        f"_Fetched {time.strftime('%Y-%m-%d %H:%M %Z')} via mihomo proxy · "
        f"{len(articles)} articles found_",
        "",
        "AI 行业 newsletter 风格聚合站。直连服务器走 Cloudflare 反爬,所以走 mihomo。",
        "",
    ]
    if articles:
        lines.append("## Articles on Home Page")
        lines.append("")
        for i, a in enumerate(articles, 1):
            lines.append(f"{i}. [{a['title']}]({a['url']})")
        lines.append("")
    else:
        lines.append("## Articles")
        lines.append("")
        lines.append("_(未能从首页提取到 /p/ 链接,可能页面结构变化或主要内容靠 JavaScript 加载)_")
        lines.append("")

    lines.append("## Home Page Text Snippet (first ~3000 chars)")
    lines.append("")
    lines.append("```")
    lines.append(snippet)
    lines.append("```")
    lines.append("")

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    elapsed = time.time() - started
    print(
        f"[fetch-theaivalley] OK ({elapsed:.1f}s) {len(articles)} articles -> {OUT_PATH}"
    )


if __name__ == "__main__":
    main()
