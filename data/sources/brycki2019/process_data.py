import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

# Compare to manual transcription
df = pd.read_csv("source_data/brycki2019_table_1.csv")
df2 = pd.read_csv("source_data/brycki2019_table_2.csv")

df = pd.concat([df,df2], axis=0)

# update the database with generated smiles
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

df["CMC"] = df["cmc (mM)"] / 1000
df["pCMC"] = -np.log10(df.CMC)
df = df.rename(columns={"Surfactant": "identifier"})

df = df.drop(
    columns=[
        "cmc (mM)",
        "cmc (mM) err",
        "α",
        "β",
        "DGomic (kJ/mol)",
        "n"
    ]
)

df = df[~(df.SMILES == "")]

df.to_csv("processed_data/brycki2019.csv", index=False)
