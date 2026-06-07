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
import tempfile
from datetime import datetime, timezone, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import state as S
from util import nblm, nblm_json, ensure_mihomo, run, get_logger, CmdResult

PROJECT_ROOT = Path("/root/.openclaw/workspace/projects/ai-daily")
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
WORKSPACE_ROOT = Path("/root/.openclaw/workspace")
AGENT_ACTIONS_DIR = WORKSPACE_ROOT / "memory" / "agent-actions"
JASON_FEISHU_TARGET = "user:ou_dbee86fe0e62ee834c7d7225015a1317"
LOCK_FILE = Path("/tmp/podcast-worker.lock")
SHANGHAI = timezone(timedelta(hours=8))

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


def now_iso() -> str:
    return datetime.now(SHANGHAI).isoformat(timespec="seconds")


def append_agent_action(state: dict, action: str, status: str, summary: str, notes: str | None = None) -> None:
    """把 worker 关键动作写入跨 session 行动日志。失败不影响主流程。"""
    try:
        AGENT_ACTIONS_DIR.mkdir(parents=True, exist_ok=True)
        path = AGENT_ACTIONS_DIR / f"{datetime.now(SHANGHAI).strftime('%Y-%m-%d')}.jsonl"
        record = {
            "ts": now_iso(),
            "session_kind": "system-cron",
            "session_id": "podcast-worker",
            "agent_id": "main",
            "agent_name": "钢铁虾",
            "task_id": "system-cron:podcast-pipeline-worker",
            "task_name": "精读播客状态机 worker",
            "action": action,
            "recipient": JASON_FEISHU_TARGET,
            "channel": "feishu",
            "summary": summary[:200],
            "outputs": {"slug": state.get("slug"), "step": state.get("step")},
            "status": status,
        }
        if notes:
            record["notes"] = notes[:1000]
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except Exception as e:
        log.info(f"  [{state.get('slug')}] 写 agent-actions 失败: {e}")


def notify_intervention(state: dict, status: str) -> None:
    """stuck/failed 时主动通知 Jason；每个 state 只通知一次。"""
    data = state.setdefault("data", {})
    if data.get("intervention_notified"):
        return

    slug = state.get("slug", "unknown")
    last_error = state.get("last_error") or "无 last_error"
    message = (
        f"⚠️ 精读播客 pipeline 需要介入\n"
        f"slug: {slug}\n"
        f"状态: {state.get('step')} / {status}\n"
        f"错误: {last_error[:500]}\n"
        f"已停止自动重试，避免误发布。"
    )
    r = run([
        "openclaw", "message", "send",
        "--channel", "feishu",
        "--target", JASON_FEISHU_TARGET,
        "--message", message,
    ], timeout=60)
    if r.ok:
        data["intervention_notified"] = True
        S.save_atomic(state)
        append_agent_action(state, "podcast_pipeline_intervention_alert", "error", f"精读播客 {slug} 进入 {state.get('step')}，已通知 Jason", last_error)
    else:
        log.info(f"  [{slug}] 飞书告警发送失败: {(r.stderr or r.stdout)[:300]}")
        append_agent_action(state, "podcast_pipeline_intervention_alert_failed", "error", f"精读播客 {slug} 进入 {state.get('step')}，但告警发送失败", (r.stderr or r.stdout or last_error))


def audio_block_from_meta(meta: dict) -> dict:
    required = {"url", "duration_seconds", "size_bytes", "uploaded_at"}
    missing = required - set(meta.keys())
    if missing:
        raise ValueError(f"audio_meta 缺字段: {sorted(missing)}")
    block = {
        "url": meta["url"],
        "duration_seconds": meta["duration_seconds"],
        "size_bytes": meta["size_bytes"],
        "generated_at": meta["uploaded_at"],
    }
    if meta.get("format"):
        block["format"] = meta["format"]
    return block


def write_audio_meta_to_json(target: Path, audio_meta: dict) -> bool:
    """写入 audio metadata。

    返回 True 表示文件语义发生变化；False 表示远端已含相同 audio，避免仅因
    JSON 缩进/字段顺序差异产生无意义 commit。
    """
    data = json.loads(target.read_text(encoding="utf-8"))
    audio = audio_block_from_meta(audio_meta)
    if data.get("audio") == audio:
        return False
    data["audio"] = audio
    tmp = target.with_suffix(target.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(target)
    return True


def cleanup_worktree(worktree: Path) -> None:
    if not worktree.exists():
        return
    run(["git", "-C", str(PROJECT_ROOT), "worktree", "remove", "--force", str(worktree)], timeout=60)
    shutil.rmtree(worktree, ignore_errors=True)


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
    """写回 reads JSON + 用临时 clean worktree commit/push，避免主 workspace 脏文件阻断发布。"""
    audio_meta = state["data"].get("audio_meta")
    if not audio_meta:
        S.mark_failed(state, "uploaded state 缺 audio_meta")
        return state

    try:
        # 先在主 workspace 定位目标文件；发布实际基于 origin/main 的 clean worktree，
        # 不依赖主 workspace 是否干净，也不把无关脏文件带进 commit。
        json_glob = list((PROJECT_ROOT / "src" / "data" / "reads").glob(f"*-{state['slug']}.json"))
        if not json_glob:
            S.mark_failed(state, f"找不到 reads JSON: {state['slug']}")
            return state
        json_file = json_glob[0].relative_to(PROJECT_ROOT)
        audio_block_from_meta(audio_meta)  # 早校验 meta 结构
    except Exception as e:
        S.mark_failed(state, f"audio meta/json 校验失败: {e}")
        return state

    worktree = Path(tempfile.mkdtemp(prefix=f"podcast-publish-{state['slug']}-"))
    try:
        # 确保基于远端 main 发布，避免本地主 workspace 脏状态影响。
        r = run(["git", "-C", str(PROJECT_ROOT), "fetch", "origin", "main"], timeout=120)
        if not r.ok:
            S.record_attempt_failure(state, f"git fetch: {(r.stderr or r.stdout)[:300]}")
            return state

        # tempfile 已创建目录；git worktree add 要求目标目录不存在或为空。
        shutil.rmtree(worktree, ignore_errors=True)
        r = run(["git", "-C", str(PROJECT_ROOT), "worktree", "add", "--detach", str(worktree), "origin/main"], timeout=120)
        if not r.ok:
            S.record_attempt_failure(state, f"git worktree add: {(r.stderr or r.stdout)[:300]}")
            return state

        target_json = worktree / json_file
        if not target_json.exists():
            S.mark_failed(state, f"origin/main 上找不到 reads JSON: {json_file}")
            return state

        changed = write_audio_meta_to_json(target_json, audio_meta)
        if not changed:
            log.info(f"  [{state['slug']}] origin/main 已包含相同 audio meta，跳过 commit")
            S.advance(state, "published", json_file=str(json_file), publish_status="unchanged")
            return state
        log.info(f"  [{state['slug']}] worktree 写入 audio meta: {json_file}")

        r = run(["git", "-C", str(worktree), "add", str(json_file)], timeout=30)
        if not r.ok:
            S.record_attempt_failure(state, f"git add(worktree): {(r.stderr or r.stdout)[:300]}")
            return state

        # 如果远端已经有同样 audio 字段，不重复 commit，直接视作 published。
        r = run(["git", "-C", str(worktree), "diff", "--cached", "--quiet", "--", str(json_file)], timeout=30)
        if r.rc == 0:
            log.info(f"  [{state['slug']}] origin/main 已包含相同 audio meta，跳过 commit")
            S.advance(state, "published", json_file=str(json_file), publish_status="unchanged")
            return state

        r = run([
            "git", "-C", str(worktree), "commit",
            "-m", f"feat(reads): 加 {state['slug']} 精读播客",
        ], timeout=60)
        if not r.ok:
            S.record_attempt_failure(state, f"git commit(worktree): {(r.stderr or r.stdout)[:300]}")
            return state

        def push_once() -> CmdResult:
            return run(["git", "-C", str(worktree), "push", "origin", "HEAD:main"], timeout=180)

        r = push_once()
        if not r.ok:
            first_err = (r.stderr or r.stdout)[:300]
            log.info(f"  [{state['slug']}] git push 失败，fetch/rebase 后重试一次: {first_err}")
            r_fetch = run(["git", "-C", str(worktree), "fetch", "origin", "main"], timeout=120)
            if not r_fetch.ok:
                S.record_attempt_failure(state, f"git fetch retry: {(r_fetch.stderr or r_fetch.stdout)[:300]}")
                return state
            r_rebase = run(["git", "-C", str(worktree), "rebase", "origin/main"], timeout=120)
            if not r_rebase.ok:
                S.record_attempt_failure(state, f"git rebase retry: {(r_rebase.stderr or r_rebase.stdout)[:300]}")
                return state
            # rebase 后确认目标文件仍含可播放 audio。
            status_after_rebase = run(["git", "-C", str(worktree), "status", "--porcelain", "--", str(json_file)], timeout=30)
            if not status_after_rebase.ok:
                S.record_attempt_failure(state, f"rebase 后 git status 失败: {(status_after_rebase.stderr or status_after_rebase.stdout)[:300]}")
                return state
            try:
                remote_data = json.loads(target_json.read_text(encoding="utf-8"))
                audio = remote_data.get("audio") or {}
                if audio.get("url") != audio_meta.get("url") or not audio.get("duration_seconds"):
                    S.record_attempt_failure(state, "rebase 后 audio meta 丢失，停止 push")
                    return state
            except Exception as e:
                S.record_attempt_failure(state, f"rebase 后校验 audio meta 失败: {e}")
                return state
            r = push_once()
            if not r.ok:
                S.record_attempt_failure(state, f"git push retry: {(r.stderr or r.stdout)[:300]}")
                return state

        commit_short = run(["git", "-C", str(worktree), "rev-parse", "--short", "HEAD"], timeout=30).stdout.strip()
        log.info(f"  [{state['slug']}] uploaded → published ✅ ({commit_short})")
        S.advance(state, "published", json_file=str(json_file), publish_status="pushed", commit=commit_short)
        return state
    finally:
        cleanup_worktree(worktree)


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
        if not dry_run:
            notify_intervention(state, "stuck")
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

    # 如果本轮把任务推进到需要人工介入的状态，立即告警并归档行动日志。
    if state.get("step") in S.INTERVENE_STEPS:
        notify_intervention(state, state.get("step", "unknown"))


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

        if not args.dry_run:
            for state in stuck:
                notify_intervention(state, "stuck")

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
