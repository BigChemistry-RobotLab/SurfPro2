import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE_1 = "source_data/kim1996_table_1.csv"
SOURCE_FILE_2 = "source_data/kim1996_table_1.csv"
PROCESSED_FILE = "processed_data/kim1996.csv"

df = pd.read_csv(SOURCE_FILE_1)
df2 = pd.read_csv(SOURCE_FILE_2)

df = pd.concat([df, df2], axis=0)

smiles_list = []
inchi_list = []
mol_wts = []
for i, row in df.iterrows():
    if pd.isna(row.SMILES):
        smiles_list.append("")
        inchi_list.append("")
        mol_wts.append("")
    else:
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

df = df.rename(
    columns={
        "Compound": "identifier",
        "CMC (M)": "CMC",
        "γCMC (mN/m)": "AW_ST_CMC",
    }
)

df["C20"] = 10**-df.pC20
df["pCMC"] = -np.log10(df.CMC)


df = df.drop(
    columns=[
        "R",
        "Krafft point (oC)",
        "Foam 0' (mL)",
        "Foam 30' (mL)",
    ]
)


df = df[df.SMILES != ""]
df = df.sort_values("identifier")
df = df.drop_duplicates()

df.to_csv(PROCESSED_FILE, index=False)
