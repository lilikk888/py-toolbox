#!/usr/bin/env python3
"""批量重命名文件（默认只预览）。

支持三种操作，可以组合使用：
    --prefix 前缀     给文件名加前缀
    --replace 旧=新    替换文件名中的文字
    --number          在末尾加连续序号 _001 _002 ...

用法:
    python rename.py ./photos --prefix 2026_                  # 预览
    python rename.py ./photos --prefix 2026_ --apply          # 执行
    python rename.py ./photos --replace IMG_=旅行_ --apply
"""

import argparse
import sys
from pathlib import Path


def build_new_name(name: str, index: int, args) -> str:
    p = Path(name)
    stem, suffix = p.stem, p.suffix

    if args.replace:
        old, new = args.replace.split("=", 1)
        stem = stem.replace(old, new)

    if args.prefix:
        stem = args.prefix + stem

    if args.number:
        stem = f"{stem}_{index:03d}"

    return stem + suffix


def main() -> int:
    parser = argparse.ArgumentParser(description="批量重命名（默认只预览）")
    parser.add_argument("folder", help="要处理的文件夹")
    parser.add_argument("--prefix", default="", help="给文件名加前缀")
    parser.add_argument("--replace", default="", help="替换文字，格式 旧=新")
    parser.add_argument("--number", action="store_true", help="末尾加连续序号")
    parser.add_argument("--apply", action="store_true", help="真的执行（不加则只预览）")
    args = parser.parse_args()

    if not (args.prefix or args.replace or args.number):
        print("至少指定一个操作：--prefix / --replace / --number")
        return 1

    root = Path(args.folder).expanduser()
    if not root.is_dir():
        print(f"[错误] 不是文件夹: {root}")
        return 1

    files = sorted(p for p in root.iterdir() if p.is_file())
    if not files:
        print("文件夹里没有文件。")
        return 0

    plan = []
    for i, f in enumerate(files, 1):
        new_name = build_new_name(f.name, i, args)
        if new_name != f.name:
            plan.append((f, f.with_name(new_name)))

    if not plan:
        print("文件名没有需要变化的地方。")
        return 0

    print(f"{'[执行]' if args.apply else '[预览]'} 共 {len(plan)} 个文件:\n")
    for src, dst in plan:
        print(f"  {src.name}")
        print(f"    -> {dst.name}")

    if not args.apply:
        print("\n以上仅为预览。确认无误后加 --apply 参数真正执行。")
        return 0

    done = 0
    for src, dst in plan:
        if dst.exists():
            print(f"[跳过] {dst.name} 已存在")
            continue
        try:
            src.rename(dst)
            done += 1
        except OSError as e:
            print(f"[失败] {src.name}: {e}")

    print(f"\n完成，成功重命名 {done} 个文件。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
