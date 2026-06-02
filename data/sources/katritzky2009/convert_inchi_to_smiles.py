import json
from pathlib import Path
from rdkit import Chem

text = Path("source_data/names_to_identifiers.json").read_text()

index = json.loads(text)

output = []
for i in index:
    inchi = index[i].get("inchi")
    if inchi:
        mol = Chem.MolFromInchi(inchi)
        smiles = Chem.MolToSmiles(mol)
        output.append((f'"{i}"', f'"{inchi}"', smiles))
    else:
        output.append((f'"{i}"', "", ""))

out_text = "\n".join([",".join(v) for v in output])

Path("source_data/names_to_smiles.csv").write_text(out_text)
