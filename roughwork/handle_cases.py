import json
import re

def parse_boxes(answer_str):
    """
    Returns:
      boxes: list of [x1,y1,x2,y2]
      is_xml: True if original format was <box>...</box>
    """
    answer_str = answer_str.strip()

    # ---------- Case 1: <box> ... </box> ----------
    xml_match = re.search(r"<box>\s*(\[\[.*?\]\])\s*</box>", answer_str)
    if xml_match:
        inner = xml_match.group(1)     # [[x1,y1,x2,y2]]
        try:
            boxes = json.loads(inner)
            return boxes, True
        except:
            pass

    # ---------- Case 2: Plain Python list ----------
    # remove malformed spaces or unexpected text
    try:
        boxes = json.loads(answer_str)
        if isinstance(boxes, list):
            # ensure nested list
            if len(boxes) > 0 and all(isinstance(b, list) for b in boxes):
                return boxes, False
    except:
        pass

    # ---------- Fallback ----------
    return [], False


def process_answers(input_jsonl, output_jsonl):
    out_file = open(output_jsonl, "w")

    for line in open(input_jsonl, "r"):
        entry = json.loads(line)

        ans_str = entry["answer"]
        boxes, is_xml = parse_boxes(ans_str)

        # ---------- Apply rules ----------
        if is_xml:
            # Do NOT multiply XML-format boxes
            final_boxes = boxes
        else:
            # Multiply clean box lists by 10
            final_boxes = []
            for b in boxes:
                final_boxes.append([v * 10 for v in b])

        # ---------- Convert back to string ----------
        entry["answer"] = json.dumps(final_boxes)

        # ---------- Write updated line ----------
        out_file.write(json.dumps(entry) + "\n")

    out_file.close()
    print("Saved:", output_jsonl)


# ---------------- RUN ----------------
if __name__ == "__main__":
    process_answers(
        input_jsonl="/home/teaching/Desktop/geo_kabir/roughwork/class_answer.jsonl",          # change to your path
        output_jsonl="/home/teaching/Desktop/geo_kabir/roughwork/class_answers_converted.jsonl"
    )
