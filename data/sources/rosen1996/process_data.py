import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

df = pd.read_csv("source_data/rosen1996_table_1.csv")

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

df["Area_min"] = df["Amin 10^2/ nm2"] / 100
df["Gamma_max"] = df["Gamma_max 10^10/ mol/cm2"] / 10**6

df = df.rename(
    columns={
        "compound": "identifier",
        "CMC/ mol/dm3": "CMC",
        "temperature": "Temp_Celsius",
        "γ_CMC/ mN/m": "AW_ST_CMC",
    }
)

df["pCMC"] = -np.log10(df.CMC)

df = df[df.Medium == "H2O"]

df = df.drop(
    columns=[
        "Medium",
        "Gamma_max 10^10/ mol/cm2",
        "Amin 10^2/ nm2",
    ]
)

if "CMC" in df.columns:
    df["pCMC"] = -np.log10(df.CMC)
elif "pCMC" in df.columns:
    df["CMC"] = 10**-df.pCMC

if "pC20" in df.columns:
    df["C20"] = 10**-df.pC20
elif "C20" in df.columns:
    df["pC20"] = -np.log10(df.C20)

df = df[df.SMILES != ""]

df.to_csv("processed_data/rosen1996.csv", index=False)
