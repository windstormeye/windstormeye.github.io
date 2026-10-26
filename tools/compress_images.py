import os
import sys
from PIL import Image, ImageSequence

MAX_SIZE = 700 * 1024  # 700KB


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
                print(f'  -> GIF: {width}x{height}, {len(frames)} 帧, {size / 1024:.2f} KB')
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
        if os.path.exists(best_path):
            os.replace(best_path, file_path)
            print(f'成功：已保留 GIF 动画，压缩至 {best_size / 1024:.2f} KB')
        else:
            print('提示：没有更小的 GIF，保留原文件')
        if best_size > MAX_SIZE:
            print('提示：GIF 已达到最小尺寸，仍超过大小限制')
    finally:
        for path in (temp_path, best_path):
            if os.path.exists(path):
                os.remove(path)

def compress_image(file_path):
    if not os.path.exists(file_path):
        return

    try:
        file_size = os.path.getsize(file_path)
        if file_size <= MAX_SIZE:
            return

        print(f"检测到大图: {file_path} ({file_size / 1024:.2f} KB)")
        print(f"正在压缩并替换原图...")

        if file_path.lower().endswith('.gif'):
            compress_gif(file_path)
            return
        
        img = Image.open(file_path)
        original_format = img.format
        
        # Determine format for saving
        save_format = original_format
        if not save_format:
            if file_path.lower().endswith(('.jpg', '.jpeg')):
                save_format = 'JPEG'
            elif file_path.lower().endswith('.png'):
                save_format = 'PNG'
            elif file_path.lower().endswith('.webp'):
                save_format = 'WEBP'
            else:
                save_format = 'JPEG'

        quality = 95
        temp_path = file_path + ".tmp"
        
        try:
            while file_size > MAX_SIZE:
                width, height = img.size
                # Reduce dimensions by 10% each step
                new_width = int(width * 0.9)
                new_height = int(height * 0.9)
                
                if new_width < 10 or new_height < 10:
                    break
                    
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Save to temp path
                if save_format == 'JPEG':
                    img.convert('RGB').save(temp_path, format=save_format, quality=quality, optimize=True)
                else:
                    img.save(temp_path, format=save_format, optimize=True)
                    
                file_size = os.path.getsize(temp_path)
                print(f"  -> 调整尺寸至: {new_width}x{new_height}, 当前大小: {file_size / 1024:.2f} KB")
                
                # If resizing isn't enough, start dropping quality for JPEGs
                if save_format == 'JPEG' and quality > 30:
                    quality -= 10
            
            # Replace original with compressed temp file
            if os.path.exists(temp_path):
                os.replace(temp_path, file_path)
                print(f"成功：已删除老图片并保留压缩后的新图片 ({os.path.getsize(file_path) / 1024:.2f} KB)")
            else:
                print(f"提示：图片已在限制范围内，无需替换")

        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
        
    except Exception as e:
        print(f"Error compressing {file_path}: {e}")

if __name__ == "__main__":
    # Filter for image extensions
    image_extensions = ('.jpg', '.jpeg', '.png', '.webp', '.gif')
    images_to_process = [arg for arg in sys.argv[1:] if arg.lower().endswith(image_extensions)]
    
    for path in images_to_process:
        compress_image(path)
