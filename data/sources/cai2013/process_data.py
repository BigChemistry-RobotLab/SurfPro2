import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE_1 = "source_data/cai2013_table_1.csv"
SOURCE_FILE_2 = "source_data/cai2013_table_2.csv"
PROCESSED_FILE = "processed_data/cai2013.csv"

df1 = pd.read_csv(SOURCE_FILE_1)

df1["CMC"] = df1["CMC no salt (mM)"] / 1000

replace_columns = {
    "Surfactants": "identifier",
    "γ_CMC no salt (mN/m)": "AW_ST_CMC",
    "A_min no salt (nm2)": "Area_min",
}

drop_columns = [
    "CMC no salt (mM)",
    "CMC with salt (mM)",
    "γ_CMC with salt (mN/m)",
    "A_min with salt (nm2)",
    "CMC second breakpoint no salt (mM)",
    "CMC second breakpoint with salt (mM)",
    "γ_CMC second breakpoint no salt (mN/m)",
    "γ_CMC second breakpoint with salt (mN/m)",
]

df1 = df1.rename(columns=replace_columns)

df1 = df1.drop(columns=drop_columns)

df2 = pd.read_csv(SOURCE_FILE_2)

df2["CMC"] = df2["cmc mmol L-1"] / 1000

replace_columns = {
    "Surfactants": "identifier",
    "T (oC)": "Temp_Celsius",
}

drop_columns = [
    "cmc mmol L-1",
    "α",
    "β",
    "ΔG0m kJ mol-1",
    "ΔH0m kJ mol-1",
    "TΔS0m kJ mol-1",
]

df2 = df2.rename(columns=replace_columns)

df2 = df2.drop(columns=drop_columns)

df = pd.concat([df1, df2], axis=0)

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
