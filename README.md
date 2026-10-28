# py-toolbox

几个日常真用得上的小脚本。**纯 Python 标准库，零依赖**，不用 `pip install` 任何东西。

设计原则：**默认只预览，不动你的文件**。所有会修改文件的脚本，都必须手动加 `--apply` 才真正执行。

## 脚本清单

| 脚本 | 作用 | 会改文件吗 |
|---|---|---|
| `organize.py` | 按类型（图片/文档/视频…）把文件夹里的文件分类归位 | 加 `--apply` 才会 |
| `dupes.py` | 找出重复文件，算出能省多少空间 | 不会，只读 |
| `bigfiles.py` | 列出文件夹里最占空间的 N 个文件 | 不会，只读 |
| `rename.py` | 批量重命名：加前缀 / 替换文字 / 加序号 | 加 `--apply` 才会 |

## 用法

需要 Python 3.8 以上。

```bash
# 看看下载文件夹能整理成什么样（预览，安全）
python organize.py ~/Downloads

# 确认没问题，真的整理
python organize.py ~/Downloads --apply

# 下载文件夹里有多少重复文件
python dupes.py ~/Downloads

# 只看大于 10MB 的重复文件
python dupes.py ~/Downloads --min-size 10

# C 盘最占空间的 30 个文件
python bigfiles.py / --top 30

# 只找视频和镜像文件
python bigfiles.py / --ext mp4,iso

# 给照片加统一前缀（先预览）
python rename.py ./photos --prefix 2026旅行_

# 确认后执行
python rename.py ./photos --prefix 2026旅行_ --apply
```

Windows 下路径用反斜杠并加引号：

```bash
python organize.py "D:\Downloads" --apply
```

## 为什么默认不删东西

整理文件最怕手滑。这些脚本的规则是：

- 只读操作（`dupes.py`、`bigfiles.py`）永远不会碰文件
- 写操作（`organize.py`、`rename.py`）默认只打印计划，加 `--apply` 才动手
- 遇到同名文件自动加序号 `(1)`，不覆盖
- 不认识的扩展名一律不动
- `dupes.py` 只报告重复文件，**不提供删除功能**

## License

MIT
