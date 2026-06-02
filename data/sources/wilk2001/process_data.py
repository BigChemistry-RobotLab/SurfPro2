import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

df = pd.read_csv("source_data/wilk2001_table_1.csv")

new_smiles_list = []
inchi_list = []
mol_wts = []
for i, row in df.iterrows():
    mol = Chem.MolFromSmiles(row.SMILES)
    smiles = Chem.MolToSmiles(mol)
    inchi = Chem.MolToInchi(mol)
    mw = Descriptors.MolWt(mol)

    new_smiles_list.append(smiles)
    inchi_list.append(inchi)
    mol_wts.append(mw)

df["SMILES"] = new_smiles_list
df["InChI"] = inchi_list
df["Molecular_Weight"] = mol_wts

df["Area_min"] = (df["1020 ACMC (m2)"] / 10**20) * 10**18
df["Gamma_max"] = df["106·ΓCMC (mol/m2)"] / 10**6

df = df.rename(
    columns={
        "Surfactant": "identifier",
        "γCMC (mN/m)": "AW_ST_CMC",
        "CMC (M)": "CMC",
    }
)

df["pCMC"] = -np.log10(df.CMC)

df = df.drop(
    columns=[
        "Krafft temp",
        "106·ΓCMC (mol/m2)",
        "1020 ACMC (m2)",
        "CMC/C20",
        "−∆G°CMC (kJ/mol)",
        "−∆G°CMC/CH2 (kJ/mol)",
        "−∆G°ads/CH2 (kJ/mol)",
        "−∆G°ads/CH2",
    ]
)


df.to_csv("processed_data/wilk2001.csv", index=False)
