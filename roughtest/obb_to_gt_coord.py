import json
import math

def obb_to_aabb(cx, cy, w, h, theta):
    """
    Convert OBB to AABB by rotating corners then taking min/max.
    Inputs are in the SAM 0-1000 scale.
    """
    theta_rad = math.radians(theta)

    # Half sizes
    w2 = w / 2
    h2 = h / 2

    # OBB corners relative to center
    corners = [
        (-w2, -h2),
        ( w2, -h2),
        ( w2,  h2),
        (-w2,  h2)
    ]

    # Rotate corners
    rotated = []
    for x, y in corners:
        xr = x * math.cos(theta_rad) - y * math.sin(theta_rad)
        yr = x * math.sin(theta_rad) + y * math.cos(theta_rad)
        rotated.append((cx + xr, cy + yr))

    xs = [p[0] for p in rotated]
    ys = [p[1] for p in rotated]

    return min(xs), min(ys), max(xs), max(ys)


def convert_obb_json(input_json, output_json, scale=1000):
    with open(input_json, "r") as f:
        data = json.load(f)

    output = {}

    for qid, entry in data.items():
        obbs = entry.get("obbs", [])

        if len(obbs) == 0:
            output[qid] = {"bbox": []}
            continue

        # Only one OBB per question
        cx, cy, w, h, theta = obbs[0]

        # Convert OBB → AABB (in 0–1000 scale)
        x1, y1, x2, y2 = obb_to_aabb(cx, cy, w, h, theta)

        # Normalize 0–1
        x1 /= scale
        y1 /= scale
        x2 /= scale
        y2 /= scale

        output[qid] = {
            "bbox": [x1, y1, x2, y2]
        }

    with open(output_json, "w") as f:
        json.dump(output, f, indent=2)

    print("Saved AABB normalized JSON →", output_json)



# Example usage
if __name__ == "__main__":
    convert_obb_json(
        input_json="/home/teaching/Desktop/geo_kabir/roughtest/obb_sam_vis.json",         # your SAM OBB JSON
        output_json="/home/teaching/Desktop/geo_kabir/roughtest/aabb_normalized.json",     # save here
        scale=1000
    )
