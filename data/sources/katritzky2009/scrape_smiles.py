import json
from pathlib import Path
import pandas as pd
import pubchempy as pcp

df = pd.read_csv("source_data/katritzky2009_table_1.csv", skiprows=2)

index = {}
for i, row in df.iterrows():
    name = row.iloc[1]
    results = pcp.get_compounds(name, "name")
    index[name] = {}

    if len(results) > 0:
        mol = results[0]
        index[name]["inchi"] = mol.inchi
        index[name]["SMILES"] = mol.canonical_smiles

Path("source_data/names_to_identifiers.json").write_text(json.dumps(index))
