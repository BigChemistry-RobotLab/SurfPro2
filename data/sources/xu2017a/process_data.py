import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE = "source_data/xu2017_table_1.csv"
PROCESSED_FILE = "processed_data/xu2017a.csv"

df = pd.read_csv(SOURCE_FILE)

df["CMC"] = df["CMC tensiometry (mM)"] / 1000
df["Gamma_max"] = df["Γmax (μmol/m2)"] / 10**6

replace_columns = {
    "Compounds": "identifier",
    "ΠCMC (mN/m)": "Pi_CMC",
    "Amin (nm2)": "Area_min",
    "γCMC (mN/m)": "AW_ST_CMC",
}

drop_columns = [
    "CMC tensiometry (mM)",
    "CMC tensiometry err (mM)",
    "CMC conductometry (mM)",
    "CMC conductometry err (mM)",
    "Γmax (μmol/m2)",
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
