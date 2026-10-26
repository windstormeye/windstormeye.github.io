import contextlib
import io
import os
import random
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image

import convert_webp


def git(cwd, *args):
    return subprocess.run(['git', *args], cwd=cwd, check=True, capture_output=True).stdout.decode()


class ConvertWebpTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        git(self.root, 'init', '-q')
        git(self.root, 'config', 'user.email', 'test@example.com')
        git(self.root, 'config', 'user.name', 'test')
        (self.root / 'source/_posts').mkdir(parents=True)
        cwd = os.getcwd()
        os.chdir(self.root)
        self.addCleanup(os.chdir, cwd)

    def make_photo(self, relative, size=(320, 240)):
        # 带噪点的渐变，接近照片，WebP 一定比 PNG/JPEG 小
        rng = random.Random(relative)
        image = Image.new('RGB', size)
        image.putdata([((x * 255) // size[0], (y * 255) // size[1], rng.randrange(256))
                       for y in range(size[1]) for x in range(size[0])])
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        # 相机/手机导出的 JPEG 通常在 90 以上
        image.save(path, quality=95)
        return path

    def write(self, relative, text):
        path = self.root / relative
        path.write_text(text, encoding='utf-8')
        return path

    def run_main(self, env=None):
        with patch.dict(os.environ, env or {}), contextlib.redirect_stdout(io.StringIO()):
            return convert_webp.main()

    def staged(self):
        return set(git(self.root, 'diff', '--cached', '--name-only').split())

    def test_new_image_converted_and_reference_updated(self):
        self.make_photo('source/images/2026/a.png')
        post = self.write('source/_posts/a.md', '![](../images/2026/a.png)\n')
        git(self.root, 'add', '.')

        self.assertEqual(self.run_main(), 0)
        self.assertFalse((self.root / 'source/images/2026/a.png').exists())
        with Image.open(self.root / 'source/images/2026/a.webp') as image:
            self.assertEqual((image.format, image.size), ('WEBP', (320, 240)))
        self.assertEqual(post.read_text(encoding='utf-8'), '![](../images/2026/a.webp)\n')
        self.assertEqual(self.staged(), {'source/images/2026/a.webp', 'source/_posts/a.md'})
        self.assertEqual(git(self.root, 'diff', '--name-only'), '')

    def test_url_encoded_chinese_path(self):
        self.make_photo('source/images/济州 岛.jpg')
        post = self.write('source/_posts/b.md', '![](/images/%E6%B5%8E%E5%B7%9E%20%E5%B2%9B.jpg)\n')
        git(self.root, 'add', '.')

        self.assertEqual(self.run_main(), 0)
        self.assertTrue((self.root / 'source/images/济州 岛.webp').exists())
        self.assertEqual(post.read_text(encoding='utf-8'), '![](/images/%E6%B5%8E%E5%B7%9E%20%E5%B2%9B.webp)\n')

    def test_unstaged_markdown_aborts_without_changes(self):
        self.make_photo('source/images/c.png')
        post = self.write('source/_posts/c.md', '![](/images/c.png)\n')
        git(self.root, 'add', '.')
        post.write_text('![](/images/c.png)\n还没暂存的段落\n', encoding='utf-8')

        self.assertEqual(self.run_main(), 1)
        self.assertTrue((self.root / 'source/images/c.png').exists())
        self.assertFalse((self.root / 'source/images/c.webp').exists())

    def test_published_image_is_not_converted(self):
        self.make_photo('source/images/d.png')
        git(self.root, 'add', '.')
        git(self.root, 'commit', '-qm', 'init')
        self.make_photo('source/images/d.png', size=(300, 200))
        git(self.root, 'add', '.')

        self.assertEqual(self.run_main(), 0)
        self.assertTrue((self.root / 'source/images/d.png').exists())
        self.assertFalse((self.root / 'source/images/d.webp').exists())

    def test_site_icons_keep_their_format(self):
        self.make_photo('source/apple-touch-icon.png', size=(180, 180))
        git(self.root, 'add', '.')

        self.assertEqual(self.run_main(), 0)
        self.assertTrue((self.root / 'source/apple-touch-icon.png').exists())
        self.assertEqual(self.staged(), {'source/apple-touch-icon.png'})

    def test_skip_env(self):
        self.make_photo('source/images/e.png')
        git(self.root, 'add', '.')

        self.assertEqual(self.run_main({'SKIP_WEBP': '1'}), 0)
        self.assertTrue((self.root / 'source/images/e.png').exists())

    def test_untracked_markdown_updated_but_not_staged(self):
        self.make_photo('source/images/f.png')
        git(self.root, 'add', 'source/images/f.png')
        draft = self.write('source/_posts/f.md', '![](../images/f.png)\n')

        self.assertEqual(self.run_main(), 0)
        self.assertEqual(draft.read_text(encoding='utf-8'), '![](../images/f.webp)\n')
        self.assertEqual(self.staged(), {'source/images/f.webp'})


if __name__ == '__main__':
    unittest.main()
