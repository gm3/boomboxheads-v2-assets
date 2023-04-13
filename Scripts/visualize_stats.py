import plotly.express as px
import pandas as pd
import json

# Load CSV data
df = pd.read_csv('stats.csv')

# Create scatter plot
fig = px.scatter(df, x='Draw calls', y='Triangles', color='Name', hover_name='Name')

# Set layout and axis labels
fig.update_layout(title='3D Asset Stats', xaxis_title='Draw calls', yaxis_title='Triangles')

# Display plot
fig.show()

# Threshold for draw calls and triangles
dc_threshold, tri_threshold = map(int, input('Enter draw call and triangle count threshold (comma-separated): ').split(','))

# Get file names above the threshold
dc_above_threshold = df[df['Draw calls'] >= dc_threshold]['Name'].tolist()
tri_above_threshold = df[df['Triangles'] >= tri_threshold]['Name'].tolist()

# Output file names
output_format = input('Enter output format (CSV, JSON, LINES, ALL): ').lower()

if output_format == 'csv':
    with open('output.csv', 'w') as f:
        f.write('Name,Draw calls,Triangles\n')
        for i, row in df.iterrows():
            if row['Name'] in dc_above_threshold and row['Name'] in tri_above_threshold:
                f.write(f"{row['Name']},{row['Draw calls']},{row['Triangles']}\n")
    print('CSV file saved as output.csv')
elif output_format == 'json':
    file_data = []
    for i, row in df.iterrows():
        if row['Name'] in dc_above_threshold and row['Name'] in tri_above_threshold:
            file_data.append({'Name': row['Name'], 'Draw calls': row['Draw calls'], 'Triangles': row['Triangles']})
    with open('output.json', 'w') as f:
        json.dump(file_data, f, indent=4)
    print('JSON file saved as output.json')
elif output_format == 'lines':
    with open('output.txt', 'w') as f:
        for name in set(dc_above_threshold).intersection(tri_above_threshold):
            f.write(f"{name}\n")
    print('File names saved as output.txt')
elif output_format == 'all':
    with open('output.csv', 'w') as f:
        f.write('Name,Draw calls,Triangles\n')
        for i, row in df.iterrows():
            if row['Name'] in dc_above_threshold and row['Name'] in tri_above_threshold:
                f.write(f"{row['Name']},{row['Draw calls']},{row['Triangles']}\n")
    print('CSV file saved as output.csv')

    file_data = []
    for i, row in df.iterrows():
        if row['Name'] in dc_above_threshold and row['Name'] in tri_above_threshold:
            file_data.append({'Name': row['Name'], 'Draw calls': row['Draw calls'], 'Triangles': row['Triangles']})
    with open('output.json', 'w') as f:
        json.dump(file_data, f, indent=4)
    print('JSON file saved as output.json')

    with open('output.txt', 'w') as f:
        for name in set(dc_above_threshold).intersection(tri_above_threshold):
            f.write(f"{name}\n")
    print('File names saved as output.txt')
else:
    print('Invalid output format. Valid options are: CSV, JSON, LINES, ALL')

