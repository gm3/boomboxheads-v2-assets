import json

# define the color map
color_map = {
    "Blue": "0000FF",
    "Green": "008000",
    "Purple": "800080",
    "Teal": "008080",
    "White": "FFFFFF",
    "Yellow": "FFFF00",
    "Black": "000000",
    "Orange": "FFA500",
    "Pink": "FFC0CB",
    "LightGreen": "90EE90",
    "Red": "FF0000",
    "Golden": "FFD700"
}

# read the JSON file
with open('combined.json') as f:
    data = json.load(f)

# add the background_color field to each object
for obj in data:
    bg_color = obj['attributes'][4]['value']
    hex_color = color_map.get(bg_color, '')
    obj['background_color'] = hex_color

# Move the "background_color" key to be the last item in the dictionary for each element in the list
for item in data:
    background_color = item.pop("background_color")
    item["background_color"] = background_color

# write the updated JSON file
with open('combined_updated.json', 'w') as f:
    json.dump(data, f, indent=2)
