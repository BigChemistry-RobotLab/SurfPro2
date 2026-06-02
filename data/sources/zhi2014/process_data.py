import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

df = pd.read_csv("source_data/zhi2014_table_1.csv")

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

df["CMC"] = df["cmc (mmol/L)"] / 1000
df["pCMC"] = -np.log10(df.CMC)
df["Area_min"] = df["Amin (Å2)"] / 100
df["Gamma_max"] = df["Γmax x 10^-10 (mol cm−2)"] / 10**6

df = df.rename(
    columns={
        "Surfactant": "identifier",
        "γcmc (mN/m)": "AW_ST_CMC",
    }
)

df = df.drop(
    columns=[
        "cmc (mmol/L)",
        "cmc/C20",
        "Γmax x 10^-10 (mol cm−2)",
        "Amin (Å2)",
    ]
)

df = df[df.SMILES != ""]


df.to_csv("processed_data/zhi2014.csv", index=False)
