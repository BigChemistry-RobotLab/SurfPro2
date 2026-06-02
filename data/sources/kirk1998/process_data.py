import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE = "source_data/kirk1998_table_1.csv"
PROCESSED_FILE = "processed_data/kirk1998.csv"

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

df["CMC"] = df["CMC (10−4 mol/L)"] / 10000
df["pCMC"] = -np.log10(df.CMC)

df = df.rename(columns={"Compound": "identifier", "γmin (mN/m)": "AW_ST_CMC"})


df = df.drop(
    columns=[
        "n",
        "6-O-Acyl side chain",
        "CMC (10−4 mol/L)",
    ]
)

df = df[df.SMILES != ""]

df.to_csv(PROCESSED_FILE, index=False)
