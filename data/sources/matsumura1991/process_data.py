import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE = "source_data/matsumura1992_table_2.csv"
PROCESSED_FILE = "processed_data/matsumura1991.csv"

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

df["CMC"] = df["cmc (mM)"] / 1000
df["pCMC"] = -np.log10(df.CMC)

df["Area_min"] = df["Amin x 10^2 (nm2)"] / 100

df = df.rename(
    columns={
        "Compound": "identifier",
        "γCMC (mN/m)": "AW_ST_CMC",
        "∏cmc (mN/m)": "Pi_CMC",
    }
)


df = df.drop(
    columns=[
        "cmc (mM)",
        "Amin x 10^2 (nm2)",
        "note",
    ]
)

df = df[df.SMILES != ""]

df.to_csv(PROCESSED_FILE, index=False)
