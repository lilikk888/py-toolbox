#!/usr/bin/env python3
"""找出文件夹里最大的 N 个文件（只读）。

用法:
    python bigfiles.py D:\\                     # 默认前 20 个
    python bigfiles.py D:\\ --top 50
    python bigfiles.py D:\\ --ext mp4,iso       # 只看指定类型
"""

import argparse
import sys
from pathlib import Path


def human(n: float) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024:
            return f"{n:.1f}{unit}"
        n /= 1024
    return f"{n:.1f}PB"


def main() -> int:
    parser = argparse.ArgumentParser(description="找出最大的文件（只读）")
    parser.add_argument("folder", help="要扫描的文件夹")
    parser.add_argument("--top", type=int, default=20, help="显示前几个，默认 20")
    parser.add_argument("--ext", default="", help="只看指定扩展名，逗号分隔，如 mp4,iso")
    args = parser.parse_args()

    root = Path(args.folder).expanduser()
    if not root.is_dir():
        print(f"[错误] 不是文件夹: {root}")
        return 1

    exts = {("." + e.strip().lstrip(".")).lower() for e in args.ext.split(",") if e.strip()}

    files = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if exts and p.suffix.lower() not in exts:
            continue
        try:
            files.append((p.stat().st_size, p))
        except OSError:
            continue

    if not files:
        print("没有找到文件。")
        return 0

    files.sort(reverse=True)
    total = sum(s for s, _ in files)
    shown = files[: args.top]

    print(f"共 {len(files)} 个文件，总计 {human(total)}\n")
    print(f"{'大小':>10}  {'占总量':>7}  路径")
    print("-" * 70)
    for size, p in shown:
        print(f"{human(size):>10}  {size / total * 100:>6.1f}%  {p}")

    print("-" * 70)
    print(f"前 {len(shown)} 个合计 {human(sum(s for s, _ in shown))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
