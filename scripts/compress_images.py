import os
import sys
from PIL import Image

MAX_SIZE = 700 * 1024  # 700KB

def compress_image(file_path):
    if not os.path.exists(file_path):
        return

    try:
        file_size = os.path.getsize(file_path)
        if file_size <= MAX_SIZE:
            return

        print(f"检测到大图: {file_path} ({file_size / 1024:.2f} KB)")
        print(f"正在压缩并替换原图...")
        
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
    image_extensions = ('.jpg', '.jpeg', '.png', '.webp')
    images_to_process = [arg for arg in sys.argv[1:] if arg.lower().endswith(image_extensions)]
    
    for path in images_to_process:
        compress_image(path)
