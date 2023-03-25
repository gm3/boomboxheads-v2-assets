#!/bin/bash

# Convert Base58btc to Base32 CIDs for files in directory

# Loop through each line in the input file
while read line; do
    # Extract the filename and CID from the line
    filename=$(echo $line | awk '{print $1}')
    cid=$(echo $line | awk '{print $2}')
    
    # Convert the CID from Base58btc to Base32
    cid_base32=$(ipfs cid base32 $cid)
    
    # Print the filename and converted CID, separated by a space
    echo "$filename $cid $cid_base32"
done < cids3.txt
