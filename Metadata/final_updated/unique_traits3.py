import json

with open('combined.json', 'r') as f:
    data = json.load(f)

# Collect all unique trait types
trait_types = set([attr.get('trait_type') for attr in data.get('attributes', [])])

# Construct output JSON for each unique trait type
output = {}
for trait_type in trait_types:
    traits = []
    for attr in data.get('attributes', []):
        if attr.get('trait_type') == trait_type:
            traits.append(attr.get('value'))
    output[trait_type] = {'values': list(set(traits)), 'count': len(traits)}

# Write output to file
with open('unique_traits.json', 'w') as f:
    json.dump(output, f, indent=2)
