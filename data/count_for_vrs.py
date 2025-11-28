import json
import os

# ------------------------------
# USER PARAMETERS
# ------------------------------
MERGED_JSON_PATH = "/home/teaching/Desktop/geo_kabir/roughwork/merged1.json"          # Input merged json
OUTPUT_JSON_PATH = "/home/teaching/Desktop/geo_kabir/roughwork/object_count_train.json"   # Output aggregated json
# ------------------------------


def main():
    # Load merged json
    with open(MERGED_JSON_PATH, "r") as f:
        merged = json.load(f)

    result = {}

    # Iterate through all images
    for image_name, content in merged.items():
        objects = content.get("objects", [])

        class_count = {}

        # Count occurrences of each obj_cls
        for obj in objects:
            cls = obj.get("obj_cls", "").strip()

            if cls:
                class_count[cls] = class_count.get(cls, 0) + 1

        result[image_name] = class_count

    # Save result
    with open(OUTPUT_JSON_PATH, "w") as f:
        json.dump(result, f, indent=4)

    print(f"✔ Saved object counts to {OUTPUT_JSON_PATH}")


if __name__ == "__main__":
    main()
