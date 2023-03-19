#1/bin/bash

for file in $(ls *.glb | sort -n); do
  echo "Stats for $file"
  echo ""
  gltf-pipeline -i $file --stats
  echo "-----------------------"
done
