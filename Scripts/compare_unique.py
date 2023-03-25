import os
import json
from itertools import combinations
try:
    import termcolor
except ImportError:
    print("termcolor is not installed.")
    print("You can install it by running: pip install termcolor")
    exit(1)




# Get a list of all the JSON files in the current directory
json_files = [file for file in os.listdir() if file.endswith('.json')]

# Load the attributes from each file
attributes = {}
for file in json_files:
    with open(file, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
        attributes[file] = tuple(attr_dict['value'] for attr_dict in data['attributes'])

# Compare the attributes of all the files
similarity_scores = []
for file1, file2 in combinations(attributes.keys(), 2):
    similarity = len(set(attributes[file1]).intersection(attributes[file2])) / len(attributes[file1])
    similarity_scores.append((file1, file2, similarity))

# Sort the similarity scores and print the top and bottom 20
similarity_scores.sort(key=lambda x: x[2], reverse=True)
num_files = len(json_files)

print("Top 20 similarity scores:")
for i, (file1, file2, score) in enumerate(similarity_scores[:20]):
    rank = i + 1
    percent = score * 100
    print(f"{rank}. {file1} and {file2}: {percent:.2f}% similarity")

print("Bottom 20 similarity scores:")
for i, (file1, file2, score) in enumerate(similarity_scores[-20:]):
    rank = num_files - 20 + i + 1
    percent = score * 100
    print(f"{rank}. {file1} and {file2}: {percent:.2f}% similarity")

# Ask the user if they want to see a colordiff
while True:
    choice = input("Enter the number of two files to compare, or 'q' to quit: ")
    if choice.lower() == 'q':
        break

    try:
        file1, file2 = similarity_scores[int(choice) - 1][:2]
        with open(file1, 'r', encoding='utf-8-sig') as f:
            data1 = json.load(f)
        with open(file2, 'r', encoding='utf-8-sig') as f:
            data2 = json.load(f)

        for attr1, attr2 in zip(data1['attributes'], data2['attributes']):
            trait_type = attr1['trait_type']
            value1 = attr1['value']
            value2 = attr2['value']
            if value1 != value2:
                print(f"{trait_type}:")
                print(colored(f"{value1} (file 1)", 'red'))
                print(colored(f"{value2} (file 2)", 'green'))
                print()
    except:
        print("Invalid input.")
