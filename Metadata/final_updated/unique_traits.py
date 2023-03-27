import json

# Load the data from the combined.json file
with open('combined.json', 'r') as f:
    data = json.load(f)

# Collect all the attributes and their values into a dictionary
attributes = {}
for item in data:
    for attribute in item['attributes']:
        trait_type = attribute['trait_type']
        value = attribute['value']
        if trait_type not in attributes:
            attributes[trait_type] = set()
        attributes[trait_type].add(value)

# Sort the attributes by the number of unique values they have
sorted_attributes = sorted(attributes.items(), key=lambda x: len(x[1]), reverse=True)

# Print the sorted attributes and their unique values
for attribute, values in sorted_attributes:
    print(f"{attribute}: {len(values)} unique values")
    print(values)
