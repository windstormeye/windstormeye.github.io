# 图片处理 Git hook

在仓库根目录安装依赖并启用 hook（每个 clone 执行一次）：

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r tools/requirements.txt
git config core.hooksPath tools/git-hooks
```

`PIL` 是 Pillow 提供的模块。hook 优先使用 `.venv/bin/python`，无需手动激活虚拟环境；没有 `.venv` 时使用 PATH 中的 `python3`。虚拟环境已加入 `.gitignore`。

提交包含新增或修改的图片时，hook 会检查图片大小，保持 JPG、PNG、GIF 等原格式和文件名，不再自动转换为 WebP，也不改写文章引用。纯文字提交不需要图片处理依赖。

大小上限为 **500 KB（500,000 字节）**。超限图片循环缩小尺寸，JPG 同时逐步降低质量，直到达到上限；已达标图片保持原样。GIF 会保留动画。压缩失败或无法达到上限时，保留原文件并阻止提交。

旧的 WebP 转换脚本已移除，提交时无需设置 `SKIP_WEBP`。hook 仅压缩新增或修改的图片，不转换图片格式。

运行图片处理测试：

```sh
.venv/bin/python -m unittest discover -s tools -p 'test_*.py'
```
