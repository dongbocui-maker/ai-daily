#!/usr/bin/env python3
"""
Fetch Chinese editorial headlines: 量子位 + 36氪 AI 频道.
Captures editor-curated AI stories from leading Chinese AI media.

Output: /tmp/ai-signals/editorial-cn.md
"""
import os
import sys
import time
import urllib.request
import re

OUT_DIR = "/tmp/ai-signals"
OUT_PATH = os.path.join(OUT_DIR, "editorial-cn.md")
TIMEOUT = 12
MAX_BYTES = 1_500_000

SOURCES = [
    {
        "name": "量子位 (qbitai)",
        "url": "https://www.qbitai.com/",
        # qbitai uses h4>a structure for article titles
        "title_re": r'<h4[^>]*>\s*<a[^>]+href="(?P<url>https?://[^"]+)"[^>]*>(?P<title>[^<]{6,150})</a>',
    },
    {
        "name": "36氪 AI 频道",
        "url": "https://36kr.com/information/AI/",
        # 36kr uses .article-item-title
        "title_re": r'<a[^>]+class="article-item-title[^"]*"[^>]+href="(?P<url>[^"]+)"[^>]*>(?P<title>[^<]{6,200})</a>',
        "base": "https://36kr.com",
    },
    # 机器之心首页是 SPA 框架渲染（HTML 仅 3KB），抓不到内容；
    # 子代理可在写稿时用 web_search "site:jiqizhixin.com" 间接获取深度内容。
]


def fetch(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (compatible; ai-daily-signals/1.0)",
        "Accept": "text/html,*/*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.5",
    })
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return resp.read(MAX_BYTES).decode("utf-8", errors="replace")


def extract_headlines(html, source):
    items = []
    seen = set()
    for m in re.finditer(source["title_re"], html, flags=re.S | re.I):
        url = m.group("url")
        title = re.sub(r"\s+", " ", m.group("title")).strip()
        if not title or title in seen:
            continue
        if not url.startswith("http") and "base" in source:
            url = source["base"] + url
        seen.add(title)
        items.append({"title": title, "url": url})
        if len(items) >= 15:
            break
    return items


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    out_lines = [
        "# 中文编辑头条 (AI)",
        f"_Fetched {time.strftime('%Y-%m-%d %H:%M %Z')}_",
        "",
    ]
    for src in SOURCES:
        out_lines.append(f"## {src['name']}")
        out_lines.append(f"_Source: {src['url']}_")
        out_lines.append("")
        try:
            html = fetch(src["url"])
            items = extract_headlines(html, src)
            if not items:
                out_lines.append("_(解析返回 0 条 — selector 可能需要更新)_")
            for i, it in enumerate(items[:10], 1):
                out_lines.append(f"{i}. [{it['title']}]({it['url']})")
        except Exception as e:
            out_lines.append(f"_(抓取失败: {e})_")
        out_lines.append("")

    with open(OUT_PATH, "w") as f:
        f.write("\n".join(out_lines))

    print(f"[editorial-cn] wrote {OUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
