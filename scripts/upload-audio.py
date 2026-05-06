#!/usr/bin/env python3
"""
upload-audio.py — 上传音频到腾讯云 COS（香港桶）

支持两种模式：
  - 日报模式：--mode daily --date YYYY-MM-DD
      key: audio/daily/YYYY-MM-DD/daily.{ext}
  - 精读模式：--mode reads --slug <slug>
      key: audio/reads/<slug>.{ext}

自动识别 mp3 / m4a，设置正确的 Content-Type。

用法：
  source /root/.config/cos/credentials.env
  python3 upload-audio.py <本地音频路径> --mode daily --date 2026-05-06
  python3 upload-audio.py <本地音频路径> --mode reads --slug karpathy-agi-decade-away

输出（JSON 单行，stdout）：
  {
    "url": "https://...",
    "key": "audio/reads/<slug>.m4a",
    "size_bytes": ...,
    "duration_seconds": ...,
    "format": "m4a",
    "etag": "...",
    "uploaded_at": "2026-05-06T..."
  }

返回码：0 成功 / 1 失败
"""
import os
import sys
import json
import argparse
import subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path

try:
    from qcloud_cos import CosConfig, CosS3Client
    from qcloud_cos.cos_exception import CosClientError, CosServiceError
except ImportError:
    print("ERROR: 缺少依赖 cos-python-sdk-v5。安装：pip3 install cos-python-sdk-v5", file=sys.stderr)
    sys.exit(1)

# ===== 配置 =====
REGION = "ap-hongkong"
BUCKET = "ai-daily-audio-1302925971"
DOMAIN = f"https://{BUCKET}.cos.{REGION}.myqcloud.com"
TZ_SH = timezone(timedelta(hours=8))

# 文件后缀 -> Content-Type 映射
CONTENT_TYPES = {
    ".mp3": "audio/mpeg",
    ".m4a": "audio/mp4",
    ".aac": "audio/aac",
    ".ogg": "audio/ogg",
    ".wav": "audio/wav",
}


def probe_duration(path: str) -> float:
    """用 ffprobe 探测音频时长（秒，浮点）"""
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", path],
            capture_output=True, text=True, check=True, timeout=30,
        )
        return round(float(result.stdout.strip()), 2)
    except (subprocess.CalledProcessError, ValueError, subprocess.TimeoutExpired) as e:
        print(f"WARN: ffprobe 失败：{e}", file=sys.stderr)
        return 0.0


def build_key(mode: str, date_str: str | None, slug: str | None, ext: str) -> str:
    """根据模式生成 COS 对象 key"""
    if mode == "daily":
        if not date_str:
            date_str = datetime.now(TZ_SH).strftime("%Y-%m-%d")
        return f"audio/daily/{date_str}/daily{ext}"
    elif mode == "reads":
        if not slug:
            raise ValueError("--mode reads 需要 --slug")
        return f"audio/reads/{slug}{ext}"
    else:
        raise ValueError(f"Unknown mode: {mode}")


def upload(
    local_path: str,
    mode: str = "daily",
    date_str: str | None = None,
    slug: str | None = None,
) -> dict:
    # 凭据从环境变量读（必须先 source credentials.env）
    secret_id = os.environ.get("SECRET_ID")
    secret_key = os.environ.get("SECRET_KEY")
    if not secret_id or not secret_key:
        raise RuntimeError("ERROR: 环境变量 SECRET_ID / SECRET_KEY 未设置。先 `source /root/.config/cos/credentials.env`")

    local_path = str(Path(local_path).expanduser().resolve())
    if not os.path.exists(local_path):
        raise FileNotFoundError(f"本地文件不存在：{local_path}")

    # 检测文件后缀 + Content-Type
    ext = Path(local_path).suffix.lower()
    if ext not in CONTENT_TYPES:
        raise ValueError(f"不支持的音频格式：{ext}。支持：{list(CONTENT_TYPES.keys())}")
    content_type = CONTENT_TYPES[ext]

    # 根据模式生成 key
    key = build_key(mode, date_str, slug, ext)

    # 探测时长 + 大小
    duration = probe_duration(local_path)
    size = os.path.getsize(local_path)

    # 配置 COS 客户端
    config = CosConfig(Region=REGION, SecretId=secret_id, SecretKey=secret_key)
    client = CosS3Client(config)

    # 上传（高级 upload_file自动处理大文件分片）
    # 重试策略：最多 4 次，指数退避（60MB+ 文件首次上传偶发失败）
    import time
    MAX_RETRIES = 4
    BACKOFF_BASE = 5  # 第 i 次重试前 sleep BACKOFF_BASE * 2^(i-1)。 0s、5s、10s、20s

    last_exc = None
    response = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            if attempt > 1:
                wait = BACKOFF_BASE * (2 ** (attempt - 2))
                print(f"  ⏳ 重试上传（第 {attempt}/{MAX_RETRIES} 次，等 {wait}s）...", file=sys.stderr)
                time.sleep(wait)

            response = client.upload_file(
                Bucket=BUCKET,
                Key=key,
                LocalFilePath=local_path,
                EnableMD5=False,
                ContentType=content_type,
                CacheControl="public, max-age=86400",  # 浏览器缓存 1 天（音频不变）
            )
            if attempt > 1:
                print(f"  ✅ 第 {attempt} 次重试成功", file=sys.stderr)
            break
        except (CosClientError, CosServiceError) as e:
            last_exc = e
            print(f"  ⚠️  第 {attempt} 次上传失败：{e}", file=sys.stderr)
            if attempt == MAX_RETRIES:
                raise RuntimeError(f"COS 上传失败（已重试 {MAX_RETRIES} 次）：{e}") from e

    if response is None:
        raise RuntimeError(f"COS 上传完全失败：{last_exc}")
    etag = response.get("ETag", "")

    return {
        "url": f"{DOMAIN}/{key}",
        "key": key,
        "size_bytes": size,
        "duration_seconds": duration,
        "format": ext.lstrip("."),
        "etag": etag,
        "uploaded_at": datetime.now(TZ_SH).isoformat(timespec="seconds"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="上传音频到腾讯云 COS")
    parser.add_argument("local_path", help="本地音频文件路径（mp3 / m4a / aac 等）")
    parser.add_argument("--mode", choices=["daily", "reads"], default="daily", help="上传模式")
    parser.add_argument("--date", help="daily 模式下的日期 YYYY-MM-DD（默认今天）", default=None)
    parser.add_argument("--slug", help="reads 模式下的精读 slug", default=None)
    parser.add_argument("--quiet", action="store_true", help="只输出 JSON 不打日志")
    args = parser.parse_args()

    try:
        result = upload(
            args.local_path,
            mode=args.mode,
            date_str=args.date,
            slug=args.slug,
        )
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
        return 1

    if not args.quiet:
        print(f"✅ 上传成功：{result['url']}", file=sys.stderr)
        print(f"   格式：{result['format']:4s} | 大小：{result['size_bytes'] / 1024 / 1024:.2f} MB | 时长：{int(result['duration_seconds'])}s ({result['duration_seconds'] / 60:.1f} 分钟)", file=sys.stderr)

    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
