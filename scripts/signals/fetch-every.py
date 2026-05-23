#!/usr/bin/env python3
"""
Fetch Every (every.to) — premium AI thinking / writing subscription platform.

Every 没有公开 RSS,抓首页 HTML 提取最新文章列表(免费部分,付费墙内容不抓)。
适合作为「精读候选素材」+ AI 日报「深度观点」补充。

Output: /tmp/ai-signals/every.md
"""
import os
import sys
import time
import urllib.request
import urllib.error
import re
import html as html_lib

OUT_DIR = "/tmp/ai-signals"
OUT_PATH = os.path.join(OUT_DIR, "every.md")
HOME_URL = "https://every.to/"
NEWSLETTER_URL = "https://every.to/newsletter"
TIMEOUT = 15
MAX_BYTES = 1_500_000
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 ai-daily-signals/1.0"

# 抓 every.to 文章链接的正则:
# 实际页面格式 <a href="/<column-slug>/<article-slug>" ...>Title</a>
# column-slug 例如 chain-of-thought / cybernaut / napkin-math / divinations / source-code / latent-space ...
ARTICLE_LINK_RE = re.compile(
    r'<a[^>]+href="(/(?!login|search|newsletter|columnists|columns|podcast|studio|guides|consulting|events|about|careers|faq|team|advertise|p/|tag/|pricing|members|jobs)[a-z0-9][a-z0-9-]*/[a-z0-9][a-z0-9-]+)"[^>]*>(.*?)</a>',
    re.S | re.I,
)


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return resp.read(MAX_BYTES).decode("utf-8", errors="replace")


def extract_articles(html, base="https://every.to"):
    seen = set()
    articles = []
    for m in ARTICLE_LINK_RE.finditer(html):
        path = m.group(1)
        # 过滤明显是导航 / 标签 / 作者 profile 页面
        if path.count("/") < 2:
            continue
        url = base + path
        if url in seen:
            continue
        # 标题:剥 inner HTML
        title = html_lib.unescape(re.sub(r"<[^>]+>", " ", m.group(2))).strip()
        title = re.sub(r"\s+", " ", title)
        if not title or len(title) < 8 or len(title) > 250:
            continue
        # 过滤纯图片 alt 或一些导航文字
        if title.lower() in {"read more", "see more", "view all", "more"}:
            continue
        seen.add(url)
        # column 是 path 第一段
        column = path.strip("/").split("/")[0]
        articles.append({"title": title, "url": url, "column": column})
    return articles


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    started = time.time()
    all_articles = []
    errors = []

    for url in (HOME_URL, NEWSLETTER_URL):
        try:
            html = fetch(url)
            arts = extract_articles(html)
            all_articles.extend(arts)
            print(f"[fetch-every] {url} -> {len(arts)} articles", file=sys.stderr)
        except Exception as e:
            errors.append(f"{url}: {e}")
            print(f"[fetch-every] {url} FAILED: {e}", file=sys.stderr)

    # 去重(以 url)
    dedup = {}
    for a in all_articles:
        dedup.setdefault(a["url"], a)
    articles = list(dedup.values())[:30]  # 最多保留 30 条

    # 按 column 分组展示
    by_column = {}
    for a in articles:
        by_column.setdefault(a["column"], []).append(a)

    lines = [
        "# Every (every.to)",
        "",
        f"_Fetched {time.strftime('%Y-%m-%d %H:%M %Z')} · {len(articles)} articles_",
        "",
        "Every 是 AI 实践者深度写作平台 (column-based)。本采集器抓首页 + Newsletter 列表的免费可见文章。",
        "适合作为「精读候选素材」+ AI 日报「深度观点」补充。",
        "",
    ]
    if errors:
        lines.append("_Errors:_ " + " ; ".join(errors))
        lines.append("")

    # 知名 column 优先排序
    priority_cols = [
        "chain-of-thought",
        "napkin-math",
        "divinations",
        "cybernaut",
        "source-code",
        "latent-space",
        "p",
    ]
    sorted_cols = sorted(
        by_column.keys(),
        key=lambda c: (priority_cols.index(c) if c in priority_cols else 999, c),
    )

    for col in sorted_cols:
        items = by_column[col]
        if not items:
            continue
        lines.append(f"## {col}")
        lines.append("")
        for i, it in enumerate(items[:10], 1):
            lines.append(f"{i}. [{it['title']}]({it['url']})")
        lines.append("")

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    elapsed = time.time() - started
    print(
        f"[fetch-every] OK ({elapsed:.1f}s) {len(articles)} unique articles -> {OUT_PATH}"
    )


if __name__ == "__main__":
    main()
