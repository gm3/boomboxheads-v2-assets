import json

# Load the input JSON file
with open('combined.json', 'r') as f:
    data = json.load(f)

# Get all unique trait types
trait_types = set([attr['trait_type'] for attr in data['attributes']])

# Extract attributes for each unique trait type
packets = []
for trait_type in trait_types:
    packet = {
        'name': data['name'],
        'created_by': data['created_by'],
        'description': data['description'],
        'vrm_url': data['vrm_url'],
        'image': data['image'],
        'external_url': data['external_url']
    }
    for attr in data['attributes']:
        if attr['trait_type'] == trait_type:
            packet[trait_type] = attr['value']
    packets.append(packet)

# Construct the output JSON
output = {'packets': packets}

# Write the output to a file
with open('output.json', 'w') as f:
    json.dump(output, f)

