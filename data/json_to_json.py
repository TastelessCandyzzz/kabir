import os
import json
import random
from tqdm import tqdm

def merge_random_jsons(folder_path, sample_size=1000, output_path="merged.json"):
    # Get all .json files
    all_files = [f for f in os.listdir(folder_path) if f.endswith(".json")]

    if len(all_files) < sample_size:
        raise ValueError("Not enough JSON files in the folder!")

    # Randomly sample 1000 JSON files
    sampled_files = random.sample(all_files, sample_size)

    merged_dict = {}

    for file_name in tqdm(sampled_files, desc="Merging JSONs"):
        file_path = os.path.join(folder_path, file_name)

        # Load JSON content
        with open(file_path, "r") as f:
            data = json.load(f)

        # Use image name as key
        image_key = data["image"]
        merged_dict[image_key] = data

    # Save merged dictionary
    with open(output_path, "w") as f:
        json.dump(merged_dict, f, indent=4)

    print(f"\nSaved merged JSON to: {output_path}")



merge_random_jsons("/home/teaching/Desktop/geo_kabir/Annotations_val", sample_size=100, output_path="merged.json")