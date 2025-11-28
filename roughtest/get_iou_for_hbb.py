import json
import re
import math

def extract_pred_bbox(answer_str):
    """
    Extracts <box>[[x1,y1,x2,y2]]</box> and normalizes by dividing by 1000.
    """
    numbers = re.findall(r"\d+\.?\d*", answer_str)
    if len(numbers) != 4:
        return None

    x1, y1, x2, y2 = map(float, numbers)
    return [x1/1000, y1/1000, x2/1000, y2/1000]


def compute_iou(boxA, boxB):
    """
    AABB IoU for normalized boxes.
    box = [x1, y1, x2, y2]
    """
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    inter_w = max(0, xB - xA)
    inter_h = max(0, yB - yA)
    inter_area = inter_w * inter_h

    areaA = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
    areaB = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])

    union_area = areaA + areaB - inter_area
    if union_area <= 0:
        return 0.0

    return inter_area / union_area


def evaluate_iou(
    pred_jsonl_path="pred_boxes.jsonl",
    gt_jsonl_path="gt.jsonl",
    out_results="iou_results.json",
    out_curve="iou_curve.json"
):
    # -------- Load Predictions --------
    preds = {}
    with open(pred_jsonl_path, "r") as f:
        for line in f:
            js = json.loads(line)
            qid = js["question_id"]
            pred_bbox = extract_pred_bbox(js["answer"])
            preds[qid] = pred_bbox

    # -------- Load Ground Truth --------
    gts = {}
    with open(gt_jsonl_path, "r") as f:
        for line in f:
            js = json.loads(line)
            gts[js["question_id"]] = js["bbox"]

    results = {}
    ious = []

    # Evaluate
    for qid, gt_box in gts.items():
        pred_box = preds.get(qid, None)

        if pred_box is None:
            iou = 0.0
        else:
            iou = compute_iou(gt_box, pred_box)

        results[qid] = {
            "gt_bbox": gt_box,
            "pred_bbox": pred_box,
            "iou": iou,
            "iou_0.5": 1 if iou >= 0.5 else 0,
            "iou_0.7": 1 if iou >= 0.7 else 0
        }

        ious.append(iou)

    # -------- Summary --------
    if len(ious) > 0:
        mean_iou = sum(ious) / len(ious)
        iou_05 = sum(1 for x in ious if x >= 0.5) / len(ious)
        iou_07 = sum(1 for x in ious if x >= 0.7) / len(ious)
    else:
        mean_iou = 0.0
        iou_05 = 0.0
        iou_07 = 0.0

    summary = {
        "mean_iou": mean_iou,
        "iou_0.5_accuracy": iou_05,
        "iou_0.7_accuracy": iou_07,
        "total": len(ious)
    }

    results["_summary"] = summary

    # -------- IoU Curve --------
    ious_sorted = sorted(ious, reverse=True)
    curve = {i+1: ious_sorted[i] for i in range(len(ious_sorted))}

    # -------- Save Outputs --------
    with open(out_results, "w") as f:
        json.dump(results, f, indent=2)

    with open(out_curve, "w") as f:
        json.dump(curve, f, indent=2)

    print("\n===== IOU SUMMARY =====")
    print(json.dumps(summary, indent=2))
    print(f"\nSaved detailed: {out_results}")
    print(f"Saved curve:   {out_curve}")


# Run
if __name__ == "__main__":
    evaluate_iou(
        pred_jsonl_path="/home/teaching/Desktop/geo_kabir/roughtest/answer.jsonl",  # contains <box> predictions
        gt_jsonl_path="/home/teaching/Desktop/geo_kabir/roughtest/gt.jsonl",            # ground truth bbox JSONL
        out_results="iou_results.json",
        out_curve="iou_curve.json"
    )
