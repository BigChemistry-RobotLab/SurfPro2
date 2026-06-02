import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE = "source_data/shaban2016_table_1.csv"
PROCESSED_FILE = "processed_data/shaban2016.csv"

df = pd.read_csv(SOURCE_FILE)

df["CMC"] = df["CMC (mM L-1)"] / 1000
df["Gamma_max"] = df["Γmax x 10^11 (mol cm-2)"] / 10**7

replace_columns = {
    "Comp.": "identifier",
    "Temp. °C": "Temp_Celsius",
    "γCMC (mN m-1)": "AW_ST_CMC",
    "πCMC (mN m-1)": "Pi_CMC",
    "PC20 (mol L-1)": "pC20",
    "Amin nm2": "Area_min",
}

drop_columns = [
    "CMC (mM L-1)",
    "CMC err (mM L-1)",
    "γCMC err (mN m-1)",
    "γCMC err (mN m-1)",
    "πCMC err (mN m-1)",
    "CMC/C20",
    "CMC/C20 err",
    "PC20 err (mol L-1)",
    "Γmax x 10^11 (mol cm-2)",
    "Γmax err x 10^11 (mol cm-2)",
    "Amin err nm2",
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
