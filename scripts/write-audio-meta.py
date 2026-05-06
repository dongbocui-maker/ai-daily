#!/usr/bin/env python3
"""
write-audio-meta.py — 把 upload-audio.py 输出的元数据写回 JSON

支持两种目标：
  - 日报：--mode daily --date YYYY-MM-DD → src/data/daily/YYYY-MM-DD.json
  - 精读：--mode reads --slug <slug>      → src/data/reads/{savedDate}-{slug}.json

用法：
  # 方式 1：从 stdin 接收 upload-audio.py 输出的 JSON
  python3 upload-audio.py /tmp/audio.m4a --mode reads --slug karpathy-agi-decade-away \
    | python3 write-audio-meta.py --mode reads --slug karpathy-agi-decade-away

  # 方式 2：通过 --meta-file 传入 JSON 文件
  python3 write-audio-meta.py --mode reads --slug xxx --meta-file /tmp/meta.json

输出（stderr）：✅ 写入成功提示
返回码：0 成功 / 1 失败

关键设计：
  - 原子写：先写 .tmp 再 os.replace 到目标
  - 校验：目标 JSON 必须已存在（不会替你兜底创建）
  - 字段：保留 url / duration_seconds / size_bytes / generated_at + format
"""
import os
import sys
import json
import argparse
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DAILY_DIR = PROJECT_ROOT / "src" / "data" / "daily"
READS_DIR = PROJECT_ROOT / "src" / "data" / "reads"

REQUIRED_KEYS = {"url", "duration_seconds", "size_bytes", "uploaded_at"}


def find_reads_json(slug: str) -> Path:
    """精读 JSON 文件名是 {savedDate}-{slug}.json，按 slug 后缀匹配"""
    candidates = list(READS_DIR.glob(f"*-{slug}.json"))
    if not candidates:
        raise FileNotFoundError(f"找不到精读 JSON：slug={slug}（在 {READS_DIR} 下没有 *-{slug}.json）")
    if len(candidates) > 1:
        raise RuntimeError(f"找到多个匹配的精读 JSON（slug 重复？）：{candidates}")
    return candidates[0]


def write_meta(mode: str, meta: dict, date: str | None = None, slug: str | None = None) -> dict:
    # 校验输入
    missing = REQUIRED_KEYS - set(meta.keys())
    if missing:
        raise ValueError(f"upload-audio.py 输出缺少字段：{missing}")

    # 定位目标 JSON
    if mode == "daily":
        if not date:
            raise ValueError("--mode daily 需要 --date")
        target = DAILY_DIR / f"{date}.json"
    elif mode == "reads":
        if not slug:
            raise ValueError("--mode reads 需要 --slug")
        target = find_reads_json(slug)
    else:
        raise ValueError(f"Unknown mode: {mode}")

    if not target.exists():
        raise FileNotFoundError(f"目标 JSON 不存在：{target}")

    # 读现有 JSON
    with target.open("r", encoding="utf-8") as f:
        data = json.load(f)

    # 构造 audio 字段（精简：只保留前端要用的）
    audio_block = {
        "url": meta["url"],
        "duration_seconds": meta["duration_seconds"],
        "size_bytes": meta["size_bytes"],
        "generated_at": meta["uploaded_at"],
    }
    if "format" in meta:
        audio_block["format"] = meta["format"]

    data["audio"] = audio_block

    # 原子写：tmp + replace
    tmp_fd, tmp_path = tempfile.mkstemp(
        prefix=f".{target.stem}.", suffix=".tmp", dir=str(target.parent)
    )
    try:
        with os.fdopen(tmp_fd, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
        os.replace(tmp_path, target)
    except Exception:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise

    return {"target": str(target.relative_to(PROJECT_ROOT)), "audio": audio_block}


def main() -> int:
    parser = argparse.ArgumentParser(description="把音频元数据写回 JSON")
    parser.add_argument("--mode", choices=["daily", "reads"], default="daily")
    parser.add_argument("--date", help="daily 模式下的日期 YYYY-MM-DD")
    parser.add_argument("--slug", help="reads 模式下的精读 slug")
    parser.add_argument("--meta-file", help="meta JSON 文件路径（不指定则从 stdin 读）")
    args = parser.parse_args()

    try:
        if args.meta_file:
            with open(args.meta_file, "r", encoding="utf-8") as f:
                meta = json.load(f)
        else:
            stdin_data = sys.stdin.read().strip()
            if not stdin_data:
                print("ERROR: stdin 为空。请 pipe upload-audio.py 输出，或用 --meta-file。", file=sys.stderr)
                return 1
            meta = json.loads(stdin_data)

        if "error" in meta:
            print(f"ERROR: 上游返回错误：{meta['error']}", file=sys.stderr)
            return 1

        result = write_meta(args.mode, meta, date=args.date, slug=args.slug)
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    except (ValueError, json.JSONDecodeError) as e:
        print(f"ERROR: 输入解析/校验失败：{e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"ERROR: 写入失败：{e}", file=sys.stderr)
        return 1

    audio = result["audio"]
    print(f"✅ 已写入 {result['target']}", file=sys.stderr)
    print(f"   url: {audio['url']}", file=sys.stderr)
    print(f"   时长 {int(audio['duration_seconds'])}s ({audio['duration_seconds'] / 60:.1f} 分钟)"
          f" | 大小 {audio['size_bytes'] / 1024 / 1024:.2f} MB"
          f" | 格式 {audio.get('format', 'mp3')}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
