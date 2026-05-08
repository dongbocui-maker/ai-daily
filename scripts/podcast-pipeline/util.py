"""
podcast-pipeline/util.py — 共享工具：subprocess 包装 + retry + 日志

设计：所有外部调用（NotebookLM CLI、git、COS）都包一层带超时和 stderr 捕获的
run() helper，方便 worker 上报失败原因。
"""
from __future__ import annotations
import os
import sys
import subprocess
import logging
from pathlib import Path
from typing import Optional


LOG_DIR = Path("/root/.openclaw/workspace/projects/ai-daily/state/podcasts/.logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)


def get_logger(name: str = "pipeline") -> logging.Logger:
    """统一 logger，每个组件一份日志文件"""
    log = logging.getLogger(name)
    if log.handlers:
        return log
    log.setLevel(logging.INFO)

    # File handler
    fh = logging.FileHandler(LOG_DIR / f"{name}.log", encoding="utf-8")
    fh.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    ))
    log.addHandler(fh)

    # Stderr handler
    sh = logging.StreamHandler(sys.stderr)
    sh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s",
                                      datefmt="%H:%M:%S"))
    log.addHandler(sh)
    return log


class CmdResult:
    def __init__(self, rc: int, stdout: str, stderr: str, duration: float):
        self.rc = rc
        self.stdout = stdout
        self.stderr = stderr
        self.duration = duration

    @property
    def ok(self) -> bool:
        return self.rc == 0


def run(
    cmd: list[str],
    timeout: int = 60,
    env_extra: Optional[dict[str, str]] = None,
    input_data: Optional[str] = None,
) -> CmdResult:
    """运行命令，捕获 stdout/stderr/rc。不抛异常——让调用方判断"""
    import time
    env = os.environ.copy()
    if env_extra:
        env.update(env_extra)

    t0 = time.time()
    try:
        p = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
            input=input_data,
        )
        return CmdResult(p.returncode, p.stdout, p.stderr, time.time() - t0)
    except subprocess.TimeoutExpired as e:
        return CmdResult(
            124,
            (e.stdout or b"").decode("utf-8", errors="replace") if isinstance(e.stdout, bytes) else (e.stdout or ""),
            f"[timeout after {timeout}s] {(e.stderr or b'').decode('utf-8', errors='replace') if isinstance(e.stderr, bytes) else (e.stderr or '')}",
            time.time() - t0,
        )
    except FileNotFoundError as e:
        return CmdResult(127, "", str(e), time.time() - t0)


# ===================== NotebookLM CLI 封装 =====================

NOTEBOOKLM_BIN = "/root/.openclaw/workspace/projects/ai-fireside/.venv/bin/notebooklm"
PROXY = "http://127.0.0.1:7890"
PROXY_ENV = {"HTTPS_PROXY": PROXY, "HTTP_PROXY": PROXY}


def ensure_mihomo() -> None:
    """确保代理在跑"""
    r = run(["pgrep", "mihomo"], timeout=5)
    if r.ok and r.stdout.strip():
        return
    # 起 mihomo
    log = get_logger("worker")
    log.info("启动 mihomo")
    subprocess.Popen(
        ["/usr/local/bin/mihomo", "-d", "/root/.config/mihomo"],
        stdout=open("/root/.config/mihomo/mihomo.log", "a"),
        stderr=subprocess.STDOUT,
    )
    import time
    time.sleep(3)


def nblm(*args, timeout: int = 60) -> CmdResult:
    """调用 notebooklm CLI"""
    return run([NOTEBOOKLM_BIN, *args], timeout=timeout, env_extra=PROXY_ENV)


def nblm_json(*args, timeout: int = 60) -> tuple[CmdResult, dict | list | None]:
    """调用并解析 JSON 输出"""
    import json
    r = nblm(*args, timeout=timeout)
    parsed = None
    if r.ok and r.stdout.strip():
        try:
            parsed = json.loads(r.stdout)
        except json.JSONDecodeError:
            pass
    return r, parsed
