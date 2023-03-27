#!/bin/bash

# To use the script, save it to a file and make it executable (e.g., chmod +x script.sh), then pass the input JSON to the script via stdin (e.g., cat input.json | ./script.sh). The transformed JSON will be printed to stdout.

# Note: This script assumes that the input JSON is well-formed and contains all the required fields. You may want to add additional error handling to the script if the input JSON is not guaranteed to be valid.

# Read the input JSON
json=$(cat)

# Extract the values of the desired fields
name=$(echo "$json" | jq '.name')
author=$(echo "$json" | jq '.created_by')
description=$(echo "$json" | jq '.description')
vrm_url=$(echo "$json" | jq '.vrm_url')
image=$(echo "$json" | jq '.image')
Hat=$(echo "$json" | jq '.attributes[] | select(.trait_type == "Hat").value')
Eyes=$(echo "$json" | jq '.attributes[] | select(.trait_type == "Eyes").value')
BodyTexture=$(echo "$json" | jq '.attributes[] | select(.trait_type == "BodyTexture").value')
Pose=$(echo "$json" | jq '.attributes[] | select(.trait_type == "Pose").value')
BGColor=$(echo "$json" | jq '.attributes[] | select(.trait_type == "BGColor").value')
BBTexture=$(echo "$json" | jq '.attributes[] | select(.trait_type == "BBTexture").value')
Border=$(echo "$json" | jq '.attributes[] | select(.trait_type == "Border").value')
external_url=$(echo "$json" | jq '.external_url')


# Construct the output JSON
output=$(cat <<EOF
{
  "packets": [
    {
      "name": $name,
      "author": $author,
      "description": $description,
      "vrm_url": $vrm_url,
      "image": $image,
      "Hat": $Hat,
      "Eyes": $Eyes,
      "BodyTexture": $BodyTexture,
      "Pose": $Pose,
      "BGColor": $BGColor,
      "BBTexture": $BBTexture,
      "Border": $Border,
      "external_url": $external_url
    }
  ]
}
EOF
)

# Print the output JSON
echo "$output"
