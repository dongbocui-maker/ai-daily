#!/usr/bin/env python3
"""
Fetch English editorial headlines: Reuters AI + The Information AI Agenda.
Outputs markdown digest of headlines (titles + URLs) — what their editors are
choosing as the top AI stories.

Output: /tmp/ai-signals/editorial-en.md
"""
import os
import sys
import time
import urllib.request
import re

OUT_DIR = "/tmp/ai-signals"
OUT_PATH = os.path.join(OUT_DIR, "editorial-en.md")
TIMEOUT = 12
MAX_BYTES = 1_500_000

# Note: Reuters & The Information are blocked from this server
# (network unreachable / 403 anti-bot). Subagent must fall back to web_search
# with site: filter for those during the writing step.
#
# We use HTML for TechCrunch (works reliably) and RSS for The Verge / Ars
# Technica (avoids anti-bot, much more stable than scraping HTML).
SOURCES = [
    {
        "name": "TechCrunch AI",
        "url": "https://techcrunch.com/category/artificial-intelligence/",
        "format": "html",
        "title_re": r'<a[^>]+href="(?P<url>https://techcrunch\.com/\d{4}/\d{2}/\d{2}/[^"#]+)"[^>]*>\s*(?P<title>[^<]{10,250})\s*</a>',
    },
    {
        "name": "The Verge AI",
        "url": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
        "format": "atom",  # Atom feed
    },
    {
        "name": "Ars Technica AI",
        "url": "https://arstechnica.com/ai/feed/",
        "format": "rss",  # RSS 2.0
    },
]


def fetch(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (compatible; ai-daily-signals/1.0)",
        "Accept": "text/html,*/*",
        "Accept-Language": "en-US,en;q=0.8",
    })
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return resp.read(MAX_BYTES).decode("utf-8", errors="replace")


def extract_headlines(content, source):
    items = []
    seen = set()
    fmt = source.get("format", "html")

    if fmt == "html":
        for m in re.finditer(source["title_re"], content, flags=re.S | re.I):
            url = m.group("url")
            title = re.sub(r"\s+", " ", m.group("title")).strip()
            if not title or url in seen:
                continue
            seen.add(url)
            items.append({"title": title, "url": url})
            if len(items) >= 15:
                break
    elif fmt == "atom":
        # Atom: <entry><title>...</title><link href="..."/>
        entries = re.findall(
            r'<entry>(.*?)</entry>', content, flags=re.S | re.I,
        )
        for entry in entries:
            tm = re.search(r'<title[^>]*>(.*?)</title>', entry, re.S)
            lm = re.search(r'<link[^>]+href="([^"]+)"', entry)
            if not tm or not lm:
                continue
            title = re.sub(r'<!\[CDATA\[|\]\]>', '', tm.group(1)).strip()
            title = re.sub(r'\s+', ' ', title)
            url = lm.group(1)
            if url in seen or not title:
                continue
            seen.add(url)
            items.append({"title": title, "url": url})
            if len(items) >= 15:
                break
    elif fmt == "rss":
        # RSS 2.0: <item><title>...</title><link>...</link>
        rss_items = re.findall(r'<item>(.*?)</item>', content, flags=re.S | re.I)
        for entry in rss_items:
            tm = re.search(r'<title[^>]*>(.*?)</title>', entry, re.S)
            lm = re.search(r'<link[^>]*>(.*?)</link>', entry, re.S)
            if not tm or not lm:
                continue
            title = re.sub(r'<!\[CDATA\[|\]\]>', '', tm.group(1)).strip()
            title = re.sub(r'\s+', ' ', title)
            url = lm.group(1).strip()
            if url in seen or not title:
                continue
            seen.add(url)
            items.append({"title": title, "url": url})
            if len(items) >= 15:
                break
    return items


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    out_lines = [
        "# English Editorial Headlines (AI)",
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
                out_lines.append("_(parse returned 0 items — selectors may need updating)_")
            for i, it in enumerate(items[:10], 1):
                out_lines.append(f"{i}. [{it['title']}]({it['url']})")
        except Exception as e:
            out_lines.append(f"_(fetch failed: {e})_")
        out_lines.append("")

    with open(OUT_PATH, "w") as f:
        f.write("\n".join(out_lines))

    print(f"[editorial-en] wrote {OUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
