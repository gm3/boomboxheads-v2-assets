$PACKETS_FILE=$args[0]
$OUTPUT_FILE=$args[1]

if (-not $PACKETS_FILE -or -not $OUTPUT_FILE) {
  Write-Host "Usage: ./convert_json.ps1 [PACKETS_FILE] [OUTPUT_FILE]"
  exit 1
}

New-Item -ItemType File -Path $OUTPUT_FILE -Force | Out-Null
Add-Content -Path $OUTPUT_FILE -Value "{" | Out-Null
Add-Content -Path $OUTPUT_FILE -Value '  "packets": [' | Out-Null

Get-Content $PACKETS_FILE | ForEach-Object {
  if ($_ -ne "") {
    if ((jq -e '.name and .created_by and .description and .vrm_url and .image and .external_url' <<< $_) -eq $true) {
      $name=$(jq -r '.name' <<< $_)
      $author=$(jq -r '.created_by' <<< $_)
      $description=$(jq -r '.description' <<< $_)
      $vrm_url=$(jq -r '.vrm_url' <<< $_)
      $image=$(jq -r '.image' <<< $_)
      $external_url=$(jq -r '.external_url' <<< $_)

      # Start packet dictionary
      Add-Content -Path $OUTPUT_FILE -Value "    {" | Out-Null
      Add-Content -Path $OUTPUT_FILE -Value "      `"name`": `"$name`"," | Out-Null
      Add-Content -Path $OUTPUT_FILE -Value "      `"author`": `"$author`"," | Out-Null
      Add-Content -Path $OUTPUT_FILE -Value "      `"description`": `"$description`"," | Out-Null
      Add-Content -Path $OUTPUT_FILE -Value "      `"vrm_url`": `"$vrm_url`"," | Out-Null
      Add-Content -Path $OUTPUT_FILE -Value "      `"image`": `"$image`"," | Out-Null
      Add-Content -Path $OUTPUT_FILE -Value "      `"external_url`": `"$external_url`"," | Out-Null

      # Extract values for each property in the array
      $properties=("Hat", "Eyes", "BodyTexture", "Pose", "BGColor", "BBTexture", "Border", "Back")
      $attribute_count=$(jq '.attributes | length' <<< $_)
      for ($i=0; $i -lt $attribute_count; $i++) {
        $trait_type=$(jq -r ".attributes[$i].trait_type" <<< $_)
        $value=$(jq -r ".attributes[$i].value" <<< $_)
        if ($i -eq $attribute_count-1) {
          # Last attribute, don't add a comma
          Add-Content -Path $OUTPUT_FILE -Value "      `"$trait_type`": `"$value`"" | Out-Null
        } else {
          # Not the last attribute, add a comma
          Add-Content -Path $OUTPUT_FILE -Value "      `"$trait_type`": `"$value`"," | Out-Null
        }
      }

      # End attributes dictionary
      Add-Content -Path $OUTPUT_FILE -Value "    }" | Out-Null

#      # End packet dictionary
#      Add-Content -Path $OUTPUT_FILE -Value "    }," | Out-Null
    }
  }
}

# Remove the trailing comma from the last packet
(Get-Content $OUTPUT_FILE)[$(Get-Content $OUTPUT_FILE).Count-1] = (Get-Content $OUTPUT_FILE)[-1].TrimEnd(',')

Add-Content -Path $OUTPUT_FILE -Value '  ]' | Out-Null
Add-Content -Path $OUTPUT_FILE -Value '}' | Out-Null

Write-Host "Conversion complete. Output written to $OUTPUT_FILE."
