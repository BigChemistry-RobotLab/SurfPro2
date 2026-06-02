import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE = "source_data/dreja1999_table_1.csv"
PROCESSED_FILE = "processed_data/dreja1999.csv"

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


df["CMC"] = df["cmc (10-4 mol‚L-1)"] / 10000
df["pCMC"] = -np.log10(df.CMC)

df = df.rename(
    columns={
        "γcmc (mN‚m-1)": "AW_ST_CMC",
        "asur (n = 3) (nm2)": "Area_min",
    }
)


df = df.drop(
    columns=[
        "x in 12-EOx-12",
        "cmc (10-4 mol‚L-1)",
        "-[dγ/d log c]T",
        "asur (n = 2) (nm2)",
        "asur (SANS) (nm2)",
        "asur (SANS) 10 wt% (nm2)",
    ]
)

df = df[df.SMILES != ""]
df.to_csv(PROCESSED_FILE, index=False)
