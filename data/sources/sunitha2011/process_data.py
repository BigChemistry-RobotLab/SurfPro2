import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

df = pd.read_csv("source_data/sunitha2011_table_1.csv")

df = df[df.SMILES != "not digitised"]

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

df["CMC"] = df["cmc 10^3 (mM)"] / 1000
df["pCMC"] = -np.log10(df.CMC)

df["Area_min"] = df["Amin (A ̊ 2)"] / 100
df["Gamma_max"] = df["Γmax 1012 (mol/mm2)"]/10**6

df = df.rename(
    columns={
        "compound": "identifier",
        "γcmc (mN/m)": "AW_ST_CMC",
    }
)

df = df.drop(
    columns=[
        "cmc 10^3 (mM)",
        "cmc err",
        "γcmc err",
        "Γmax 1012 (mol/mm2)",
        "Γmax err",
        "Amin (A ̊ 2)",
        "Amin err",
    ]
)


df.to_csv("processed_data/sunitha2011.csv", index=False)
