import json

def compute_iou(boxA, boxB):
    """
    Compute IoU of two normalized AABB boxes:
    box = [x1, y1, x2, y2]
    """

    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    interW = max(0, xB - xA)
    interH = max(0, yB - yA)
    interArea = interW * interH

    areaA = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
    areaB = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])

    unionArea = areaA + areaB - interArea
    if unionArea == 0:
        return 0.0

    return interArea / unionArea


def evaluate_iou(
    gt_jsonl_path="gt.jsonl",
    pred_json_path="aabb_normalized.json",
    output_json="iou_results.json"
):
    # Load Ground Truth
    gt = {}
    with open(gt_jsonl_path, "r") as f:
        for line in f:
            js = json.loads(line)
            qid = js["question_id"]
            gt[qid] = js["bbox"]

    # Load Predictions
    with open(pred_json_path, "r") as f:
        pred = json.load(f)

    results = {}
    merged_iou_sum = 0
    total = 0
    iou_05_count = 0
    iou_07_count = 0

    for qid, gt_box in gt.items():

        pred_box = pred.get(qid, {}).get("bbox", None)

        if pred_box is None or len(pred_box) != 4:
            iou = 0.0
        else:
            iou = compute_iou(gt_box, pred_box)

        iou05 = 1 if iou >= 0.5 else 0
        iou07 = 1 if iou >= 0.7 else 0

        results[qid] = {
            "gt_bbox": gt_box,
            "pred_bbox": pred_box,
            "iou": iou,
            "iou_0.5": iou05,
            "iou_0.7": iou07
        }

        merged_iou_sum += iou
        iou_05_count += iou05
        iou_07_count += iou07
        total += 1

    merged_iou = merged_iou_sum / total if total > 0 else 0

    summary = {
        "merged_iou": merged_iou,
        "iou_0.5_accuracy": iou_05_count / total,
        "iou_0.7_accuracy": iou_07_count / total,
        "total_samples": total
    }

    results["_summary"] = summary

    # Save
    with open(output_json, "w") as f:
        json.dump(results, f, indent=2)

    print("\n=========== IOU RESULTS ===========")
    print(json.dumps(summary, indent=2))
    print("Saved full results to:", output_json)


# Example run
if __name__ == "__main__":
    evaluate_iou(
        gt_jsonl_path="/home/teaching/Desktop/geo_kabir/roughtest/gt.jsonl",                     # your GT JSONL
        pred_json_path="/home/teaching/Desktop/geo_kabir/roughtest/aabb_normalized.json",        # your predictions
        output_json="/home/teaching/Desktop/geo_kabir/roughtest/iou_results.json"
    )
