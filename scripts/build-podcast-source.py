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

==========================================================================
2026-05-09 v2 升级（C 方案，brynjolfsson 截断事件后）：
  - 加入「段落规整层」——所有 markdown 输出都过自动拆段
  - 单段 > 200 字符 → 自动拆分（基于句号、分号、破折号、编号）
  - 单 keyPoint > 130 字符 → 第一句作 lead，后续缩进
  - 长 insight > 600 字符 → 找(a)(b)(c)/(1)(2)(3)拆段
  - 输出末尾加「讨论指引」防 NotebookLM 提前收尾
  - 输出 stderr 健康度 + 预估时长（不影响 NotebookLM 输入）

  根因：brynjolfsson 精读 summaryZh 段落颗粒度过粗（17 段 / max 365 字符 /
  avg 138 字符），NotebookLM 处理超长无换气段落时会"概括过头"或"提早收尾"。
  对比 13 篇成功精读：max 段 ≤ 239 字符，平均 ≤ 89 字符。
==========================================================================
"""
import sys
import json
import argparse
import glob
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
READS_DIR = PROJECT_ROOT / "src" / "data" / "reads"

# ============ 段落规整层 配置 ============
MAX_PARA_CHARS = 180          # summaryZh 单段超此值就拆
MAX_KEYPOINT_CHARS = 130      # 单条 keyPoint 超此值就 lead+detail 拆
MAX_INSIGHT_CHARS = 600       # insight 超此值找编号拆
WARN_LINE_CHARS = 200         # 警告：单行超此字符数
WARN_AVG_LINE_CHARS = 100     # 警告：平均行长超此值


def load_read(slug: str) -> dict:
    candidates = list(READS_DIR.glob(f"*-{slug}.json"))
    if not candidates:
        raise FileNotFoundError(f"找不到精读 JSON：slug={slug}")
    if len(candidates) > 1:
        raise RuntimeError(f"精读 slug 重复：{candidates}")
    with candidates[0].open(encoding="utf-8") as f:
        return json.load(f)


# ===================== 段落规整层 =====================

def split_long_paragraph(text: str, max_chars: int = MAX_PARA_CHARS) -> list[str]:
    """
    把超长段落拆成多个短段落。

    拆分点优先级（高到低）：
    1. 句号「。」后跟 2 个以上汉字
    2. 分号「；」
    3. 数字编号 `(1) (2) (3)` 或 `1. 2. 3.` 在中间
    4. 全角破折号「——」后跟独立成意句

    保证拆出的每段 ≤ max_chars，且不在引号/括号内部断开。
    """
    if len(text) <= max_chars:
        return [text]

    # 不要拆 markdown 标题、列表项（行首有特殊标记的）
    if text.lstrip().startswith(("#", "-", "*", ">")):
        return [text]

    # 在句号「。」处拆
    # 先用占位符保护"等"、"如"等不应该拆的位置
    # 简单策略：「。」后紧跟非标点的中文/英文字符就是拆点
    sentences = re.split(r'(?<=。)(?=[\u4e00-\u9fff\w])', text)

    if len(sentences) <= 1:
        # 没拆成功，尝试分号
        sentences = re.split(r'(?<=；)\s*', text)

    if len(sentences) <= 1:
        # 还没拆成功，尝试破折号
        sentences = re.split(r'(?<=——)\s*(?=[\u4e00-\u9fff])', text)

    if len(sentences) <= 1:
        # 实在拆不开就保持原样（有可能是引号里的内容）
        return [text]

    # 把短句合并到接近 max_chars 的段
    merged = []
    buf = ""
    for s in sentences:
        s = s.strip()
        if not s:
            continue
        if not buf:
            buf = s
        elif len(buf) + len(s) + 1 <= max_chars:
            buf = buf + s if buf.endswith(("。", "；", "！", "？")) else buf + " " + s
        else:
            merged.append(buf)
            buf = s
    if buf:
        merged.append(buf)

    # 如果某个段落还是超长，重拆一次（但只拆一轮防爆栈）
    final = []
    for seg in merged:
        if len(seg) > max_chars and "(" in seg:
            # 含编号 (a) / (1) → 在编号前拆
            sub_parts = re.split(r'(?=\([a-z\d]\))', seg)
            sub_parts = [p.strip() for p in sub_parts if p.strip()]
            if len(sub_parts) > 1:
                final.extend(sub_parts)
                continue

        # 超长且含多个句号 → 以句号为边界再拆
        if len(seg) > max_chars:
            sentences = re.split(r'(?<=。)\s*', seg)
            sentences = [s.strip() for s in sentences if s.strip()]
            if len(sentences) > 1:
                # 合并短句到接近 max_chars 但不到超过
                buf = ""
                for s in sentences:
                    if not buf:
                        buf = s
                    elif len(buf) + len(s) <= max_chars:
                        buf = buf + s
                    else:
                        final.append(buf)
                        buf = s
                if buf:
                    final.append(buf)
                continue

        final.append(seg)

    return final


def reformat_paragraph_block(text: str) -> str:
    """
    对包含多段的 markdown 文本（用 \n\n 分段）逐段规整，输出新的 \n\n 分隔字符串。
    保留原本就是列表 / 标题 / 引用的段落不动。
    """
    paras = text.split("\n\n")
    new_paras = []
    for p in paras:
        p = p.strip()
        if not p:
            continue
        sub = split_long_paragraph(p, MAX_PARA_CHARS)
        new_paras.extend(sub)
    return "\n\n".join(new_paras)


def reformat_keypoint(point: str) -> str:
    """
    对超长 keyPoint 做"lead + detail"拆分：
    第一句作为要点本身，后续作为 sub-bullet 子项。
    """
    if len(point) <= MAX_KEYPOINT_CHARS:
        return point

    # 找第一句结尾（句号 / 冒号后跟描述）
    # 优先：粗体「**...**」段后第一个句号
    m = re.search(r'^(\*\*[^*]+\*\*[^。]*。)(.+)$', point, re.DOTALL)
    if m:
        lead = m.group(1).strip()
        detail = m.group(2).strip()
        # detail 再按句号拆成子项
        details = re.split(r'(?<=。)(?=[\u4e00-\u9fff])', detail)
        details = [d.strip() for d in details if d.strip()]
        if details:
            return lead + "\n" + "\n".join(f"   - {d}" for d in details)

    # 没有粗体引导，尝试找第一个 「：」
    m = re.search(r'^([^：]{10,}：)(.+)$', point, re.DOTALL)
    if m:
        lead = m.group(1).strip()
        detail = m.group(2).strip()
        details = re.split(r'(?<=。)(?=[\u4e00-\u9fff])', detail)
        details = [d.strip() for d in details if d.strip()]
        if len(details) >= 2:
            return lead + "\n" + "\n".join(f"   - {d}" for d in details)

    # 拆不动就保持原样
    return point


def reformat_insight(text: str) -> str:
    """
    长 insight：找 (a)(b)(c) 或 (1)(2)(3) 编号，每个独立成段。
    无关总长——只要内含编号且编号段总长 > MAX_PARA_CHARS 就拆。
    """
    # 找 (a)(b)(c) 类编号
    if re.search(r'\([a-z]\)', text):
        parts = re.split(r'(?=\([a-z]\))', text)
        lead = parts[0].strip()
        items = [p.strip() for p in parts[1:] if p.strip()]
        if lead and items and len(items) >= 2:
            result = lead + "\n\n" + "\n\n".join(f"- {item}" for item in items)
            return reformat_paragraph_block(result)

    # 找 (1)(2)(3) 类
    if re.search(r'\(\d\)', text):
        parts = re.split(r'(?=\(\d\))', text)
        lead = parts[0].strip()
        items = [p.strip() for p in parts[1:] if p.strip()]
        if lead and items and len(items) >= 2:
            result = lead + "\n\n" + "\n\n".join(f"- {item}" for item in items)
            return reformat_paragraph_block(result)

    # 没编号就走通用规整
    return reformat_paragraph_block(text)


# ===================== 健康度报告 =====================

def health_report(md: str, article: dict) -> dict:
    """对生成的 markdown 做健康度统计，stderr 输出

    警告仅针对叙述性段落：exclude 引用行 (> 开头是 markdown quote)、
    列表项 (- / *)、标题 (#)。这些本身就是语义独立的，
    NotebookLM 会作为单位词处理、不会引发提早收尾。
    """
    lines = md.split("\n")
    # 估算总体体量用所有非空行
    line_lens = [len(l) for l in lines if l.strip()]
    # 健康度警告仅看叙述性行
    # 排除：引用 (>)、标题 (#)、列表 (-/*，含缩进)、表格 (|)、编号 (1.)
    narrative_lens = []
    for l in lines:
        if not l.strip():
            continue
        stripped = l.lstrip()
        if stripped.startswith((">", "#", "-", "*", "|")):
            continue
        if re.match(r'^\s*\d+\.\s', l):
            continue
        narrative_lens.append(len(l))
    longest = max(narrative_lens) if narrative_lens else 0
    avg = sum(narrative_lens) // len(narrative_lens) if narrative_lens else 0
    total = len(md)

    # 估时（粗略经验值）
    n_keypoints = len(article.get("keyPoints", []))
    n_quotes = len(article.get("quotes", []))
    summary_zh_chars = len(article.get("summaryZh", ""))

    est_min = round(
        n_keypoints * 0.6        # 每个观点 ~36 秒
        + n_quotes * 0.4          # 每条金句 ~24 秒
        + summary_zh_chars / 800  # 深度解读：800 字 ~ 1 分钟
        + 2                       # 开场 + 结尾
    )
    est_max = round(est_min * 1.3)

    return {
        "total_chars": total,
        "lines": len(lines),
        "non_empty_lines": len(line_lens),
        "longest_line": longest,
        "avg_line": avg,
        "est_duration_min": (est_min, est_max),
        "n_keypoints": n_keypoints,
        "n_quotes": n_quotes,
        "summary_zh_chars": summary_zh_chars,
    }


def build_md(article: dict) -> str:
    """精读 JSON → NotebookLM source markdown（v2: 含段落规整）"""
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
    summary = reformat_paragraph_block(article["summary"])
    parts.append(summary)
    parts.append("")

    # 核心观点（v2: 长条目自动拆 lead/detail）
    if article.get("keyPoints"):
        parts.append("## 核心观点")
        for i, p in enumerate(article["keyPoints"], 1):
            reformatted = reformat_keypoint(p)
            # 多行 keyPoint：保留缩进结构
            if "\n" in reformatted:
                lines = reformatted.split("\n")
                parts.append(f"{i}. {lines[0]}")
                for sub in lines[1:]:
                    parts.append(sub)
            else:
                parts.append(f"{i}. {reformatted}")
            parts.append("")  # 每条之间空行，提升可读性 + 给 NotebookLM 换气位
        parts.append("")

    # 启示与思考（v2: 长 insight 找编号拆段）
    if article.get("insight"):
        parts.append("## 启示与思考")
        parts.append(reformat_insight(article["insight"]))
        parts.append("")

    # 中文深度解读（v2: 自动段落规整 - 这是最重要的修复点）
    if article.get("summaryZh"):
        parts.append("## 完整深度解读")
        parts.append(reformat_paragraph_block(article["summaryZh"]))
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
        parts.append("")

    # v2 新增：讨论指引（防 NotebookLM 提前收尾）
    n_kps = len(article.get("keyPoints", []))
    n_quotes = len(article.get("quotes", []))
    parts.append("---")
    parts.append("")
    parts.append("## 讨论指引（请双主持人务必完整覆盖）")
    parts.append("")
    parts.append(
        f"以上是本期精读的**全部内容**。请双主持人在 deep-dive 对话中：")
    parts.append("")
    parts.append(f"1. 完整讨论所有 **{n_kps} 个核心观点**——不要跳过任何一条")
    parts.append(f"2. 展开「完整深度解读」的所有章节——给每个章节足够时长")
    parts.append(f"3. 引用并解读所有 **{n_quotes} 条关键金句**")
    parts.append("4. 结合「启示与思考」给出对企业、咨询行业的实操建议")
    parts.append("5. 在结尾给出完整收束——不要中途停止")
    parts.append("")
    parts.append("**预期播客时长：15-25 分钟，请充分展开。**")

    return "\n".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(description="精读 JSON → NotebookLM source markdown")
    parser.add_argument("slug", help="精读 slug（不含日期前缀）")
    parser.add_argument("-o", "--output", help="输出文件路径（不指定则 stdout）")
    parser.add_argument("--no-health", action="store_true", help="不输出健康度报告")
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

    if not args.no_health:
        h = health_report(md, article)
        print("", file=sys.stderr)
        print("📊 健康度报告：", file=sys.stderr)
        print(f"   总字符: {h['total_chars']}", file=sys.stderr)
        print(f"   行数: {h['lines']} (非空 {h['non_empty_lines']})", file=sys.stderr)
        print(f"   平均行长: {h['avg_line']} 字符", file=sys.stderr)
        print(f"   最长行: {h['longest_line']} 字符", file=sys.stderr)
        print(f"   keyPoints: {h['n_keypoints']} 条 / quotes: {h['n_quotes']} 条 / summaryZh: {h['summary_zh_chars']} 字符", file=sys.stderr)
        print(f"   ⏱️ 预估播客时长: {h['est_duration_min'][0]}-{h['est_duration_min'][1]} 分钟", file=sys.stderr)

        # 健康度警告
        if h['longest_line'] > WARN_LINE_CHARS:
            print(f"   ⚠️ 警告：最长行 {h['longest_line']} 字符 > 阈值 {WARN_LINE_CHARS}（NotebookLM 可能提早收尾）", file=sys.stderr)
        if h['avg_line'] > WARN_AVG_LINE_CHARS:
            print(f"   ⚠️ 警告：平均行长 {h['avg_line']} 字符 > 阈值 {WARN_AVG_LINE_CHARS}（段落颗粒度过粗）", file=sys.stderr)
        if h['longest_line'] <= WARN_LINE_CHARS and h['avg_line'] <= WARN_AVG_LINE_CHARS:
            print(f"   ✅ 段落结构健康，NotebookLM 可正常处理", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
