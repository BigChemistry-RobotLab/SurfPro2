import pandas as pd
import json
from pathlib import Path
import pubchempy as pcp
from rdkit import Chem


df = pd.read_csv("source_data/gaudin2018_table_2.csv")
names = df.Surfactant.to_list()

index = dict()
for name_orig in names:
    name = name_orig.replace(" ", "")
    name = name.replace("α", "alpha")
    name = name.replace("β", "beta")
    results = pcp.get_compounds(name, "name")
    if index.get(name_orig) is None:
        index[name_orig] = {}
    if len(results) > 0:
        mol = results[0]
        index[name_orig]["inchi"] = mol.inchi
        index[name_orig]["SMILES"] = mol.canonical_smiles
    else:
        results = pcp.get_compounds(name_orig, "name")
        if index.get(name_orig) is None:
            index[name_orig] = {}
        if len(results) > 0:
            mol = results[0]
            index[name_orig]["inchi"] = mol.inchi
            index[name_orig]["SMILES"] = mol.canonical_smiles

for n in index:
    smiles = index[n].get("SMILES")
    inchi = index[n].get("inchi")

    if smiles is None:
        if inchi is not None:
            mol = Chem.MolFromInchi(inchi)
            sm = Chem.MolToSmiles(mol)
            index[n]["SMILES"] = sm
        else:
            print(n)
    elif inchi is None:
        mol = Chem.MolFromSmiles(smiles)
        inchi = Chem.MolToInchi(mol)
        index[n]["inchi"] = inchi

Path("source_data/names_to_identifiers.json").write_text(json.dumps(index, indent=4))
