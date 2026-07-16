import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

# Compare to manual transcription
df1 = pd.read_csv("source_data/song2013_table_1.csv")
df2 = pd.read_csv("source_data/song2013_table_2.csv")

df = pd.concat([df1, df2], axis=0)

# update the database with generated smiles
new_smiles_list = []
inchi_list = []
reference_keys = []
reference_doi = []
mol_wts = []

for i, row in df.iterrows():
    code = row.Surfactant
    new_smiles = row.SMILES

    if pd.isna(row.SMILES):
        new_smiles_list.append("")
        inchi_list.append("")
        mol_wts.append("")
        continue

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
df["Temp_Celsius"] = df["Temperature (K)"] - 272.15
df["CMC"] = df["cac (mM)"] / 1000
df["pCMC"] = -np.log10(df.CMC)
df["Gamma_max"] = df["Γmax 10−10 (mol/cm2)"] / 10**6
df["Area_min"] = df["Amin (Å2)"] / 100
df["AW_ST_CMC"] = df["γcac (mN/m)"]

if "pC20" in df.columns:
    df["C20"] = 10**-df.pC20
elif "C20" in df.columns:
    df["pC20"] = -np.log10(df.C20)

df = df.rename(
    columns={
        "Surfactant": "identifier",
    }
)

df = df.drop(
    columns=[
        "Amin (Å2)",
        "Temperature (K)",
        "cac (mM)",
        "cac/c20",
        "pC20",
        "Γmax 10−10 (mol/cm2)",
        "ΔGagg (kJ/mol)",
        "ΔHagg (kJ/mol)",
        "β",
        "−TΔSagg (kJ/mol)",
        "γcac (mN/m)",
    ]
)

df = df[df.SMILES != ""]
df.to_csv("processed_data/song2013.csv", index=False)
