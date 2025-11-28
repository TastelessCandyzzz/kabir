import json
import os
import cv2
import numpy as np

# ------------ USER CONFIG -------------------
PRED_JSON = "/home/teaching/Desktop/geo_kabir/roughtest/aabb_normalized.json"   # format: {question_id: {"bbox":[...]}}
QA_JSONL = "/home/teaching/Desktop/geo_kabir/roughtest/gt.jsonl"              # list of items with image_id, question_id, bbox, question
IMAGE_FOLDER = "/home/teaching/Desktop/geo_kabir/roughwork/images"          # folder where images are stored
OUTPUT_FOLDER = "/home/teaching/Desktop/geo_kabir/roughtest/hbb_visualise"
# ---------------------------------------------

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def denormalize_bbox(bbox, w, h):
    """Convert normalized bbox [x1,y1,x2,y2] → absolute pixel coordinates."""
    x1 = int(bbox[0] * w)
    y1 = int(bbox[1] * h)
    x2 = int(bbox[2] * w)
    y2 = int(bbox[3] * h)
    return x1, y1, x2, y2

# ---------------- LOAD PREDICTIONS ----------------
with open(PRED_JSON, "r") as f:
    pred_data = json.load(f)

# ---------------- LOAD QA JSONL --------------------
qa_data = []
with open(QA_JSONL, "r") as f:
    for line in f:
        line = line.strip()
        if line:
            qa_data.append(json.loads(line))

# ---------------- PROCESS EACH ENTRY ----------------
for item in qa_data:

    qid = item["question_id"]
    img_name = item["image_id"]
    gt_bbox = item["bbox"]          # ground truth normalized
    question = item["question"]

    # Skip if prediction is missing
    if qid not in pred_data:
        print(f"Skipping {qid}, no prediction found.")
        continue

    pred_bbox = pred_data[qid]["bbox"]

    img_path = os.path.join(IMAGE_FOLDER, img_name)
    if not os.path.exists(img_path):
        print(f"Image not found: {img_path}")
        continue

    img = cv2.imread(img_path)
    if img is None:
        print(f"Failed to read image {img_path}")
        continue

    h, w = img.shape[:2]

    # Denormalize both boxes
    px1, py1, px2, py2 = denormalize_bbox(pred_bbox, w, h)
    gx1, gy1, gx2, gy2 = denormalize_bbox(gt_bbox, w, h)

    # Draw predicted box (RED)
    cv2.rectangle(img, (px1, py1), (px2, py2), (0, 0, 255), 3)
    cv2.putText(img, "Pred", (px1, max(py1 - 10, 0)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    # Draw ground truth box (GREEN)
    cv2.rectangle(img, (gx1, gy1), (gx2, gy2), (0, 255, 0), 3)
    cv2.putText(img, "GT", (gx1, max(gy1 - 10, 0)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # Add question text at bottom
    question_area = np.ones((80, w, 3), dtype=np.uint8) * 255
    cv2.putText(question_area, question[:150], (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

    # Stack image + question area
    out_img = np.vstack((img, question_area))

    save_path = os.path.join(OUTPUT_FOLDER, f"{qid}.jpg")
    cv2.imwrite(save_path, out_img)

    print(f"Saved: {save_path}")
