from PIL import Image
import os

folder = "src/assets/monsters"

for filename in os.listdir(folder):
    if not filename.lower().endswith(".png"):
        continue

    path = os.path.join(folder, filename)

    try:
        with Image.open(path) as img:
            img = img.convert("RGBA")
            img.save(path, format="PNG", icc_profile=None)

        print(f"Fixed: {filename}")

    except Exception as e:
        print(f"Failed: {filename} -> {e}")