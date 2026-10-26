"""pre-commit 用：把本次新增的 jpg/png 转成 WebP，并把文章里的引用改成 .webp。

- 只处理新增（git 状态为 A）的 source/images/ 下的文章图片，已经发布过的图片不动，避免老链接失效；
  favicon、apple-touch-icon 这类必须保持原格式的文件不在这个目录里。
- WebP 比原图大（例如很小的图标）时保留原图。
- 引用这些图片的 Markdown 如果还有未暂存的修改，会中止提交，避免把别的改动一起带进来。
- 设置环境变量 SKIP_WEBP=1 可以跳过转换。
"""
import os
import subprocess
import sys
from urllib.parse import quote

from PIL import Image, ImageOps

CONVERTIBLE = ('.jpg', '.jpeg', '.png')
TEXT_DIRS = ('source', 'draft')
JPEG_QUALITY = 82
PNG_QUALITY = 90


def git(*args, check=True):
    return subprocess.run(['git', *args], check=check, capture_output=True)


def git_paths(*args):
    output = git(*args).stdout.decode('utf-8')
    return [path for path in output.split('\0') if path]


def added_images():
    return [path for path in git_paths('diff', '--cached', '--name-only', '--diff-filter=A', '-z')
            if path.startswith('source/images/') and path.lower().endswith(CONVERTIBLE) and os.path.isfile(path)]


def markdown_files():
    return [path for path in git_paths('ls-files', '-z', '--cached', '--others', '--exclude-standard', '--', *TEXT_DIRS)
            if path.endswith('.md') and os.path.isfile(path)]


def is_tracked(path):
    return git('ls-files', '--error-unmatch', '--', path, check=False).returncode == 0


def has_unstaged_changes(path):
    return git('diff', '--quiet', '--', path, check=False).returncode != 0


def webp_path(path):
    return os.path.splitext(path)[0] + '.webp'


def references(path):
    # 文章里的写法有 ../images/x.png、/images/x.png 以及 URL 编码后的中文路径
    site_path = path[len('source/'):]
    return [site_path, quote(site_path)]


def convert(path):
    target = webp_path(path)
    with Image.open(path) as source:
        if getattr(source, 'is_animated', False):
            return None
        image = ImageOps.exif_transpose(source)
        has_alpha = image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info)
        image = image.convert('RGBA' if has_alpha else 'RGB')
        quality = PNG_QUALITY if path.lower().endswith('.png') else JPEG_QUALITY
        # 不写入 EXIF，顺带去掉照片里的 GPS 等信息
        image.save(target, 'WEBP', quality=quality, method=6)
    if os.path.getsize(target) >= os.path.getsize(path):
        os.remove(target)
        return None
    return target


def main():
    if os.environ.get('SKIP_WEBP') == '1':
        return 0

    images = [path for path in added_images() if not os.path.exists(webp_path(path))]
    if not images:
        return 0

    texts = {}
    for markdown in markdown_files():
        with open(markdown, encoding='utf-8') as file:
            content = file.read()
        if any(ref in content for image in images for ref in references(image)):
            texts[markdown] = content

    dirty = [markdown for markdown in texts if is_tracked(markdown) and has_unstaged_changes(markdown)]
    if dirty:
        print('错误：以下文章引用了新图片，但还有未暂存的修改，请先 git add 后再提交：')
        for markdown in dirty:
            print('  ' + markdown)
        return 1

    converted = []
    for image in images:
        target = convert(image)
        if not target:
            print(f'保留原图（WebP 没有更小）: {image}')
            continue
        before, after = os.path.getsize(image), os.path.getsize(target)
        print(f'转成 WebP: {image} ({before / 1024:.0f} KB -> {after / 1024:.0f} KB)')
        git('rm', '--cached', '--quiet', '--', image)
        os.remove(image)
        git('add', '--', target)
        converted.append(image)

    for markdown, content in texts.items():
        updated = content
        for image in converted:
            for old, new in zip(references(image), references(webp_path(image))):
                updated = updated.replace(old, new)
        if updated == content:
            continue
        with open(markdown, 'w', encoding='utf-8') as file:
            file.write(updated)
        if is_tracked(markdown):
            git('add', '--', markdown)
            print(f'已更新引用: {markdown}')
        else:
            print(f'已更新引用（文件未加入 git，未暂存）: {markdown}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
