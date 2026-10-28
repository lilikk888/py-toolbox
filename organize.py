#!/usr/bin/env python3
"""按文件类型整理文件夹。

默认只预览，不会移动任何文件。加 --apply 才真的动手。

用法:
    python organize.py D:\\Downloads              # 预览
    python organize.py D:\\Downloads --apply      # 真的整理
"""

import argparse
import shutil
import sys
from pathlib import Path

# 扩展名 -> 目标文件夹
CATEGORIES = {
    "图片": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".ico", ".heic"},
    "视频": {".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm"},
    "音频": {".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"},
    "文档": {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".md", ".csv"},
    "压缩包": {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"},
    "安装包": {".exe", ".msi", ".dmg", ".pkg", ".apk"},
    "代码": {".py", ".js", ".ts", ".html", ".css", ".json", ".yaml", ".yml", ".java", ".go", ".rs", ".c", ".cpp", ".h"},
}

# 反查表: .jpg -> 图片
EXT_TO_CATEGORY = {}
for _cat, _exts in CATEGORIES.items():
    for _ext in _exts:
        EXT_TO_CATEGORY[_ext] = _cat


def build_plan(root: Path) -> list[tuple[Path, Path]]:
    """返回 [(源文件, 目标路径), ...]"""
    plan = []
    for item in root.iterdir():
        if not item.is_file():
            continue  # 跳过子文件夹
        if item.name.startswith("."):
            continue  # 跳过隐藏文件
        category = EXT_TO_CATEGORY.get(item.suffix.lower())
        if category is None:
            continue  # 不认识的类型不处理
        target = root / category / item.name
        if target.exists():
            # 重名时加序号, 避免覆盖
            stem, suffix = item.stem, item.suffix
            i = 1
            while target.exists():
                target = root / category / f"{stem} ({i}){suffix}"
                i += 1
        plan.append((item, target))
    return plan


def main() -> int:
    parser = argparse.ArgumentParser(description="按文件类型整理文件夹（默认只预览）")
    parser.add_argument("folder", help="要整理的文件夹路径")
    parser.add_argument("--apply", action="store_true", help="真的执行移动（不加则只预览）")
    args = parser.parse_args()

    root = Path(args.folder).expanduser()
    if not root.is_dir():
        print(f"[错误] 不是文件夹: {root}")
        return 1

    plan = build_plan(root)
    if not plan:
        print("没有需要整理的文件。")
        return 0

    print(f"{'[执行]' if args.apply else '[预览]'} 共 {len(plan)} 个文件:\n")
    for src, dst in plan:
        print(f"  {src.name}  ->  {dst.parent.name}/{dst.name}")

    if not args.apply:
        print("\n以上仅为预览。确认无误后加 --apply 参数真正执行。")
        return 0

    moved = 0
    for src, dst in plan:
        dst.parent.mkdir(exist_ok=True)
        try:
            shutil.move(str(src), str(dst))
            moved += 1
        except OSError as e:
            print(f"[跳过] {src.name}: {e}")

    print(f"\n完成，成功移动 {moved} 个文件。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
