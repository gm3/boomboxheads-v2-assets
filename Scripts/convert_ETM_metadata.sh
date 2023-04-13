#!/bin/bash

## Use: ./script.sh out -c (combined) or -s (separate) files

combine=false
separate=false
suffix="$2"
output_file=""

function usage() {
  echo "Usage: $0 [-c | -s] out"
  echo "  -c: Combine output into a single file 'output.json'"
  echo "  -s: Generate separate output files 'Nout.json'"
  exit 1
}

while getopts 'csh' flag; do
  case "${flag}" in
    c) combine=true; output_file="output.json" ;;
    s) separate=true ;;
    h) usage ;;
    *) usage ;;
  esac
done

function generate_json() {
cat <<EOF
{
  "name": "$name",
  "description": "$description",
  "metadataStandard": "ETM_v1.0.0",
  "animation_url": "$animation_url",
  "image": "$image",
  "extensions": ["ETM_MULTIASSET_v1.0.0"],
  "assets": [
    {
      "media_type": "model",
      "files": [
        {
          "name": "${i}.vrm",
          "url": "$vrm_url",
          "file_type": "model/vrm"
        },
        {
          "name": "${i}_LOD0.glb",
          "url": "ipfs://$hash_lod0",
          "file_type": "model/gltf"
        },
        {
          "name": "${i}_LOD1.glb",
          "url": "ipfs://$hash_lod1",
          "file_type": "model/gltf"
        }
      ]
    }
  ],
  "background_color": "$background_color"
EOF
}
  
if $combine; then
  echo "[" > "$output_file"
fi

for i in {1..420}; do
  name=$(jq -r '.name' "$i".json)
  description=$(jq -r '.description' "$i".json)
  animation_url=$(jq -r '.animation_url' "$i".json)
  image=$(jq -r '.image' "$i".json)
  vrm_url=$(jq -r '.vrm_url' "$i".json)
  background_color=$(jq -r '.background_color' "$i".json)
  hash_lod0=$(grep -w "${i}_LOD0.glb" LOD0.txt | awk '{print $2}')
  hash_lod1=$(grep -w "${i}_LOD1.glb" LOD1.txt | awk '{print $2}')

  if $combine; then
    generate_json >> "$output_file"
    if [ "$i" -lt 420 ]; then
      echo "}," >> "$output_file"
    else
      echo "}" >> "$output_file"
      echo "]" >> "$output_file"
    fi
  elif $separate; then
    output_file="${i}_${suffix}.json"
    generate_json > "$output_file"
    echo "}" >> "$output_file"
  else
    generate_json
    echo "}"
  fi
done
