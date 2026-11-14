import os
import sys
from PIL import Image, ImageOps, ImageSequence

MAX_SIZE = 500_000  # 500 KB，按十进制字节计，确保文件管理器中也不超过 500 KB。


def gif_palette(source):
    # One palette prevents the static area of a composite GIF changing colors
    # between frames, and lets the encoder keep that area as a small delta.
    source.seek(0)
    samples = Image.new('RGB', (128, 128 * source.n_frames))
    for index, frame in enumerate(ImageSequence.Iterator(source)):
        samples.paste(frame.convert('RGB').resize((128, 128), Image.Resampling.NEAREST),
                      (0, index * 128))
    palette = samples.quantize(colors=255)
    colors = palette.getpalette()[:765]
    colors += [0] * (765 - len(colors))
    # The spare slot duplicates the last real color before indices are shifted.
    palette.putpalette(colors + colors[-3:])
    return palette


def gif_frame(frame, size, palette):
    # Pillow has already applied the source frame's disposal and local rectangle.
    rgba = frame.convert('RGBA')
    if rgba.size != size:
        rgba = rgba.resize(size, Image.Resampling.LANCZOS)
    alpha = rgba.getchannel('A')
    transparent = alpha.getextrema()[0] < 128
    quantized = rgba.convert('RGB').quantize(palette=palette, dither=Image.Dither.NONE)
    # Reserve index 0 for transparency in every local palette.
    result = quantized.point(list(range(1, 256)) + [255])
    colors = palette.getpalette()[:765]
    result.putpalette([0, 0, 0] + colors)
    result.paste(0, mask=alpha.point(lambda value: 255 if value < 128 else 0))
    result.info = {'transparency': 0}
    return result, transparent


def compress_gif(file_path):
    original_size = os.path.getsize(file_path)
    temp_path = file_path + '.tmp'
    best_path = file_path + '.best.tmp'
    best_size = original_size
    try:
        with Image.open(file_path) as source:
            width, height = source.size
            options = {key: source.info[key] for key in ('loop', 'comment') if key in source.info}
            palette = gif_palette(source)
            while True:
                source.seek(0)
                frames, durations = [], []
                has_transparency = False
                for frame in ImageSequence.Iterator(source):
                    encoded, transparent = gif_frame(frame, (width, height), palette)
                    frames.append(encoded)
                    durations.append(frame.info.get('duration', 0))
                    has_transparency |= transparent
                # Full composited frames can use delta encoding when opaque.
                # Transparent canvases must clear between frames to avoid trails.
                frames[0].save(temp_path, format='GIF', save_all=True,
                               append_images=frames[1:], duration=durations,
                               disposal=2 if has_transparency else 1,
                               transparency=0, background=0, optimize=True, **options)
                size = os.path.getsize(temp_path)
                print(f'  -> GIF: {width}x{height}, {len(frames)} 帧, {size / 1000:.2f} KB')
                with Image.open(temp_path) as result:
                    if source.n_frames > 1 and result.n_frames < 2:
                        print('提示：继续缩小会丢失动画，保留上一版')
                        break
                    if result.info.get('loop') != options.get('loop'):
                        raise ValueError('GIF 循环设置发生变化')
                    duration = 0
                    for frame in ImageSequence.Iterator(result):
                        frame.load()
                        duration += frame.info.get('duration', 0)
                    if duration != sum(durations):
                        raise ValueError('GIF 播放时长发生变化')
                if size < best_size:
                    os.replace(temp_path, best_path)
                    best_size = size
                if best_size <= MAX_SIZE:
                    break
                new_width, new_height = int(width * 0.9), int(height * 0.9)
                if min(new_width, new_height) < 10:
                    break
                width, height = new_width, new_height
        if best_size > MAX_SIZE:
            raise ValueError('GIF 无法在保留动画的同时压缩到 500 KB 以内，保留原文件')
        if os.path.exists(best_path):
            os.replace(best_path, file_path)
            print(f'成功：已保留 GIF 动画，压缩至 {best_size / 1000:.2f} KB')
        else:
            print('提示：没有更小的 GIF，保留原文件')
    finally:
        for path in (temp_path, best_path):
            if os.path.exists(path):
                os.remove(path)

def compress_image(file_path):
    temp_path = file_path + '.tmp'
    try:
        file_size = os.path.getsize(file_path)
        if file_size <= MAX_SIZE:
            return True

        print(f'检测到大图: {file_path} ({file_size / 1000:.2f} KB)')
        if file_path.lower().endswith('.gif'):
            compress_gif(file_path)
            return True

        with Image.open(file_path) as source:
            # 手机 JPEG 可能包含 MPO 辅助图层；网页保留主图并按 JPEG 编码。
            save_format = 'JPEG' if source.format == 'MPO' else source.format
            img = ImageOps.exif_transpose(source)
            # 转正照片后移除 EXIF 等元数据，保持原始图片格式。
            img.info.clear()

        quality = 95
        while file_size > MAX_SIZE:
            width, height = img.size
            new_size = (max(1, int(width * 0.9)), max(1, int(height * 0.9)))
            if new_size == img.size:
                raise ValueError('图片已达到最小尺寸，仍超过 500 KB，保留原文件')
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            if save_format == 'JPEG':
                img.convert('RGB').save(temp_path, format=save_format, quality=quality, optimize=True)
            else:
                img.save(temp_path, format=save_format, optimize=True)
            file_size = os.path.getsize(temp_path)
            print(f'  -> 调整尺寸至: {new_size[0]}x{new_size[1]}, 当前大小: {file_size / 1000:.2f} KB')
            if save_format == 'JPEG':
                quality = max(30, quality - 10)

        # 只有达到大小上限才替换原图；失败时保持原文件。
        os.replace(temp_path, file_path)
        print(f'成功：保留 {save_format} 格式，压缩至 {file_size / 1000:.2f} KB')
        return True
    except Exception as error:
        print(f'压缩失败: {file_path}: {error}', file=sys.stderr)
        return False
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


if __name__ == '__main__':
    image_extensions = ('.jpg', '.jpeg', '.png', '.webp', '.gif')
    images_to_process = [arg for arg in sys.argv[1:] if arg.lower().endswith(image_extensions)]
    success = True
    for path in images_to_process:
        if not compress_image(path):
            success = False
    sys.exit(0 if success else 1)
