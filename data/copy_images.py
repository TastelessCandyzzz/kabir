import json
import os
import shutil

# -----------------------------
# USER PARAMETERS
# -----------------------------
MERGED_JSON_PATH = "/home/teaching/Desktop/geo_kabir/roughwork/merged1.json"         # path to your merged.json
SOURCE_IMAGE_FOLDER = "/home/teaching/Desktop/geo_kabir/Images_val"          # folder containing ALL images
DEST_IMAGE_FOLDER = "/home/teaching/Desktop/geo_kabir/roughwork/images"   # folder to copy images into
# -----------------------------


def main():
    # Create destination folder if missing
    os.makedirs(DEST_IMAGE_FOLDER, exist_ok=True)

    # Load merged JSON
    with open(MERGED_JSON_PATH, "r") as f:
        merged = json.load(f)

    # Extract image names
    image_names = list(merged.keys())

    count = 0

    for img_name in image_names:
        src = os.path.join(SOURCE_IMAGE_FOLDER, img_name)
        dst = os.path.join(DEST_IMAGE_FOLDER, img_name)

        # Copy only if file exists
        if os.path.isfile(src):
            shutil.copy(src, dst)
            count += 1
        else:
            print(f"⚠ Image not found: {src}")

    print(f"\n✔ Copied {count} images to: {DEST_IMAGE_FOLDER}")


if __name__ == "__main__":
    main()
