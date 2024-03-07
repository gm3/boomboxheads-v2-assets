import os
import json
import re
import argparse

def main():
    parser = argparse.ArgumentParser(description="Process JSON files and replace VRM URLs")
    parser.add_argument("input_file", help="Input JSON file")
    parser.add_argument("-o", "--output_file", help="Output JSON file")
    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file

    # Read the JSON file
    with open(input_file, 'r') as file:
        data = json.load(file)

    # Check if data is a list or a single object
    if isinstance(data, list):
        for obj in data:
            vrm_url = obj.get("vrm_url")
            if vrm_url:
                # Extract the original hash from the VRM URL
                original_hash_match = re.search(r'ipfs://([a-zA-Z0-9]+)/[0-9]+\.vrm', vrm_url)
                if original_hash_match:
                    original_hash = original_hash_match.group(1)

                    # Replace the hash in the description field
                    description = obj.get("description")
                    if description:
                        new_description = description.replace(original_hash, "QmURAuSRmFFAyragN3h6M6thhMhBPQmNgoNJApDSvob3D5")
                        obj["description"] = new_description

                    # Replace the hash in the vrm_url field
                    new_vrm_url = vrm_url.replace(original_hash, "QmURAuSRmFFAyragN3h6M6thhMhBPQmNgoNJApDSvob3D5")
                    obj["vrm_url"] = new_vrm_url
    else:
        # For single JSON object
        vrm_url = data.get("vrm_url")
        if vrm_url:
            # Extract the original hash from the VRM URL
            original_hash_match = re.search(r'ipfs://([a-zA-Z0-9]+)/[0-9]+\.vrm', vrm_url)
            if original_hash_match:
                original_hash = original_hash_match.group(1)

                # Replace the hash in the description field
                description = data.get("description")
                if description:
                    new_description = description.replace(original_hash, "QmURAuSRmFFAyragN3h6M6thhMhBPQmNgoNJApDSvob3D5")
                    data["description"] = new_description

                # Replace the hash in the vrm_url field
                new_vrm_url = vrm_url.replace(original_hash, "QmURAuSRmFFAyragN3h6M6thhMhBPQmNgoNJApDSvob3D5")
                data["vrm_url"] = new_vrm_url

    # If output file is provided, write to file, otherwise print to stdout
    if output_file:
        with open(output_file, 'w') as file:
            json.dump(data, file, indent=2)
    else:
        print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()
