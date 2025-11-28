import json
import re

# -----------------------------
# USER PARAMETERS
# -----------------------------
INPUT_JSONL = "/home/teaching/Desktop/geo_kabir/GeoGround/answers___.jsonl"               # your input jsonl
OUTPUT_JSON = "object_counts_from_answers.json"   # output json
# -----------------------------


def extract_box_count(answer_str: str) -> int:
    """
    Extract number of boxes from the answer string.
    Works for:
        "<box>[[34,7,42,11]]</box>"
        "[[34,7,42,11],[12,13,14,15]]"
        "<box>[[x],[y],[z]]</box>"
    """
    # Remove <box> tags if present
    clean = answer_str.replace("<box>", "").replace("</box>", "")

    # Find all occurrences of bounding-box brackets
    # Pattern matches "[a,b,c,d]" groups
    boxes = re.findall(r"\[[0-9\s.,]+\]", clean)

    # boxes includes sublists, but also includes the list itself.
    # So count only the innermost lists which represent boxes:
    # They should contain 4 numbers.
    count = 0
    for b in boxes:
        nums = re.findall(r"\d+", b)
        if len(nums) == 4:
            count += 1

    return count


def main():
    out_dict = {}

    with open(INPUT_JSONL, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            item = json.loads(line)

            qid = item["question_id"]
            image_id = item["image_id"]
            answer = item.get("answer", "")

            obj_count = extract_box_count(answer)

            out_dict[qid] = {
                "image_id": image_id,
                "object_count": obj_count
            }

    with open(OUTPUT_JSON, "w") as f:
        json.dump(out_dict, f, indent=4)

    print(f"✔ Saved object counts to {OUTPUT_JSON}")


if __name__ == "__main__":
    main()
