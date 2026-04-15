from PIL import Image
import os
import sys

mode = 0
if mode == 1:
    folder = sys.argv[1] if len(sys.argv) > 1 else "assets/images"
else:
    folder = "../src/assets/monsters"

for filename in os.listdir(folder):
    if not filename.lower().endswith(".png"):
        continue

    path = os.path.join(folder, filename)

    try:
        with Image.open(path) as img:
            # make a clean copy of pixel data only
            cleaned = Image.new(img.mode, img.size)
            if mode == 1:
                cleaned.putdata(list(img.getdata()))
            else:
                cleaned.save(path, format="PNG")

            # save without old metadata / ICC profile
            cleaned.save(path, format="PNG")

        print(f"Cleaned: {filename}")

    except Exception as e:
        print(f"Failed: {filename} -> {e}")