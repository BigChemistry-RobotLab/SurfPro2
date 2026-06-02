import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

df = pd.read_csv("source_data/abdel-lateef2016_table_1.csv")

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

df["CMC"] = df["CMC surface tension (mM/L)"] / 1000
df["pCMC"] = -np.log10(df.CMC)

df["Gamma_max"] = df["Γmax surface tension 10^11 (mol/cm2)"] / 10**7

df = df.rename(
    columns={
        "Compounds": "identifier",
        "Pi_CMC surface tension (mN/m)": "Pi_CMC",
        "γCMC surface tension (mN/m)": "AW_ST_CMC",
        "Amin surface tension (nm2)": "Area_min",
    }
)

df = df.drop(
    columns=[
        "CMC surface tension (mM/L)",
        "Γmax surface tension 10^11 (mol/cm2)",
        "CMC conductivity (mM/L)",
        "α conductivity",
        "β conductivity",
        "ΔGomic conductivity (kJ/mol)",
        "ΔGoads conductivity (kJ/mol)",
    ]
)


df.to_csv("processed_data/abdel-lateef2016.csv", index=False)
