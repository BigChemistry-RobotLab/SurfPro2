import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

df = pd.read_csv("source_data/he2014_table_1.csv")

df = df[df.SMILES != "not digitised"]

new_smiles_list = []
inchi_list = []
mol_wts = []
for i, row in df.iterrows():
    mol = Chem.MolFromSmiles(row.SMILES)
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
df["Area_min"] = df["am (Å2)"] / 100
df["Gamma_max"] = df["Γ × 1010 (mol/cm2)"] / 10**6

df = df.rename(
    columns={
        "Surfactant": "identifier",
        "γcmc (mN/m)": "AW_ST_CMC",
        "Temp": "Temp_Celsius",
        "Ref_all": "source_doi",
    }
)

df = df.drop(
    columns=[
        "cmc (mmol/L)",
        "cmc/C20",
        "TK (◦C)",
        "Γ × 1010 (mol/cm2)",
    ]
)


df.to_csv("processed_data/he2014.csv", index=False)
