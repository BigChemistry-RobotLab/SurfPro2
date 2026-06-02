import pandas as pd
import json
from pathlib import Path
import pandas as pd
import pubchempy as pcp
from rdkit import Chem


df = pd.read_csv("names.csv")
names = df.name.to_list()

index = {
    "octyl-D,L-glycerol": {
        "SMILES": "CCCCCCCCOCC(O)CO",
        "inchi": "InChI=1S/C11H24O3/c1-2-3-4-5-6-7-8-14-10-11(13)9-12/h11-13H,2-10H2,1H3",
    },
    "octylglycol": {
        "SMILES": "CCCCCCCCOCCO",
        "inchi": "InChI=1S/C10H22O2/c1-2-3-4-5-6-7-9-12-10-8-11/h11H,2-10H2,1H3",
    },
}
for name in names:
    name = name.replace(" ", "")
    name = name.replace("α", "alpha")
    name = name.replace("β", "beta")
    results = pcp.get_compounds(name, "name")
    if index.get(name) is None:
        index[name] = {}
    if len(results) > 0:
        mol = results[0]
        index[name]["inchi"] = mol.inchi
        index[name]["SMILES"] = mol.canonical_smiles

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

Path("names_to_identifiers.json").write_text(json.dumps(index, indent=4))
