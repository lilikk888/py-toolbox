#!/usr/bin/env python3
"""查找重复文件（只读，绝不删除任何东西）。

先按文件大小分组，只对大小相同的文件算哈希，速度快很多。

用法:
    python dupes.py D:\\Downloads
    python dupes.py D:\\Downloads --min-size 1     # 只看大于 1MB 的
"""

import argparse
import hashlib
import sys
from collections import defaultdict
from pathlib import Path


def file_hash(path: Path, chunk: int = 1 << 20) -> str:
    """分块读取计算 MD5，避免大文件吃光内存。"""
    h = hashlib.md5()
    with path.open("rb") as f:
        while True:
            data = f.read(chunk)
            if not data:
                break
            h.update(data)
    return h.hexdigest()


def human(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024:
            return f"{n:.1f}{unit}"
        n /= 1024
    return f"{n:.1f}PB"


def main() -> int:
    parser = argparse.ArgumentParser(description="查找重复文件（只读）")
    parser.add_argument("folder", help="要扫描的文件夹")
    parser.add_argument("--min-size", type=float, default=0, help="最小文件大小(MB)，默认 0")
    args = parser.parse_args()

    root = Path(args.folder).expanduser()
    if not root.is_dir():
        print(f"[错误] 不是文件夹: {root}")
        return 1

    min_bytes = int(args.min_size * 1024 * 1024)

    # 第一步：按大小分组
    by_size: dict[int, list[Path]] = defaultdict(list)
    total = 0
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        try:
            size = p.stat().st_size
        except OSError:
            continue
        total += 1
        if size >= min_bytes and size > 0:
            by_size[size].append(p)

    # 第二步：只对大小重复的算哈希
    candidates = {s: paths for s, paths in by_size.items() if len(paths) > 1}
    by_hash: dict[str, list[Path]] = defaultdict(list)
    for paths in candidates.values():
        for p in paths:
            try:
                by_hash[file_hash(p)].append(p)
            except OSError:
                continue

    groups = [paths for paths in by_hash.values() if len(paths) > 1]
    groups.sort(key=lambda g: g[0].stat().st_size * (len(g) - 1), reverse=True)

    if not groups:
        print(f"扫描了 {total} 个文件，没有发现重复。")
        return 0

    wasted = 0
    print(f"扫描 {total} 个文件，发现 {len(groups)} 组重复:\n")
    for i, paths in enumerate(groups, 1):
        size = paths[0].stat().st_size
        extra = size * (len(paths) - 1)
        wasted += extra
        print(f"[{i}] {human(size)} x {len(paths)} 份（可省 {human(extra)}）")
        for p in paths:
            print(f"    {p}")
        print()

    print(f"合计可节省空间: {human(wasted)}")
    print("提示: 本工具只报告，不会删除任何文件。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
