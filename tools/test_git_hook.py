import os
from pathlib import Path
import random
import shutil
import subprocess
import sys
import tempfile
import unittest

from PIL import Image


class ImageHookTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix='blog hook ')
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.env = dict(os.environ, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM='1')
        source = Path(__file__).parent
        (self.root / 'tools/git-hooks').mkdir(parents=True)
        shutil.copy2(source / 'compress_images.py', self.root / 'tools/compress_images.py')
        shutil.copy2(source / 'git-hooks/pre-commit', self.root / 'tools/git-hooks/pre-commit')
        (self.root / '.venv').symlink_to(sys.prefix, target_is_directory=True)
        self.git('init', '-q')
        self.git('config', 'user.name', 'Hook test')
        self.git('config', 'user.email', 'hook-test@example.invalid')
        self.git('config', 'core.hooksPath', 'tools/git-hooks')
        self.git('config', 'commit.gpgsign', 'false')
        (self.root / 'source/images').mkdir(parents=True)

    def git(self, *args, check=True):
        return subprocess.run(['git', *args], cwd=self.root, env=self.env,
                              capture_output=True, text=True, check=check)

    def test_commit_compresses_jpg_and_png_without_webp_or_reference_changes(self):
        photo = self.root / 'source/images/photo.jpg'
        png = self.root / 'source/images/透明 图片.png'
        Image.frombytes('RGB', (1600, 1200), random.Random(0).randbytes(1600 * 1200 * 3)).save(photo, quality=98)
        Image.frombytes('RGBA', (800, 600), random.Random(1).randbytes(800 * 600 * 4)).save(png)
        post = self.root / 'post.md'
        content = '![](/images/photo.jpg)\n![](/images/透明 图片.png)\n'
        post.write_text(content, encoding='utf-8')
        self.git('add', 'source', 'post.md')
        result = self.git('commit', '-qm', 'images', check=False)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        for path, expected in [(photo, 'JPEG'), (png, 'PNG')]:
            self.assertLessEqual(path.stat().st_size, 500_000)
            with Image.open(path) as image:
                self.assertEqual(image.format, expected)
                if expected == 'PNG':
                    self.assertIn('A', image.getbands())
        self.assertFalse(list(self.root.rglob('*.webp')))
        self.assertEqual(post.read_text(encoding='utf-8'), content)
        self.assertEqual(self.git('diff', 'HEAD', '--name-only').stdout, '')

    def test_compression_failure_blocks_commit(self):
        broken = self.root / 'source/images/broken.jpg'
        content = b'invalid image' * 50_000
        broken.write_bytes(content)
        self.git('add', 'source')
        result = self.git('commit', '-qm', 'must fail', check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(broken.read_bytes(), content)
        self.assertNotEqual(self.git('rev-parse', '--verify', 'HEAD', check=False).returncode, 0)


if __name__ == '__main__':
    unittest.main()
