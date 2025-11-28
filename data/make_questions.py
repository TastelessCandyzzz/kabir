import json
import os

# -----------------------------
# USER PARAMETERS
# -----------------------------
MERGED_JSON_PATH = "/home/teaching/Desktop/geo_kabir/data/merged.json"                 # input merged json
QUESTIONS_JSONL_PATH = "/home/teaching/Desktop/geo_kabir/data/questions2.jsonl"         # output jsonl file
ANSWERS_JSON_PATH = "/home/teaching/Desktop/geo_kabir/data/answers1.jsonl"               # output ground-truth file
DATASET_NAME = "vrs_bench_val"                   # dataset field value
# -----------------------------


def generate_question_string(ref_sentence: str) -> str:
    """Add the prefix to referring sentence."""
    return f"Locate and return bounding boxes for {ref_sentence.strip()}"


def main():
    # Load merged json
    with open(MERGED_JSON_PATH, "r") as f:
        merged = json.load(f)

    answers_dict = {}   # stores true bbox + poly

    # Open .jsonl output file
    with open(QUESTIONS_JSONL_PATH, "w") as q_out:

        # Iterate over each image entry
        for image_name, content in merged.items():

            objects = content.get("objects", [])
            for obj in objects:
                obj_id = obj.get("obj_id")
                ref_sentence = obj.get("referring_sentence", "").strip()

                # Construct question_id
                qid = f"{image_name}_q{obj_id}"

                # Build question line
                question_text = generate_question_string(ref_sentence)

                question_entry = {
                    "image_id": image_name,
                    "question": question_text,
                    "question_id": qid,
                    "bbox": [0, 0, 0, 0],  # always zero for questions.jsonl
                    "poly": "",
                    "dataset": DATASET_NAME
                }

                # Write one line per question
                q_out.write(json.dumps(question_entry) + "\n")

                # Store ground truth in answers.json
                answers_dict[qid] = {
                    "image_id": image_name,
                    "bbox": obj.get("obj_coord", []),
                    "poly": obj.get("obj_corner", [])
                }

    # Write answers.json
    with open(ANSWERS_JSON_PATH, "w") as a_out:
        json.dump(answers_dict, a_out, indent=4)

    print(f"\n✔ Generated {QUESTIONS_JSONL_PATH}")
    print(f"✔ Generated {ANSWERS_JSON_PATH}")
    print("Done.")


if __name__ == "__main__":
    main()
