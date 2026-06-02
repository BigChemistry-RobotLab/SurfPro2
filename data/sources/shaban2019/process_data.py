import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE = "source_data/shaban2019_table_1.csv"
PROCESSED_FILE = "processed_data/shaban2019.csv"

df = pd.read_csv(SOURCE_FILE)

df["CMC"] = df["CMC surface tension (mM)"] / 1000
df["C20"] = df["C20 (μmol)"] / 10**6
df["Gamma_max"] = df["Гmax *10−10 (mol.cm−2)"] / 10**6
df["Area_min"] = df["Amin/ A2"] / 100

replace_columns = {
    "Comp.": "identifier",
    "πCMC/ (mN m−1)": "Pi_CMC",
    "Temp. C": "Temp_Celsius",
}

drop_columns = [
    "CMC surface tension (mM)",
    "CMC conductometry (mM)",
    "α",
    "C20 (μmol)",
    "Гmax *10−10 (mol.cm−2)",
    "Amin/ A2",
    "CMC/C20",
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
