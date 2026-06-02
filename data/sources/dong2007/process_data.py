import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE = "source_data/dong2007_table_3.csv"
PROCESSED_FILE = "processed_data/dong2007.csv"

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


df["CMC"] = df["cmc (mmol/L)"] / 1000
df["pCMC"] = -np.log10(df.CMC)

df["C20"] = 10**-df.pC20

df["Gamma_max"] = df["Γmax (μmol/m2)"] / 1000000
df["Area_min"] = df["Amin (Å2)"] / 100

df = df.rename(
    columns={
        "ILs": "identifier",
        "γcmc (mN/m)": "AW_ST_CMC",
        "Πcmc (mN/m)": "Pi_CMC",
    }
)


df = df.drop(columns=["cmc (mmol/L)", "Γmax (μmol/m2)", "Amin (Å2)"])

df = df[df.SMILES != ""]

df.to_csv(PROCESSED_FILE, index=False)
