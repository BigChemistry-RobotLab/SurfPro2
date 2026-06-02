import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE = "source_data/zhou2007a_table_1.csv"
PROCESSED_FILE = "processed_data/zhou2007a.csv"

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

df["CMC"] = df["cmc tensiometry (mM)"] / 1000
df["pCMC"] = -np.log10(df.CMC)
df["Gamma_max"] = df["106Γmax (mol/m2)"] / 1000000
df["C20"] = df["C20 (mM)"] / 1000
df["pC20"] = 10 ** (df.C20)

df = df.rename(
    columns={
        "γcmc (mN/m)": "AW_ST_CMC",
        "Amin (nm2/mol)": "Area_min",
    }
)


df = df.drop(
    columns=[
        "surfactant",
        "cmc tensiometry (mM)",
        "cmc fluorometry (mM)",
        "C20 (mM)",
        "106Γmax (mol/m2)",
        "γcac (mN/m)",
        "cac tensiometry (mM)",
        "cac fluorometry (mM)",
    ]
)

df = df[df.SMILES != ""]
df.to_csv(PROCESSED_FILE, index=False)
