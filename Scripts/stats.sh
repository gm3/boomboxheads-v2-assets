#!/bin/bash

# Set default units to MB
units="MB"

# Define function to print help menu
print_help() {
  echo "Usage: $0 [DIRECTORY] [UNIT]"
  echo "Get statistics of glTF files in a directory and output as CSV."
  echo "  DIRECTORY  Path to the directory containing the glTF files to analyze."
  echo "  UNIT       Units to use for displaying size. Options: B, KB, MB (default: MB)"
}

# Check if help flag was provided
if [ "$1" = "-h" ] || [ "$1" = "--help" ]
then
  print_help
  exit 0
fi

# Check if a directory was provided as a command-line argument
if [ -z "$1" ]
then
  echo "Error: directory not provided"
  echo
  print_help
  exit 1
fi

# Check if a unit was provided as a command-line argument
if [ -n "$2" ]
then
  case $2 in
    B | b)
      units="B"
      ;;
    KB | kb)
      units="KB"
      ;;
    MB | mb)
      units="MB"
      ;;
    *)
      echo "Error: invalid unit specified"
      echo
      print_help
      exit 1
      ;;
  esac
fi

# Output header row to CSV file
echo "Name,Size,Images,Draw calls,Triangles" > stats.csv

# Loop over each glb file in the directory and get its stats
find "$1" -name "*.glb" -print0 | while read -d $'\0' file
do
  # Get the statistics from the glTF file and store them in variables
  stats=$(gltf-pipeline -i "$file" --stats)
  total_byte_length=$(echo "$stats" | grep 'Total byte length of all buffers' | awk '{print $(NF-1)}')
  num_images=$(echo "$stats" | grep 'Images:' | awk '{print $NF}')
  num_draw_calls=$(echo "$stats" | grep 'Draw calls:' | awk '{print $NF}')
  num_triangles=$(echo "$stats" | grep 'Rendered primitives' | awk '{print $NF}' | sed 's/,//g')

  # Convert the byte length to the specified units
  case $units in
    B)
      size="$total_byte_length B"
      ;;
    KB)
      size=$(echo "scale=2; $total_byte_length / 1024" | bc)" KB"
      ;;
    MB)
      size=$(echo "scale=2; $total_byte_length / 1048576" | bc)" MB"
      ;;
  esac

  # Output the results to CSV file
  echo "$(basename "$file"),$size,$num_images,$num_draw_calls,$num_triangles" >> stats.csv
done
