#!/usr/bin/env python3
"""
notebooklm-poll.py — generate-podcast.sh 的幂等 + 轮询助手

用 snapshot before/after 策略找出本次 generate audio 创建的新 artifact，
不依赖 title 模糊匹配（NotebookLM 必然改写 title）。

子命令：

  before <notebook-id>
    输出当前 audio artifact ID 集合（一行一个），可重定向到文件作为 BEFORE 集。

  in-progress-recent <notebook-id> [minutes]
    输出最近 N 分钟（默认 30）创建的 in_progress audio artifact ID（如有），用于检测双生成。

  poll <notebook-id> <before-ids-file> [--max-tries N] [--interval S]
    轮询「不在 before 集且 status=completed」的新 audio artifact。
    出现就输出 ID 并退出 0；超时退出 1。
    每次轮询失败 print 一条进度到 stderr（不影响 stdout 解析）。
"""
import os
import sys
import time
import json
import argparse
import subprocess
from datetime import datetime, timedelta


def get_notebooklm_bin() -> str:
    """优先用环境变量 NOTEBOOKLM，没有就尝试默认路径"""
    env = os.environ.get("NOTEBOOKLM")
    if env:
        return env
    default = "/root/.openclaw/workspace/projects/ai-fireside/.venv/bin/notebooklm"
    if os.path.isfile(default):
        return default
    return "notebooklm"


def list_audio_artifacts(notebook_id: str) -> list[dict]:
    """调 notebooklm artifact list，返回所有 audio artifact"""
    bin_path = get_notebooklm_bin()
    result = subprocess.run(
        [bin_path, "artifact", "list", "-n", notebook_id, "--type", "audio", "--json"],
        capture_output=True, text=True, timeout=30,
    )
    if result.returncode != 0:
        print(f"  ⚠️ artifact list 失败 rc={result.returncode}: {result.stderr[:300]}", file=sys.stderr)
        return []
    try:
        data = json.loads(result.stdout)
        return data.get("artifacts", []) if isinstance(data, dict) else data or []
    except json.JSONDecodeError as e:
        print(f"  ⚠️ artifact list JSON 解析失败：{e}", file=sys.stderr)
        return []


def cmd_before(notebook_id: str) -> int:
    items = list_audio_artifacts(notebook_id)
    for a in items:
        if a.get("id"):
            print(a["id"])
    return 0


def cmd_in_progress_recent(notebook_id: str, minutes: int) -> int:
    items = list_audio_artifacts(notebook_id)
    cutoff = datetime.now() - timedelta(minutes=minutes)
    for a in items:
        if a.get("status") != "in_progress":
            continue
        ct_str = a.get("created_at", "").split("+")[0]
        try:
            ct = datetime.fromisoformat(ct_str)
        except ValueError:
            continue
        # NotebookLM 的 created_at 是无时区的本地时间字面量
        if ct >= cutoff:
            print(a["id"])
            return 0
    return 0


def cmd_poll(notebook_id: str, before_file: str, max_tries: int, interval: int) -> int:
    try:
        with open(before_file, "r", encoding="utf-8") as f:
            before_ids = {l.strip() for l in f if l.strip()}
    except FileNotFoundError:
        before_ids = set()
    print(f"  ⏳ poll: before={len(before_ids)} ids, max_tries={max_tries}, interval={interval}s",
          file=sys.stderr)

    start_epoch = time.time()
    for i in range(1, max_tries + 1):
        time.sleep(interval)
        items = list_audio_artifacts(notebook_id)
        # 找：不在 before 集 + status=completed
        for a in items:
            aid = a.get("id")
            if not aid or aid in before_ids:
                continue
            status = a.get("status")
            if status == "completed":
                elapsed = int(time.time() - start_epoch)
                print(f"  ✅ 找到新 completed artifact: {aid}（耗时 {elapsed}s, 轮询 #{i}）",
                      file=sys.stderr)
                print(aid)
                return 0
            # 还在生成
        # 进度日志（每 4 次）
        if i % 4 == 0:
            elapsed = int(time.time() - start_epoch)
            new_in_progress = sum(
                1 for a in items
                if a.get("id") not in before_ids and a.get("status") == "in_progress"
            )
            print(f"  …还在生成中（已等 {elapsed}s / 轮询 #{i}, 新 in_progress={new_in_progress}）",
                  file=sys.stderr)

    print(f"  ❌ 轮询 {max_tries * interval}s 后仍未发现新 completed artifact", file=sys.stderr)
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(description="generate-podcast.sh 的幂等 + 轮询助手")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_before = sub.add_parser("before", help="snapshot 当前 audio artifact ID 集")
    p_before.add_argument("notebook_id")

    p_ipr = sub.add_parser("in-progress-recent", help="检测最近 in_progress（避免双生成）")
    p_ipr.add_argument("notebook_id")
    p_ipr.add_argument("minutes", type=int, nargs="?", default=30)

    p_poll = sub.add_parser("poll", help="轮询新 completed artifact")
    p_poll.add_argument("notebook_id")
    p_poll.add_argument("before_file")
    p_poll.add_argument("--max-tries", type=int, default=70, help="默认 70 次")
    p_poll.add_argument("--interval", type=int, default=30, help="默认 30s")

    args = parser.parse_args()

    if args.cmd == "before":
        return cmd_before(args.notebook_id)
    if args.cmd == "in-progress-recent":
        return cmd_in_progress_recent(args.notebook_id, args.minutes)
    if args.cmd == "poll":
        return cmd_poll(args.notebook_id, args.before_file, args.max_tries, args.interval)
    return 2


if __name__ == "__main__":
    sys.exit(main())
