import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

df = pd.read_csv("source_data/mulley1962_plot_digitised.csv")


new_smiles_list = []
inchi_list = []
mol_wts = []

for i, row in df.iterrows():
    new_smiles = row.SMILES
    mol = Chem.MolFromSmiles(new_smiles)
    smiles = Chem.MolToSmiles(mol)
    inchi = Chem.MolToInchi(mol)
    mw = Descriptors.MolWt(mol)

    new_smiles_list.append(smiles)
    inchi_list.append(inchi)
    mol_wts.append(mw)

df["SMILES"] = new_smiles_list
df["InChI"] = inchi_list
df["Molecular_Weight"] = mol_wts

df = df.rename(
    columns={
        "surface tension at CMC/ dyne cm-1": "AW_ST_CMC",
    }
)

df = df.drop(
    columns=[
        "glycol units",
        "Log(concentration)",
    ]
)

df.to_csv("processed_data/mulley1962.csv", index=False)
