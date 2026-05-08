"""
podcast-pipeline/state.py — 状态机的核心抽象

职责：
- 定义 step 状态枚举（顺序前进，不能回退）
- 提供原子读写（避免并发冲突）
- 记录 attempts / last_error / 时间戳 / 历史

每个任务一个 JSON 文件：
  state/podcasts/<slug>.json

文件结构：
{
  "slug": "ai-call-center-revolution",
  "step": "queued",                    # 见 STEPS
  "created_at": "2026-05-08T23:00:00+08:00",
  "updated_at": "2026-05-08T23:05:00+08:00",
  "attempts": 0,                       # 当前 step 已尝试次数
  "total_attempts": 3,                 # 跨所有 step 累计
  "last_error": "...",
  "last_error_at": "...",
  "history": [
      {"step": "submitted",   "at": "2026-05-08T23:00:00+08:00"},
      {"step": "source_added", "at": "2026-05-08T23:00:30+08:00"},
      {"step": "queued",      "at": "2026-05-08T23:01:00+08:00"}
  ],
  "data": {
      # 各步骤产生的数据
      "notebook_id": "b35b...",
      "notebook_title": "AI 日报精读 2026-05",
      "source_id": "...",
      "source_title": "...",
      "task_id": "0b06...",        # NotebookLM task_id == artifact_id
      "audio_path": "/tmp/.../podcast.m4a",
      "audio_size_mb": 18,
      "audio_url": "https://...cos.../...m4a",
      "audio_duration_sec": 1024,
      "json_file": "src/data/reads/2026-05-08-...json"
  }
}
"""
from __future__ import annotations
import json
import os
import tempfile
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any

# State 顺序前进的步骤
# submitted     → 任务刚入队，还未做任何外部调用
# source_added  → notebook 已就绪 + source 已加 + index 完成
# queued        → 已调 generate audio，拿到 task_id（= artifact_id），等 NotebookLM 跑
# audio_ready   → NotebookLM 已生成完成（status=completed）
# downloaded    → m4a 已下到本地
# uploaded      → 已上传 COS，拿到 audio_url
# published     → JSON 已写回 + git committed + git pushed
# done          → 完成（终态）
# stuck         → 重试次数过多，需要人工介入
# failed        → 不可恢复失败（终态）
STEPS = [
    "submitted",
    "source_added",
    "queued",
    "audio_ready",
    "downloaded",
    "uploaded",
    "published",
    "done",
]
TERMINAL_STEPS = {"done", "failed"}
INTERVENE_STEPS = {"stuck", "failed"}

# 每个 step 最多重试次数，超过标 stuck
MAX_ATTEMPTS_PER_STEP = {
    "submitted": 3,
    "source_added": 5,
    "queued": 200,        # NotebookLM 生成需要 13-25 分钟，5 分钟一次 cron = 50 次循环不算多
    "audio_ready": 5,
    "downloaded": 5,
    "uploaded": 8,
    "published": 8,
}

SHANGHAI = timezone(timedelta(hours=8))
STATE_DIR = Path("/root/.openclaw/workspace/projects/ai-daily/state/podcasts")


def _now() -> str:
    return datetime.now(SHANGHAI).isoformat(timespec="seconds")


def _state_path(slug: str) -> Path:
    return STATE_DIR / f"{slug}.json"


def exists(slug: str) -> bool:
    return _state_path(slug).exists()


def load(slug: str) -> dict[str, Any]:
    """读 state 文件，没有就返回 None"""
    p = _state_path(slug)
    if not p.exists():
        raise FileNotFoundError(f"state not found: {slug}")
    return json.loads(p.read_text(encoding="utf-8"))


def load_all() -> list[dict[str, Any]]:
    """读所有 state，按 updated_at 升序"""
    if not STATE_DIR.exists():
        return []
    items = []
    for p in STATE_DIR.glob("*.json"):
        try:
            items.append(json.loads(p.read_text(encoding="utf-8")))
        except Exception:
            continue
    items.sort(key=lambda x: x.get("updated_at", ""))
    return items


def save_atomic(state: dict[str, Any]) -> None:
    """原子写：tmp file + rename，避免读到半截"""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    p = _state_path(state["slug"])
    state["updated_at"] = _now()
    fd, tmp = tempfile.mkstemp(dir=STATE_DIR, prefix=".tmp.", suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        os.replace(tmp, p)
    except Exception:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def create(slug: str) -> dict[str, Any]:
    """新建任务"""
    if exists(slug):
        raise ValueError(f"task already exists: {slug}")
    state = {
        "slug": slug,
        "step": "submitted",
        "created_at": _now(),
        "updated_at": _now(),
        "attempts": 0,
        "total_attempts": 0,
        "last_error": None,
        "last_error_at": None,
        "history": [{"step": "submitted", "at": _now()}],
        "data": {},
    }
    save_atomic(state)
    return state


def advance(state: dict[str, Any], next_step: str, **data_updates: Any) -> dict[str, Any]:
    """
    前进到下一步。重置 attempts，写 history。
    data_updates 会 merge 进 state["data"]。
    """
    state["step"] = next_step
    state["attempts"] = 0
    state["last_error"] = None
    state["last_error_at"] = None
    if data_updates:
        state.setdefault("data", {}).update(data_updates)
    state.setdefault("history", []).append({"step": next_step, "at": _now()})
    save_atomic(state)
    return state


def record_attempt_failure(state: dict[str, Any], error: str) -> dict[str, Any]:
    """
    本 step 内一次尝试失败：
    - attempts +1
    - 如果超过该 step 的 MAX_ATTEMPTS，标 stuck
    """
    state["attempts"] = state.get("attempts", 0) + 1
    state["total_attempts"] = state.get("total_attempts", 0) + 1
    state["last_error"] = error[:1000]
    state["last_error_at"] = _now()

    cap = MAX_ATTEMPTS_PER_STEP.get(state["step"], 5)
    if state["attempts"] >= cap:
        state["step"] = "stuck"
        state.setdefault("history", []).append({
            "step": "stuck",
            "at": _now(),
            "from": state.get("history", [{}])[-1].get("step"),
            "reason": f"exceeded MAX_ATTEMPTS={cap}",
        })

    save_atomic(state)
    return state


def mark_failed(state: dict[str, Any], error: str) -> dict[str, Any]:
    """标记不可恢复失败（终态）"""
    state["step"] = "failed"
    state["last_error"] = error[:1000]
    state["last_error_at"] = _now()
    state.setdefault("history", []).append({"step": "failed", "at": _now(), "reason": error[:300]})
    save_atomic(state)
    return state


def reset_stuck(slug: str) -> dict[str, Any]:
    """从 stuck 恢复——回退到 stuck 之前那个 step，attempts 清零"""
    state = load(slug)
    if state["step"] != "stuck":
        return state
    # 倒着找最后一个非 stuck 的 step
    history = state.get("history", [])
    for h in reversed(history):
        if h["step"] != "stuck":
            state["step"] = h["step"]
            state["attempts"] = 0
            state["last_error"] = None
            state["last_error_at"] = None
            state.setdefault("history", []).append({
                "step": h["step"],
                "at": _now(),
                "note": "recovered from stuck",
            })
            save_atomic(state)
            return state
    raise RuntimeError(f"cannot find non-stuck step in history for {slug}")


def archive(slug: str) -> Path:
    """完成或永久失败的任务挪到 .archive"""
    p = _state_path(slug)
    if not p.exists():
        raise FileNotFoundError(slug)
    archive_dir = STATE_DIR / ".archive"
    archive_dir.mkdir(exist_ok=True)
    target = archive_dir / f"{slug}.{datetime.now(SHANGHAI).strftime('%Y%m%d-%H%M%S')}.json"
    p.rename(target)
    return target
