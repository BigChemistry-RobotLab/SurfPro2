import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

df = pd.read_csv("source_data/abdel-salam2016_table_2.csv")
df = df[~df.SMILES.isna()]

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

df["CMC"] = df["cmc/ mmol L-1"] / 1000
df["pCMC"] = -np.log10(df.CMC)

df["Area_min"] = df["A 10^20 nm2"] / 100
df["Gamma_max"] = df["Γmax/10-10 (mol/cm2)"] / 10**6

df = df.rename(
    columns={
        "Surfactant": "identifier",
        "γcmc (mN/m)": "AW_ST_CMC",
    }
)

df = df.drop(
    columns=[
        "cmc/ mmol L-1",
        "Γmax/10-10 (mol/cm2)",
        "A 10^20 nm2",
        "cmc/C20",
        "ΔGmic (kJ/mol1)",
        "ΔGads (kJ/mol)",
        "I activity",
        "Peff",
        "pi_cmc",
    ]
)


df.to_csv("processed_data/abdel-salam2016.csv", index=False)
