import json

# -----------------------------
# USER PARAMETERS
# -----------------------------
CLASS_COUNT_JSON = "/home/teaching/Desktop/geo_kabir/roughwork/object_count_train.json"      # input json (image -> class counts)
OUTPUT_JSONL = "/home/teaching/Desktop/geo_kabir/roughwork/class_based_questions.jsonl" # output
DATASET_NAME = "vrs_bench_val"
# -----------------------------


def pluralize(cls_name: str) -> str:
    """Add 's' to make plural. (Simple pluralization as requested)."""
    return cls_name + "s"


def main():
    # Load class count json
    with open(CLASS_COUNT_JSON, "r") as f:
        class_map = json.load(f)

    with open(OUTPUT_JSONL, "w") as out_file:

        for image_id, cls_dict in class_map.items():
            # For each class, create 1 question
            q_index = 0

            for cls_name in cls_dict.keys():
                plural = pluralize(cls_name)

                question_text = (
                    f"Locate and return bounding boxes for all of the {plural} seen in the image."
                )

                question_id = f"{image_id}_q{q_index}"

                entry = {
                    "image_id": image_id,
                    "question": question_text,
                    "question_id": question_id,
                    "bbox": [0, 0, 0, 0],
                    "poly": "",
                    "dataset": DATASET_NAME
                }

                out_file.write(json.dumps(entry) + "\n")
                q_index += 1

    print(f"✔ Generated JSONL at: {OUTPUT_JSONL}")


if __name__ == "__main__":
    main()
