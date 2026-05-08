#!/usr/bin/env python3
"""
worker.py — Layer 2: 后台 worker（cron 拉起，每 5 分钟一次）

职责：扫所有 active state，按 step 推进。每步是幂等的，失败不破坏 state。

state transition：
  queued       → audio_ready    （poll 到 status=completed）
  audio_ready  → downloaded     （下载 m4a 到 state['data']['audio_path']）
  downloaded   → uploaded       （上传 COS）
  uploaded     → published      （写回 JSON + git commit + git push）
  published    → done           （归档 state 文件）

worker 跑一轮的流程：
1. 列所有 state（排除 done/failed/stuck）
2. 用 lock 防同时跑多个 worker
3. 对每个 active 任务调对应的 step handler
4. 一轮跑完写运行日志

CSRF 抖动等暂时性失败：record_attempt_failure 但不抛出，下次 cron 再来。
不可恢复失败（比如 task_id 已被删除）：mark_failed。

用法：
  worker.py             # 跑一轮
  worker.py --slug X    # 只跑某个任务
  worker.py --dry-run   # 只看会做什么不实际做
"""
from __future__ import annotations
import argparse
import fcntl
import json
import os
import shutil
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import state as S
from util import nblm, nblm_json, ensure_mihomo, run, get_logger, CmdResult

PROJECT_ROOT = Path("/root/.openclaw/workspace/projects/ai-daily")
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
LOCK_FILE = Path("/tmp/podcast-worker.lock")

log = get_logger("worker")


def acquire_lock():
    """文件锁，避免同时跑多个 worker"""
    f = open(LOCK_FILE, "w")
    try:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        f.write(f"{os.getpid()}\n")
        f.flush()
        return f
    except BlockingIOError:
        log.info("另一个 worker 在跑，跳过本轮")
        return None


# ===================== Step handlers =====================

def handle_queued(state: dict) -> dict:
    """检查 NotebookLM task 是否完成"""
    task_id = state["data"].get("task_id")
    notebook_id = state["data"].get("notebook_id")
    if not task_id or not notebook_id:
        S.mark_failed(state, "queued state 缺 task_id 或 notebook_id")
        return state

    # poll：CLI 会返回 task 状态
    r, parsed = nblm_json("artifact", "poll", task_id, "-n", notebook_id, timeout=60)

    # CSRF 抖动等暂时失败：non-zero rc 但不是"task 不存在"
    if not r.ok:
        # CSRF 超时大多数表现为 "Error:" 空消息 + 30s timeout
        err_brief = (r.stderr or r.stdout or "").strip()[:200]
        log.info(f"  [{state['slug']}] queued: poll 失败（暂时）：rc={r.rc} {err_brief}")
        S.record_attempt_failure(state, f"poll rc={r.rc}: {err_brief}")
        return state

    # poll CLI 输出格式见示例（需要解析 status 字段）
    if not parsed:
        # 输出不是 JSON——可能是 plain text："Status: in_progress" 之类
        out = (r.stdout or "").strip()
        log.info(f"  [{state['slug']}] queued: poll 输出非 JSON: {out[:200]}")
        if "completed" in out.lower():
            S.advance(state, "audio_ready")
            log.info(f"  [{state['slug']}] queued → audio_ready")
        else:
            # 还在跑
            S.record_attempt_failure(state, f"poll plain output: {out[:200]}")
        return state

    status = parsed.get("status") if isinstance(parsed, dict) else None
    if status == "completed":
        log.info(f"  [{state['slug']}] queued → audio_ready ✅")
        S.advance(state, "audio_ready")
    elif status in ("in_progress", "queued", "pending"):
        log.info(f"  [{state['slug']}] queued: 还在生成（{status}）")
        # 不算失败，但更新 attempts 让监控可见
        state["attempts"] = state.get("attempts", 0) + 1
        S.save_atomic(state)
    elif status in ("failed", "error"):
        S.mark_failed(state, f"NotebookLM 报告 task failed: {parsed}")
    else:
        log.info(f"  [{state['slug']}] queued: 未知 status={status}")
        S.record_attempt_failure(state, f"unknown status: {status}")

    return state


def handle_audio_ready(state: dict) -> dict:
    """下载 m4a"""
    task_id = state["data"]["task_id"]
    work_dir = Path(state["data"].get("work_dir", f"/tmp/podcast-{state['slug']}"))
    work_dir.mkdir(parents=True, exist_ok=True)
    audio_path = work_dir / "podcast.m4a"

    r = nblm("download", "audio", "-a", task_id, str(audio_path), timeout=300)
    if not r.ok:
        log.info(f"  [{state['slug']}] download 失败: {r.stderr[:200]}")
        S.record_attempt_failure(state, f"download rc={r.rc}: {r.stderr[:200]}")
        return state
    if not audio_path.exists():
        S.record_attempt_failure(state, "download 报成功但文件不存在")
        return state

    size_mb = audio_path.stat().st_size // (1024 * 1024)
    log.info(f"  [{state['slug']}] audio_ready → downloaded ✅ ({size_mb} MB)")
    S.advance(state, "downloaded",
              audio_path=str(audio_path),
              audio_size_mb=size_mb)
    return state


def handle_downloaded(state: dict) -> dict:
    """上传 COS——复用现有 publish-audio.sh"""
    audio_path = state["data"]["audio_path"]
    if not Path(audio_path).exists():
        # m4a 没了——可能 /tmp 被清理了。回退到 audio_ready 重下
        log.info(f"  [{state['slug']}] m4a 丢失，回退到 audio_ready: {audio_path}")
        state["step"] = "audio_ready"
        state["attempts"] = 0
        S.save_atomic(state)
        return state

    upload_script = SCRIPTS_DIR / "upload-audio.py"
    creds_file = "/root/.config/cos/credentials.env"

    # 加载 COS 凭据
    if not Path(creds_file).exists():
        S.mark_failed(state, f"COS 凭据文件不存在: {creds_file}")
        return state

    env_extra = {}
    for line in Path(creds_file).read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env_extra[k.strip()] = v.strip().strip('"').strip("'")

    r = run(
        ["python3", str(upload_script), audio_path, "--mode", "reads", "--slug", state["slug"], "--quiet"],
        timeout=300,
        env_extra=env_extra,
    )
    if not r.ok:
        log.info(f"  [{state['slug']}] COS 上传失败: rc={r.rc} {r.stderr[:200]}")
        S.record_attempt_failure(state, f"upload rc={r.rc}: {r.stderr[:200]}")
        return state

    # 解析 upload-audio.py 输出（meta JSON）
    try:
        meta = json.loads(r.stdout)
    except json.JSONDecodeError:
        log.info(f"  [{state['slug']}] upload-audio.py 输出非 JSON: {r.stdout[:300]}")
        S.record_attempt_failure(state, f"upload output non-JSON: {r.stdout[:300]}")
        return state

    log.info(f"  [{state['slug']}] downloaded → uploaded ✅")
    S.advance(state, "uploaded",
              audio_url=meta.get("url") or meta.get("audio_url"),
              audio_meta=meta)
    return state


def handle_uploaded(state: dict) -> dict:
    """写回 JSON + git commit + push"""
    write_script = SCRIPTS_DIR / "write-audio-meta.py"
    audio_meta = state["data"].get("audio_meta")
    if not audio_meta:
        S.mark_failed(state, "uploaded state 缺 audio_meta")
        return state

    r = run(
        ["python3", str(write_script), "--mode", "reads", "--slug", state["slug"]],
        timeout=60,
        input_data=json.dumps(audio_meta, ensure_ascii=False),
    )
    if not r.ok:
        log.info(f"  [{state['slug']}] 写 JSON 失败: {r.stderr[:200]}")
        S.record_attempt_failure(state, f"write-audio-meta rc={r.rc}: {r.stderr[:200]}")
        return state

    # git add + commit + push
    project_dir = PROJECT_ROOT
    json_glob = list((project_dir / "src" / "data" / "reads").glob(f"*-{state['slug']}.json"))
    if not json_glob:
        S.mark_failed(state, f"找不到 reads JSON: {state['slug']}")
        return state
    json_file = json_glob[0].relative_to(project_dir)

    log.info(f"  [{state['slug']}] git add {json_file}")
    r = run(["git", "-C", str(project_dir), "add", str(json_file)], timeout=30)
    if not r.ok:
        S.record_attempt_failure(state, f"git add: {r.stderr[:200]}")
        return state

    r = run(
        ["git", "-C", str(project_dir), "commit", "-m", f"feat(reads): 加 {state['slug']} 精读播客"],
        timeout=30,
    )
    # commit 失败可能是 nothing to commit（之前手动 commit 过），这种允许跳过
    if not r.ok and "nothing to commit" not in (r.stdout + r.stderr):
        S.record_attempt_failure(state, f"git commit: {r.stderr[:200]}")
        return state

    # pull --rebase + push（pull 失败也算暂时性）
    r = run(["git", "-C", str(project_dir), "pull", "--rebase"], timeout=60)
    if not r.ok:
        log.info(f"  [{state['slug']}] git pull 失败（暂时）: {r.stderr[:200]}")
        S.record_attempt_failure(state, f"git pull: {r.stderr[:200]}")
        return state

    r = run(["git", "-C", str(project_dir), "push"], timeout=180)
    if not r.ok:
        log.info(f"  [{state['slug']}] git push 失败（暂时）: {r.stderr[:200]}")
        S.record_attempt_failure(state, f"git push: {r.stderr[:200]}")
        return state

    log.info(f"  [{state['slug']}] uploaded → published ✅")
    S.advance(state, "published",
              json_file=str(json_file))
    return state


def handle_published(state: dict) -> dict:
    """归档 state，标 done"""
    log.info(f"  [{state['slug']}] published → done 🎉")
    S.advance(state, "done")
    # 归档
    archived_to = S.archive(state["slug"])
    log.info(f"  [{state['slug']}] state 已归档: {archived_to}")
    return state


HANDLERS = {
    "queued": handle_queued,
    "audio_ready": handle_audio_ready,
    "downloaded": handle_downloaded,
    "uploaded": handle_uploaded,
    "published": handle_published,
}


# ===================== Main loop =====================

def process_one(state: dict, dry_run: bool = False) -> None:
    step = state["step"]
    if step in S.TERMINAL_STEPS:
        return
    if step == "stuck":
        log.info(f"  [{state['slug']}] STUCK ({state['attempts']} attempts) — 跳过 (用 reset_stuck 恢复)")
        return
    handler = HANDLERS.get(step)
    if not handler:
        log.info(f"  [{state['slug']}] 没找到 step={step} 的 handler")
        return

    if dry_run:
        log.info(f"  [{state['slug']}] [dry-run] 会跑 {handler.__name__}")
        return

    try:
        handler(state)
    except Exception as e:
        log.exception(f"  [{state['slug']}] handler 抛异常")
        S.record_attempt_failure(state, f"handler exception: {e}")


def main() -> int:
    parser = argparse.ArgumentParser(description="podcast worker")
    parser.add_argument("--slug", help="只跑这一个 slug")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    lock = acquire_lock()
    if not lock:
        return 0

    try:
        ensure_mihomo()

        if args.slug:
            try:
                state = S.load(args.slug)
            except FileNotFoundError:
                log.error(f"找不到 state: {args.slug}")
                return 1
            log.info(f"single mode: {args.slug} step={state['step']}")
            process_one(state, args.dry_run)
            return 0

        # 跑所有
        all_states = S.load_all()
        active = [s for s in all_states if s["step"] not in S.TERMINAL_STEPS and s["step"] != "stuck"]
        stuck = [s for s in all_states if s["step"] == "stuck"]
        log.info(f"worker tick: {len(active)} active, {len(stuck)} stuck, {len(all_states)} total")

        for state in active:
            process_one(state, args.dry_run)

        log.info(f"worker tick done")
        return 0
    finally:
        if lock:
            lock.close()
            try:
                LOCK_FILE.unlink()
            except FileNotFoundError:
                pass


if __name__ == "__main__":
    sys.exit(main())
