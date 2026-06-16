import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE = "source_data/li2014d_table_1.csv"
PROCESSED_FILE = "processed_data/li2014d.csv"

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

df["Gamma_max"] = df["Γ∞ (10−6 mol m−2)"] / 1000000

df = df.rename(
    columns={
        "Surfactant": "identifier",
        "γmc (mN m−1)": "AW_ST_CMC",
        "Amin (nm2)": "Area_min",
    }
)


df = df.drop(
    columns=[
        "identifier",
        "cmc (mM)",
        "cmc err (mM)",
        "Γ∞ (10−6 mol m−2)",
        "α",
        "α err",
    ]
)

df = df[df.SMILES != ""]

df.to_csv(PROCESSED_FILE, index=False)
