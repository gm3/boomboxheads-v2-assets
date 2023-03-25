#!/bin/bash

# Parse JSON and extract values
name=$(jq -r '.name' $1)
description=$(jq -r '.description' $1)
color=$(jq -r '.attributes[] | select(.trait_type == "Color Hue") | .value' $1 || echo "")
clouds=$(jq -r '.attributes[] | select(.trait_type == "Clouds") | .value' $1 || echo "")
chains=$(jq -r '.attributes[] | select(.trait_type == "Chains") | .value' $1 || echo "")
special=$(jq -r '.attributes[] | select(.trait_type == "Special") | .value' $1 || echo "")

# Print values in CSV format
echo "name,description,attributes[Color Hue],attributes[Clouds],attributes[Chains],attributes[Special]"
echo "$name,\"$description\",$color,$clouds,$chains,$special"
