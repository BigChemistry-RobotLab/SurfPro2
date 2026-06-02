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

df["CMC"] = df["Ccmc surface tension x 103 (M)"] / 1000
df["pCMC"] = -np.log10(df.CMC)

df["Gamma_max"] = (df["Γmax × 1010 surface tension (mol cm−2)"] / 10**10) * 10**4

df = df.rename(
    columns={
        "Surfactant name": "identifier",
        "γcmc surface tension (mN m−1)": "AW_ST_CMC",
        "πcmc surface tension (mN m−1)": "Pi_CMC",
        "Amin conductivity (nm2)": "Area_min",
    }
)


df = df.drop(
    columns=[
        "Ccmc surface tension x 103 (M)",
        "Γmax × 1010 surface tension (mol cm−2)",
        "Ccmc conductivity × 103 (M)",
        "β conductivity",
        "ΔG°mic conductivity (kJ mol−1)",
    ]
)

df = df[df.SMILES != ""]

df.to_csv(PROCESSED_FILE, index=False)
