import shutil
import os

source_dir = r"e:\Anti-gravity\Microsoft_hackathon"
target_dir = r"e:\Anti-gravity\Microsoft_hackathon\apex-platform\assets"

mapping = {
    "image.png": "image1.png",
    "image copy.png": "image2.png",
    "image copy 2.png": "image3.png"
}

if not os.path.exists(target_dir):
    os.makedirs(target_dir)

for src, dst in mapping.items():
    src_path = os.path.join(source_dir, src)
    dst_path = os.path.join(target_dir, dst)
    if os.path.exists(src_path):
        print(f"Copying {src_path} to {dst_path}")
        shutil.copy2(src_path, dst_path)
    else:
        print(f"Source not found: {src_path}")
