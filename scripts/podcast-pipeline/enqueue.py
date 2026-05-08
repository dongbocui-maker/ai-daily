#!/usr/bin/env python3
"""
enqueue.py — Layer 1: 提交一个精读播客任务

职责：
- 验证精读 JSON 存在 + 格式正确（quotes 必须是 [{en, zh}]）
- 创建本月 notebook（如果不存在）
- 把精读 markdown 加为 source
- 调 generate audio 拿 task_id
- 写 state.json: step=queued，data 里有 task_id

退出后立即返回，不等音频生成。worker 会接管。

用法：
  enqueue.py <slug>
  enqueue.py ai-call-center-revolution

退出码：
  0 成功提交，state 已写入
  1 验证失败（JSON 格式错、找不到精读文件）
  2 NotebookLM 调用失败（不重试，直接返回让人介入）
  3 任务已存在
"""
from __future__ import annotations
import argparse
import glob
import json
import os
import sys
import shutil
import tempfile
from datetime import datetime, timezone, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import state as S
from util import nblm, nblm_json, ensure_mihomo, run, get_logger, CmdResult

PROJECT_ROOT = Path("/root/.openclaw/workspace/projects/ai-daily")
READS_DIR = PROJECT_ROOT / "src" / "data" / "reads"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
SHANGHAI = timezone(timedelta(hours=8))

log = get_logger("enqueue")


def find_reads_json(slug: str) -> Path:
    matches = list(READS_DIR.glob(f"*-{slug}.json"))
    if not matches:
        raise FileNotFoundError(
            f"找不到 {slug} 对应的精读 JSON。期望路径形如：{READS_DIR}/YYYY-MM-DD-{slug}.json"
        )
    if len(matches) > 1:
        raise RuntimeError(f"多个文件匹配 {slug}：{matches}")
    return matches[0]


def validate_quotes(reads_path: Path) -> tuple[str, list]:
    """验证 quotes 字段必须是 [{en, zh}]，并返回 titleZh + quotes"""
    data = json.loads(reads_path.read_text(encoding="utf-8"))
    title = data.get("titleZh") or data.get("title") or ""
    if not title:
        raise ValueError(f"{reads_path.name} 缺 titleZh / title 字段")

    quotes = data.get("quotes", [])
    if quotes and not isinstance(quotes[0], dict):
        raise ValueError(
            f"{reads_path.name} quotes 字段格式错——必须是 [{{en,zh}}] "
            "不能是纯字符串列表（5/7 踩过的坑）"
        )
    return title, quotes


def build_source_markdown(slug: str, dest: Path) -> None:
    """调 build-podcast-source.py 生成中文 markdown"""
    builder = SCRIPTS_DIR / "build-podcast-source.py"
    r = run(["python3", str(builder), slug, "-o", str(dest)], timeout=60)
    if not r.ok:
        raise RuntimeError(f"build-podcast-source.py 失败: rc={r.rc}\n{r.stderr}")


def find_or_create_notebook(month_title: str) -> str:
    """返回 notebook_id"""
    r, parsed = nblm_json("list", "--json", timeout=60)
    if not r.ok:
        raise RuntimeError(f"notebooklm list 失败: {r.stderr[:300]}")

    items = parsed if isinstance(parsed, list) else (parsed or {}).get("notebooks", [])
    for n in items:
        if n.get("title") == month_title:
            log.info(f"复用本月 notebook: {n['id']}")
            return n["id"]

    # 创建
    log.info(f"本月 notebook 不存在，创建: {month_title}")
    r = nblm("create", month_title, timeout=60)
    if not r.ok:
        raise RuntimeError(f"notebooklm create 失败: {r.stderr[:300]}")

    # 重查取 ID（创建命令的输出格式不固定）
    r, parsed = nblm_json("list", "--json", timeout=60)
    if not r.ok:
        raise RuntimeError("create 后 list 失败，无法拿 notebook_id")
    items = parsed if isinstance(parsed, list) else (parsed or {}).get("notebooks", [])
    for n in items:
        if n.get("title") == month_title:
            log.info(f"创建成功: {n['id']}")
            return n["id"]
    raise RuntimeError(f"create 后仍找不到 {month_title}")


def find_or_add_source(notebook_id: str, source_title: str, source_md: Path, work_dir: Path) -> str:
    """如果同名 source 已存在则复用，否则添加"""
    # 切到当前 notebook
    nblm("use", notebook_id, timeout=30)

    # 列已有 source
    r, parsed = nblm_json("source", "list", "--json", timeout=60)
    if r.ok and parsed:
        sources = parsed.get("sources", []) if isinstance(parsed, dict) else parsed
        for s in sources:
            if s.get("title") == source_title:
                log.info(f"复用同名 source: {s['id']}")
                return s["id"]

    # 重命名 markdown 文件，让 NotebookLM 用中文标题
    named_md = work_dir / f"{source_title}.md"
    shutil.copy2(source_md, named_md)

    r, parsed = nblm_json("source", "add", str(named_md), "--json", timeout=120)
    if not r.ok:
        raise RuntimeError(f"source add 失败: {r.stderr[:300]}")

    sid = None
    if parsed:
        sid = (parsed.get("source") or {}).get("id") or parsed.get("id")
    if not sid:
        raise RuntimeError(f"source add 输出缺 id: {r.stdout[:500]}")

    log.info(f"source 已加: {sid}")

    # 等索引完成（不强求）
    nblm("source", "wait", sid, "--timeout", "120", timeout=130)

    # 重命名让标题更整齐（也不强求）
    nblm("source", "rename", sid, source_title, timeout=30)

    return sid


def build_podcast_prompt(source_title: str) -> str:
    return f"""这期播客介绍《{source_title}》。中文双主持人对谈，深度阐释原文。

严格要求：
1. 本期节目标题必须是《{source_title}》。不要重写、不要改名、不要起别的名字。
2. 所有论点、数据、例子、引言、背景信息都必须严格出自原文。不准编原文未讲过的内容。
3. 可以重述、阐释、讨论原文观点，但不准联想、不准类比到原文未提的例子、不准「补充背景」。
4. 如果原文某个点介绍不够详细，说「作者未详述」即可，不准填补。
风格：严谨专业、信息密集、面向专业人士，不要闲聊化。"""


def submit_audio_generation(source_id: str, source_title: str) -> str:
    """调 generate audio --json 拿 task_id"""
    prompt = build_podcast_prompt(source_title)
    r, parsed = nblm_json(
        "generate", "audio",
        "-s", source_id,
        "--format", "deep-dive",
        "--length", "long",
        "--language", "zh_Hans",
        "--json",
        prompt,
        timeout=120,
    )
    if not r.ok or not parsed:
        raise RuntimeError(f"generate audio 失败: rc={r.rc} stderr={r.stderr[:300]}")
    task_id = parsed.get("task_id")
    if not task_id:
        raise RuntimeError(f"generate audio 输出缺 task_id: {r.stdout[:500]}")
    log.info(f"generate audio 已提交，task_id={task_id}")
    return task_id


def main() -> int:
    parser = argparse.ArgumentParser(description="提交精读播客任务")
    parser.add_argument("slug", help="精读 slug（不带日期前缀）")
    parser.add_argument("--force", action="store_true", help="即使已存在也重新创建")
    args = parser.parse_args()

    slug = args.slug

    # 已存在检查
    if S.exists(slug):
        existing = S.load(slug)
        if not args.force:
            log.info(f"任务已存在: {slug} step={existing['step']}")
            print(json.dumps(existing, ensure_ascii=False, indent=2))
            return 3
        # force：归档旧的
        S.archive(slug)
        log.info(f"归档旧任务: {slug}")

    # 1. 找精读 JSON 验证格式
    try:
        reads_path = find_reads_json(slug)
        title, quotes = validate_quotes(reads_path)
    except (FileNotFoundError, ValueError, RuntimeError) as e:
        log.error(f"验证失败: {e}")
        return 1

    log.info(f"精读：{reads_path.name}")
    log.info(f"标题：{title}")
    log.info(f"Quotes 数：{len(quotes)} (格式 OK)")

    # 2. 创建 state（submitted）
    state = S.create(slug)

    try:
        ensure_mihomo()

        # 3. 生成 source markdown
        work_dir = Path(tempfile.mkdtemp(prefix=f"podcast-{slug}-"))
        source_md = work_dir / "source.md"
        build_source_markdown(slug, source_md)

        # 4. 找/创 本月 notebook
        month_title = f"AI 日报精读 {datetime.now(SHANGHAI).strftime('%Y-%m')}"
        notebook_id = find_or_create_notebook(month_title)

        # 5. 加 source
        source_id = find_or_add_source(notebook_id, title, source_md, work_dir)

        # 标记到 source_added
        state = S.advance(state, "source_added",
                          notebook_id=notebook_id,
                          notebook_title=month_title,
                          source_id=source_id,
                          source_title=title,
                          work_dir=str(work_dir),
                          reads_json=str(reads_path))

        # 6. 提交 audio 生成
        task_id = submit_audio_generation(source_id, title)

        # 标记到 queued
        state = S.advance(state, "queued", task_id=task_id)

        log.info("=" * 60)
        log.info(f"✅ 任务已入队: {slug}")
        log.info(f"   step: queued")
        log.info(f"   task_id: {task_id}")
        log.info(f"   notebook: {notebook_id}")
        log.info(f"   source: {source_id}")
        log.info(f"   work_dir: {work_dir}")
        log.info("worker 会自动接管，~13-25 分钟后产出音频")
        log.info("=" * 60)

        # 把 state 打印给 stdout 方便调用方解析
        print(json.dumps(state, ensure_ascii=False, indent=2))
        return 0

    except Exception as e:
        log.error(f"❌ 入队失败: {e}")
        S.record_attempt_failure(state, str(e))
        return 2


if __name__ == "__main__":
    sys.exit(main())
