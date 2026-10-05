import contextlib
import hashlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image, ImageChops, ImageDraw, ImageSequence
import compress_images


class GifCompressionTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)

    def make_gif(self, disposal=2, loop=3):
        frames = []
        for x in [5, 15, 25, 35, 45, 55]:
            frame = Image.new('RGBA', (96, 80), (0, 0, 0, 0))
            draw = ImageDraw.Draw(frame)
            draw.rectangle((x, 15, x + 16, 45), fill='red')
            draw.rectangle((x, 48, x + 16, 62), fill='black')
            frames.append(frame)
        path = self.root / 'animation.gif'
        options = {} if loop is None else {'loop': loop}
        frames[0].save(path, save_all=True, append_images=frames[1:],
                       duration=[40, 100, 70, 120, 50, 90],
                       disposal=disposal, optimize=False, **options)
        return path

    def read_gif(self, path):
        with Image.open(path) as image:
            loop = image.info.get('loop')
            frames, durations = [], []
            for frame in ImageSequence.Iterator(image):
                frames.append(frame.convert('RGBA').copy())
                durations.append(frame.info.get('duration', 0))
            return loop, durations, frames

    def compress(self, path):
        with patch.object(compress_images, 'MAX_SIZE', path.stat().st_size - 1):
            with contextlib.redirect_stdout(io.StringIO()):
                compress_images.compress_image(str(path))

    def test_transparency_disposal_and_playback(self):
        for disposal in [1, 2, 3]:
            with self.subTest(disposal=disposal):
                path = self.make_gif(disposal=disposal)
                original_size = path.stat().st_size
                expected_loop, expected_times, expected_frames = self.read_gif(path)
                self.compress(path)
                loop, times, frames = self.read_gif(path)
                self.assertLess(path.stat().st_size, original_size)
                self.assertEqual(loop, expected_loop)
                self.assertEqual(times, expected_times)
                self.assertEqual(len(frames), len(expected_frames))
                for expected, actual in zip(expected_frames, frames):
                    self.assertEqual(actual.size, expected.size)
                    for color in ['white', 'black']:
                        background = Image.new('RGBA', expected.size, color)
                        before = Image.alpha_composite(background, expected).convert('RGB')
                        after = Image.alpha_composite(background, actual).convert('RGB')
                        self.assertIsNone(ImageChops.difference(before, after).getbbox())

    def test_absent_loop_is_not_changed_to_infinite(self):
        path = self.make_gif(loop=None)
        self.compress(path)
        with Image.open(path) as image:
            self.assertNotIn('loop', image.info)

    def test_small_gif_unchanged(self):
        path = self.make_gif()
        before = path.read_bytes()
        compress_images.compress_image(str(path))
        self.assertEqual(path.read_bytes(), before)

    def test_encoding_failure_preserves_original(self):
        path = self.make_gif()
        before = hashlib.sha256(path.read_bytes()).digest()
        with patch.object(Image.Image, 'save', side_effect=OSError('encoding failed')):
            self.compress(path)
        self.assertEqual(hashlib.sha256(path.read_bytes()).digest(), before)
        self.assertFalse(list(self.root.glob('*.tmp')))


if __name__ == '__main__':
    unittest.main()
