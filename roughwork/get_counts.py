import json
import re

def extract_object_class(question):
    """
    Extracts the object name from:
    "Locate and return bounding boxes for all of the vehicles seen in the image."
    """
    q = question.lower().strip()

    # Remove prefix & suffix
    prefix = "locate and return bounding boxes for all of the "
    suffix = "s seen in the image."

    if q.startswith(prefix) and q.endswith(suffix):
        obj = q[len(prefix):-len(suffix)]
        return obj.strip()  # singular class name

    # Fallback: try simple pattern
    m = re.search(r"for all of the (.*?)s seen in the image", q)
    return m.group(1) if m else None


def parse_pred_boxes(answer_str):
    """
    Convert answer string like:
      "[[10,20,30,40],[40,50,60,70]]"
    into Python list of boxes.
    """
    try:
        boxes = json.loads(answer_str)
        if isinstance(boxes, list):
            return boxes
    except:
        return []
    return []


def build_count_json(
    pred_jsonl_path,
    real_count_json_path,
    output_path="counts_output.json"
):
    # Load real counts
    with open(real_count_json_path, "r") as f:
        real_counts = json.load(f)

    results = []

    # Process predictions
    for line in open(pred_jsonl_path, "r"):
        entry = json.loads(line)

        qid = entry["question_id"]
        image_id = entry["image_id"]
        question = entry["question"]
        ans_str = entry["answer"]

        # --- extract predicted boxes ---
        pred_boxes = parse_pred_boxes(ans_str)
        pred_count = len(pred_boxes)

        # --- extract object class ---
        obj_class = extract_object_class(question)

        # default real count
        real_count = 0

        # find real count from lookup
        if image_id in real_counts and obj_class in real_counts[image_id]:
            real_count = real_counts[image_id][obj_class]

        # build result entry
        results.append({
            "question_id": qid,
            "image_id": image_id,
            "pred_count": pred_count,
            "real_count": real_count
        })

    # write result json
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    print("Saved:", output_path)


# ---------------- RUN ----------------
if __name__ == "__main__":
    build_count_json(
        pred_jsonl_path="/home/teaching/Desktop/geo_kabir/roughwork/class_answers_converted.jsonl",      # your predictions
        real_count_json_path="/home/teaching/Desktop/geo_kabir/roughwork/object_count_train.json",
        output_path="count_results.json"
    )
