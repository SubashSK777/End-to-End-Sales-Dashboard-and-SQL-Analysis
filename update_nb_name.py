import json

notebook_path = 'sales_analysis.ipynb'
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Replace in cells
for cell in nb['cells']:
    if 'source' in cell:
        new_source = []
        for line in cell['source']:
            new_source.append(line.replace('CargoTrack', 'End-to-End Sales Dashboard + SQL Analysis'))
        cell['source'] = new_source

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print("Project name updated in notebook.")
