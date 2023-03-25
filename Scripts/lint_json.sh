#!/bin/bash

# Create the out directory if it doesn't exist
mkdir -p out

# Loop through all .json files in the current directory
for file in *.json
do
  # Validate the file using jq
  if jq . "$file" >/dev/null 2>&1; then
    # Export the validated file to the out directory
    jq . "$file" > "out/$file"
    echo "$file is valid."
  else
    echo "$file is not a valid JSON file."
  fi
done
