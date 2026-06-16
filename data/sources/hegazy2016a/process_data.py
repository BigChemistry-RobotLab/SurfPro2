import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE = "source_data/hegazy2016a_table_1.csv"
PROCESSED_FILE = "processed_data/hegazy2016a.csv"

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

df["CMC"] = df["Ccmc x 103 (M)"] / 1000
df["pCMC"] = -np.log10(df.CMC)

df["Gamma_max"] = (df["Γmax × 1010 (mol cm−2)"] / 10**10) * 10**4

df = df.rename(
    columns={
        "Surfactant name": "identifier",
        "γcmc (mN m−1)": "AW_ST_CMC",
        "πcmc (mN m−1)": "Pi_CMC",
        "Amin (nm2)": "Area_min",
    }
)


df = df.drop(
    columns=[
        "Ccmc x 103 (M)",
        "Γmax × 1010 (mol cm−2)",
        "β",
        "ΔG°mic (kJ mol−1)",
    ]
)

df = df[df.SMILES != ""]

df.to_csv(PROCESSED_FILE, index=False)
