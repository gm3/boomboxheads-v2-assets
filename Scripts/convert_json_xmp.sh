#!/bin/bash
PACKETS_FILE=$1
OUTPUT_FILE=$2

if [[ -z $PACKETS_FILE || -z $OUTPUT_FILE ]]; then
  echo "Usage: ./convert_json.sh [PACKETS_FILE] [OUTPUT_FILE]"
  exit 1
fi

echo "{" > $OUTPUT_FILE
echo '  "packets": [' >> $OUTPUT_FILE

while read line
do
  if [[ ! -z "$line" ]]; then
    if jq -e '.name and .created_by and .description and .vrm_url and .image and .external_url' >/dev/null <<<"$line"; then
      name=$(jq -r '.name' <<< "$line")
      author=$(jq -r '.created_by' <<< "$line")
      description=$(jq -r '.description' <<< "$line")
      vrm_url=$(jq -r '.vrm_url' <<< "$line")
      image=$(jq -r '.image' <<< "$line")
      external_url=$(jq -r '.external_url' <<< "$line")

      # Start packet dictionary
      echo "    {" >> $OUTPUT_FILE
      echo "      \"name\": \"$name\"," >> $OUTPUT_FILE
      echo "      \"author\": \"$author\"," >> $OUTPUT_FILE
      echo "      \"description\": \"$description\"," >> $OUTPUT_FILE
      echo "      \"vrm_url\": \"$vrm_url\"," >> $OUTPUT_FILE
      echo "      \"image\": \"$image\"," >> $OUTPUT_FILE
      echo "      \"external_url\": \"$external_url\"," >> $OUTPUT_FILE

      # Extract values for each property in the array
      properties=("Hat" "Eyes" "BodyTexture" "Pose" "BGColor" "BBTexture" "Border" "Back" "Mouth" "Special")
      attribute_count=$(jq '.attributes | length' <<< "$line")
      for ((i=0;i<$attribute_count;i++)); do
        trait_type=$(jq -r ".attributes[$i].trait_type" <<< "$line")
        value=$(jq -r ".attributes[$i].value" <<< "$line")
        if (( $i == $attribute_count-1 )); then
          # Last attribute, don't add a comma
          echo "      \"$trait_type\": \"$value\"" >> $OUTPUT_FILE
        else
          # Not the last attribute, add a comma
          echo "      \"$trait_type\": \"$value\"," >> $OUTPUT_FILE
        fi
      done

      # End attributes dictionary
      echo "    }" >> $OUTPUT_FILE

#      # End packet dictionary
#      echo "    }," >> $OUTPUT_FILE
    fi
  fi
done < $PACKETS_FILE

# Remove the trailing comma from the last packet
sed -i '$ s/,$//' $OUTPUT_FILE

echo '  ]' >> $OUTPUT_FILE
echo '}' >> $OUTPUT_FILE

echo "Conversion complete. Output written to $OUTPUT_FILE."
