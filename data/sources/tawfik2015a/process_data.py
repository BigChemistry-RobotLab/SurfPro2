import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE = "source_data/tawfik2015a_table_2.csv"
PROCESSED_FILE = "processed_data/tawfik2015a.csv"

df = pd.read_csv(SOURCE_FILE)

df["CMC"] = df["CMC M × 10−4"] / 10000
df["Gamma_max"] = df["Γmax × 10−11 mol.cm−2"] / 10**7
df["Area_min"] = df["Amin A°"] / 100

replace_columns = {
    "Compound": "identifier",
    "T °C": "Temp_Celsius",
    "πcmc mN−1m−1": "Pi_CMC",
    "Pc20 M/l": "pC20",
}

drop_columns = [
    "CMC M × 10−4",
    "Γmax × 10−11 mol.cm−2",
    "Amin A°",
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
