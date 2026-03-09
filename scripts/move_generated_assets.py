import shutil
import os

artifact_dir = r"C:\Users\yashk\.gemini\antigravity\brain\728092e5-cb07-4af4-acfb-9de97ec7f4d8"
target_dir = r"e:\Anti-gravity\Microsoft_hackathon\apex-platform\assets"

files = [
    ("e_anti_gravity_microsoft_hackathon_apex_platform_assets_image1_png_1773099708297.png", "image1.png"),
    ("e_anti_gravity_microsoft_hackathon_apex_platform_assets_image2_png_1773099722687.png", "image2.png"),
    ("e_anti_gravity_microsoft_hackathon_apex_platform_assets_image3_png_1773099737023.png", "image3.png")
]

if not os.path.exists(target_dir):
    os.makedirs(target_dir)

for artifact_name, target_name in files:
    src_path = os.path.join(artifact_dir, artifact_name)
    dst_path = os.path.join(target_dir, target_name)
    if os.path.exists(src_path):
        print(f"Moving {src_path} to {dst_path}")
        shutil.copy2(src_path, dst_path)
    else:
        print(f"Artifact not found: {src_path}")
