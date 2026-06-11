import json
from string import Template

temp = Template(
    "${R}c1ccc(NC(=O)C[N+](C)(C)${S}[N+](C)(C)CC(=O)Nc2ccc(O${R})cc2)cc1.[Br-].[Br-]"
)

codes = {
    "8-2-8": (8, 2),
    "8-4-8": (8, 4),
    "8-6-8": (8, 6),
    "10-2-10": (10, 2),
    "10-4-10": (10, 4),
    "10-6-10": (10, 6),
    "12-2-12": (12, 2),
    "12-4-12": (12, 4),
    "12-6-12": (12, 6),
    "14-2-14": (14, 2),
    "14-4-14": (14, 4),
    "14-6-14": (14, 6),
    "16-2-16": (16, 2),
    "16-4-16": (16, 4),
    "16-6-16": (16, 6),
}

results = {}
for c in codes:
    smiles = temp.substitute(R=codes[c][0]*"C", S=codes[c][1]*"C")
    results[c] = smiles

output = json.dumps(results, indent=4)

with open("source_data/code_to_smiles.json", "w") as file:
    file.write(output)
