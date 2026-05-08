#!/usr/bin/env python3
"""
status.py — Layer 3: 查询任务状态（秒级返回）

用法：
  status.py             # 总览所有 active 任务
  status.py <slug>      # 详细状态
  status.py --all       # 含归档
  status.py --json      # JSON 输出（给我钢铁虾解析用）
"""
from __future__ import annotations
import argparse
import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import state as S

SHANGHAI = timezone(timedelta(hours=8))


def fmt_age(iso: str) -> str:
    if not iso:
        return "?"
    try:
        t = datetime.fromisoformat(iso)
    except ValueError:
        return "?"
    now = datetime.now(SHANGHAI)
    delta = now - t
    secs = int(delta.total_seconds())
    if secs < 60:
        return f"{secs}s"
    if secs < 3600:
        return f"{secs // 60}m"
    if secs < 86400:
        return f"{secs // 3600}h{(secs % 3600) // 60}m"
    return f"{secs // 86400}d"


STEP_EMOJI = {
    "submitted": "📝",
    "source_added": "📚",
    "queued": "⏳",
    "audio_ready": "🎵",
    "downloaded": "💾",
    "uploaded": "☁️",
    "published": "📤",
    "done": "✅",
    "stuck": "🚧",
    "failed": "❌",
}


def print_summary(states: list[dict]) -> None:
    if not states:
        print("无任务")
        return

    print(f"{'slug':<45} {'step':<14} {'attempts':<10} {'age':<8} {'note':<30}")
    print("-" * 120)
    for s in states:
        emoji = STEP_EMOJI.get(s["step"], "❓")
        slug = s["slug"][:44]
        step_str = f"{emoji} {s['step']}"
        age = fmt_age(s.get("updated_at", ""))
        attempts = f"{s.get('attempts', 0)}/{s.get('total_attempts', 0)}"
        note = ""
        if s["step"] == "stuck":
            note = (s.get("last_error") or "")[:30]
        elif s["step"] == "queued":
            note = f"task={s.get('data', {}).get('task_id', '?')[:8]}"
        elif s["step"] == "uploaded":
            url = s.get("data", {}).get("audio_url", "")
            note = url[-30:] if url else ""
        print(f"{slug:<45} {step_str:<14} {attempts:<10} {age:<8} {note:<30}")


def print_detail(state: dict) -> None:
    print(json.dumps(state, ensure_ascii=False, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser(description="查询任务状态")
    parser.add_argument("slug", nargs="?", help="某个 slug 的详情")
    parser.add_argument("--all", action="store_true", help="含归档")
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    parser.add_argument("--active-only", action="store_true", help="只看活跃任务")
    args = parser.parse_args()

    if args.slug:
        try:
            state = S.load(args.slug)
        except FileNotFoundError:
            print(f"找不到任务: {args.slug}", file=sys.stderr)
            return 1
        if args.json:
            print(json.dumps(state, ensure_ascii=False, indent=2))
        else:
            print_detail(state)
        return 0

    states = S.load_all()
    if args.active_only:
        states = [s for s in states if s["step"] not in S.TERMINAL_STEPS]

    if args.json:
        print(json.dumps(states, ensure_ascii=False, indent=2))
    else:
        print_summary(states)
    return 0


if __name__ == "__main__":
    sys.exit(main())
