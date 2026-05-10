#!/usr/bin/env python3
"""
Fetch latest Smol AI News (news.smol.ai) — daily AI Twitter/Reddit/HN aggregation
by swyx (founder of AI Engineer Summit, Latent Space podcast).

Output: /tmp/ai-signals/smol-ai.md — markdown excerpt of latest issue + headlines.
"""
import os
import sys
import time
import urllib.request
import urllib.error
import re

OUT_DIR = "/tmp/ai-signals"
OUT_PATH = os.path.join(OUT_DIR, "smol-ai.md")
URL = "https://news.smol.ai/"
TIMEOUT = 15
MAX_BYTES = 600_000


def fetch(url):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "ai-daily-signals/1.0 (+ai-daily.openclaw.ai)"}
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return resp.read(MAX_BYTES).decode("utf-8", errors="replace")


def html_to_text(html):
    # strip scripts/styles
    html = re.sub(r"<script.*?</script>", "", html, flags=re.S | re.I)
    html = re.sub(r"<style.*?</style>", "", html, flags=re.S | re.I)
    # extract issue links and titles
    issues = re.findall(
        r'<a[^>]*href="(/issues/[^"]+)"[^>]*>(.*?)</a>',
        html, flags=re.S | re.I,
    )
    # tags & topics
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\s+", " ", text).strip()
    return text, issues


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    started = time.time()
    try:
        html = fetch(URL)
    except Exception as e:
        print(f"[smol-ai] fetch failed: {e}", file=sys.stderr)
        with open(OUT_PATH, "w") as f:
            f.write(f"# Smol AI News\n\nFetch failed: {e}\n")
        return 1

    text, issues = html_to_text(html)

    # Compose a markdown digest: latest 5 issue links + first 4000 chars of text
    lines = ["# Smol AI News (news.smol.ai)", "",
             f"_Author: swyx (Latent Space, AI Engineer Summit). Fetched {time.strftime('%Y-%m-%d %H:%M %Z')}_",
             "", "## Recent Issues", ""]
    seen = set()
    for href, title in issues[:8]:
        title_clean = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", title)).strip()
        if not title_clean or href in seen:
            continue
        seen.add(href)
        full_url = href if href.startswith("http") else f"https://news.smol.ai{href}"
        lines.append(f"- [{title_clean}]({full_url})")

    lines += ["", "## Page Text Snippet (first ~4000 chars)", "", text[:4000]]

    with open(OUT_PATH, "w") as f:
        f.write("\n".join(lines))

    print(f"[smol-ai] wrote {OUT_PATH} ({len(text)} chars page text, {len(issues)} issues)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
