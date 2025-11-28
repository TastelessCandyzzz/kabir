import json
import os

def build_jsonl_entries(data, zero_bbox=False):
    """
    Builds jsonl entries for predictions (zero_bbox=True) or ground truth (zero_bbox=False).
    """
    entries = []

    for image_id, content in data.items():
        objects = content.get("objects", [])

        for obj in objects:
            ref = obj.get("referring_sentence", "").strip()
            if not ref.endswith("."):
                ref += "."

            question = f"Locate and return the bounding box for {ref}"

            if zero_bbox:
                bbox = [0, 0, 0, 0]
            else:
                bbox = obj.get("obj_coord", [0, 0, 0, 0])

            entry = {
                "image_id": image_id,
                "question": question,
                "question_id": f"{image_id}_q{obj.get('obj_id', 0)}",
                "bbox": bbox,
                "poly": "",
                "dataset": "vrs_bench_val"
            }

            entries.append(entry)

    return entries


def save_jsonl(path, entries):
    with open(path, "w") as f:
        for e in entries:
            f.write(json.dumps(e) + "\n")


def main():
    input_json_path = "/home/teaching/Desktop/geo_kabir/roughtest/merged1.json"   # change this if needed
    pred_out = "/home/teaching/Desktop/geo_kabir/roughtest/pred.jsonl"
    gt_out = "/home/teaching/Desktop/geo_kabir/roughtest/gt.jsonl"

    # Load input JSON
    with open(input_json_path, "r") as f:
        data = json.load(f)

    # Build prediction JSONL (bbox all zeros)
    pred_entries = build_jsonl_entries(data, zero_bbox=True)

    # Build ground-truth JSONL (use actual obj_coord)
    gt_entries = build_jsonl_entries(data, zero_bbox=False)

    # Save files
    save_jsonl(pred_out, pred_entries)
    save_jsonl(gt_out, gt_entries)

    print("Saved:")
    print("  →", pred_out)
    print("  →", gt_out)


if __name__ == "__main__":
    main()
