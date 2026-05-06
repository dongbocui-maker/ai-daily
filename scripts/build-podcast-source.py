#!/usr/bin/env python3
"""
build-podcast-source.py — 把精读 JSON 转成 NotebookLM source 输入的 markdown

输入：精读 slug
输出：stdout 一份 markdown（包含原文链接、核心观点、启示、中文解读、金句）
      用于 `notebooklm source add --file` 的输入

设计原则：
  - 让 NotebookLM 主持人有足够素材展开 deep-dive 对话
  - 不只是列要点，要给"语境 + 解读 + 张力"
  - 标题清晰，方便 NotebookLM 索引
"""
import sys
import json
import argparse
import glob
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
READS_DIR = PROJECT_ROOT / "src" / "data" / "reads"


def load_read(slug: str) -> dict:
    candidates = list(READS_DIR.glob(f"*-{slug}.json"))
    if not candidates:
        raise FileNotFoundError(f"找不到精读 JSON：slug={slug}")
    if len(candidates) > 1:
        raise RuntimeError(f"精读 slug 重复：{candidates}")
    with candidates[0].open(encoding="utf-8") as f:
        return json.load(f)


def build_md(article: dict) -> str:
    """精读 JSON → NotebookLM source markdown"""
    parts = []

    # 标题区
    parts.append(f"# {article['titleZh']}")
    parts.append("")
    if article.get("titleEn"):
        parts.append(f"**原标题**：*{article['titleEn']}*")
    parts.append(f"**作者**：{article['author']}"
                 + (f"（{article['authorTitle']}）" if article.get('authorTitle') else ""))
    parts.append(f"**原文链接**：{article['originalUrl']}")
    if article.get("publishDate"):
        parts.append(f"**发布日期**：{article['publishDate']}")
    parts.append("")
    parts.append("---")
    parts.append("")

    # 一句话核心
    parts.append("## 一句话核心")
    parts.append(article["summary"])
    parts.append("")

    # 核心观点
    if article.get("keyPoints"):
        parts.append("## 核心观点")
        for i, p in enumerate(article["keyPoints"], 1):
            parts.append(f"{i}. {p}")
        parts.append("")

    # 启示与思考
    if article.get("insight"):
        parts.append("## 启示与思考")
        parts.append(article["insight"])
        parts.append("")

    # 中文深度解读（这是最重要的播客素材）
    if article.get("summaryZh"):
        parts.append("## 完整深度解读")
        parts.append(article["summaryZh"])
        parts.append("")

    # 金句
    if article.get("quotes"):
        parts.append("## 关键金句")
        for q in article["quotes"]:
            if q.get("en"):
                parts.append(f'> "{q["en"]}"')
            parts.append(f'> 「{q["zh"]}」')
            parts.append("")

    # 标签
    if article.get("tags"):
        parts.append("---")
        parts.append(f"**标签**：{', '.join(article['tags'])}")

    return "\n".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(description="精读 JSON → NotebookLM source markdown")
    parser.add_argument("slug", help="精读 slug（不含日期前缀）")
    parser.add_argument("-o", "--output", help="输出文件路径（不指定则 stdout）")
    args = parser.parse_args()

    try:
        article = load_read(args.slug)
        md = build_md(article)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    if args.output:
        Path(args.output).write_text(md, encoding="utf-8")
        print(f"✅ 写入 {args.output}（{len(md)} 字符）", file=sys.stderr)
    else:
        sys.stdout.write(md)

    return 0


if __name__ == "__main__":
    sys.exit(main())
