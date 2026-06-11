import os
from PIL import Image

folder = r"c:\Users\user\Desktop\doctor\frontend\image"
for filename in os.listdir(folder):
    if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
        filepath = os.path.join(folder, filename)
        try:
            with Image.open(filepath) as img:
                # Convert to RGB if needed
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Resize if it's too large (e.g., max width 800px)
                max_width = 800
                if img.width > max_width:
                    ratio = max_width / img.width
                    new_size = (max_width, int(img.height * ratio))
                    img = img.resize(new_size, Image.Resampling.LANCZOS)
                
                # Save with lower quality to compress
                img.save(filepath, "JPEG", optimize=True, quality=70)
                print(f"Compressed {filename}")
        except Exception as e:
            print(f"Failed to compress {filename}: {e}")
