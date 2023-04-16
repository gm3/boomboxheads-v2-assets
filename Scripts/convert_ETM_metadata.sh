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
{"name": "$name", "created_by": "$created_by", "external_url": "$external_url", "description": "$description https://github.com/gm3/boom-tools","metadataStandard": "ETM_v1.0.0","animation_url": "$animation_url","image": "ipfs://$preview_hash","extensions": ["ETM_ATTRIBUTES_v1.0.0", "ETM_MULTIASSET_v1.0.0"],"assets": [{"media_type": "model","files": [{"name": "${i}.vrm","url": "$vrm_url","file_type": "model/vrm"},{"name": "$name HD","url": "$image","file_type": "image/jpeg"},{"name": "${i}_LOD0.glb","description": "$desc_lod0","url": "ipfs://$hash_lod0","file_type": "model/gltf-binary"},{"name": "${i}_LOD1.glb","description": "$desc_lod1","url": "ipfs://$hash_lod1","file_type": "model/gltf-binary"}]}],"attributes": [$attributes],"background_color": "$background_color"}
EOF
}
  
if $combine; then
  echo "[" > "$output_file"
fi

count=0
while read i; do
  name=$(jq -r '.name' "$i".json)
  description=$(jq -r '.description' "$i".json)
  animation_url=$(jq -r '.animation_url' "$i".json)
  external_url=$(jq -r '.external_url' "$i".json)
  created_by=$(jq -r '.created_by' "$i".json)
  image=$(jq -r '.image' "$i".json)
  preview_hash=$(grep -w "boomboxhead${i}.jpg" hd_images.txt | awk '{print $1}')
  vrm_url=$(jq -r '.vrm_url' "$i".json)
  attributes=$(jq -c '.attributes[]' "$i".json | paste -sd "," -)
  background_color=$(jq -r '.background_color' "$i".json)
  hash_lod0=$(grep -w "${i}_LOD0.glb" LOD0.txt | awk '{print $2}')
  hash_lod1=$(grep -w "${i}_LOD1.glb" LOD1.txt | awk '{print $2}')
  desc_lod0=$(echo "lodRatio 0.5, average size 1.3 MB")
  desc_lod1=$(echo "lodRatio 0.1, average size 118 KB")

  if $combine; then
    if [ "$count" -eq 0 ]; then
      echo "["
    fi
    if [ "$count" -lt 419 ]; then
      generate_json | sed '$ s/}$/},/'
      (( count++ ))
    else
      generate_json
      echo "]"
      break  # break the loop if $combine flag is set and count reaches 420
    fi
  fi

  if $separate; then
    output_file="${i}_${suffix}.json"
    generate_json > "$output_file"
    if [ "$count" -eq 420 ]; then

      break  # break the loop if $separate flag is set and count reaches 420
    fi
  fi
done < <(seq 1 420)
