import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE_1 = "source_data/zheng2021_table_1.csv"
SOURCE_FILE_2 = "source_data/zheng2021_table_2.csv"
PROCESSED_FILE = "processed_data/zheng2021.csv"

df1 = pd.read_csv(SOURCE_FILE_1)
df2 = pd.read_csv(SOURCE_FILE_2)

df = pd.concat([df1, df2], axis=0)

df["CMC"] = df["CMC (mM/L)"] / 1000
df["Gamma_max"] = df["Γ (μmol/m2)"] / 10**6
df["Temp_Celsius"] = df["Temperature (K)"] - 273.15
df["Gamma_max"] = df["Γ (μmol/m2)"] / 10**6

replace_columns = {
    "Surfactant": "identifier",
    "Amin (nm2)": "Area_min",
    "γcmc (mN/M)": "AW_ST_CMC",
}

drop_columns = [
    "-TΔSmic (kJ/mol)",
    "CMC (mM/L)",
    "Temperature (K)",
    "Γ (μmol/m2)",
    "ΔGads (kJ/mol)",
    "ΔGmic (kJ/mol)",
    "ΔHmic (kJ/mol)",
    "β",
]

df = df.rename(columns=replace_columns)

df = df.drop(columns=drop_columns)

if "CMC" in df.columns:
    df["pCMC"] = -np.log10(df.CMC)
elif "pCMC" in df.columns:
    df["CMC"] = 10**-df.pCMC

if "pC20" in df.columns:
    df["C20"] = 10**-df.pC20
elif "C20" in df.columns:
    df["pC20"] = -np.log10(df.C20)

smiles_list = []
inchi_list = []
mol_wts = []
for i, row in df.iterrows():
    smiles = row.SMILES

    if pd.isna(smiles):
        mol = None
        smiles = ""
        inchi = ""
        mw = np.nan
    else:
        mol = Chem.MolFromSmiles(smiles)
        smiles = Chem.MolToSmiles(mol)
        inchi = Chem.MolToInchi(mol)
        mw = Descriptors.MolWt(mol)

    smiles_list.append(smiles)
    inchi_list.append(inchi)
    mol_wts.append(mw)

df["SMILES"] = smiles_list
df["Molecular_Weight"] = mol_wts
df["InChI"] = inchi_list

df = df[df.SMILES != ""]

df.to_csv(PROCESSED_FILE, index=False)
