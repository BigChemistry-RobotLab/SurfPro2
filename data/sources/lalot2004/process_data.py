import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE = "source_data/lalot2004_table_2.csv"
PROCESSED_FILE = "processed_data/lalot2004.csv"

df = pd.read_csv(SOURCE_FILE)

smiles_list = []
inchi_list = []
mol_wts = []
for i, row in df.iterrows():
    smiles = row.SMILES
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


df["CMC"] = df["CMC (10−3 M)"] / 1000
df["pCMC"] = -np.log10(df.CMC)

df["C20"] = 10**-df.pC20

df["Gamma_max"] = (df["1010Γ (mol cm−2)"] / 10**10)*10000
df["Area_min"] = df["A0 (Å2 mol−1)"]/100

df = df.rename(
    columns={
        "Amin/ nm2": "Area_min",
        "γ (mN m−1)":"AW_ST_CMC",
    }
)


df = df.drop(
    columns=[
        "Surfactant",
        "Code",
        "n",
        "CMC (10−3 M)",
        "1010Γ (mol cm−2)",
        "CPP",
        "A0 (Å2 mol−1)",
    ]
)

df = df[df.SMILES != ""]

df.to_csv(PROCESSED_FILE, index=False)
