import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors


# Compare to manual transcription
df = pd.read_csv("source_data/zhang2022c_table_1.csv")

df = df.iloc[[0, -1], :]

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

df["CMC"] = df["CMC (mmol/L)"] / 1000
df["pCMC"] = -np.log10(df.CMC)
df["Gamma_max"] = df["Γmax"] / 1000000

df = df.rename(
    columns={
        "γCMC": "AW_ST_CMC",
        "Amin": "Area_min",
        "∏CMC (mN/m)": "Pi_CMC",
    }
)

df = df.drop(
    columns=[
        "CMC (mmol/L)",
        "ratio_SLG",
        "Aideal min",
        "DG0m (kJ/mol)",
        "DG0 ads (kJ/mol)",
    ]
)

df.to_csv("processed_data/zhang2022c.csv", index=False)
