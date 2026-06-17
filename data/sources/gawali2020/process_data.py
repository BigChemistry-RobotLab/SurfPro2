import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE = "source_data/gawali2020_table_1.csv"
PROCESSED_FILE = "processed_data/gawali2020.csv"

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

df["CMC"] = df["CMC 10^3 (mol/L)"] / 1000
df["pCMC"] = -np.log10(df.CMC)

df["C20"] = df["C20 10^3 (mol/L)"] / 1000
df["pC20"] = -np.log10(df.C20)

df["Gamma_max"] = df["Γmax 10^11 (mol/cm2)"] / 10**7

df = df.rename(
    columns={
        "Compounds Name": "identifier",
        "γCMC (mN/m)" : "AW_ST_CMC",
        "πCMC (mN/m)": "Pi_CMC",
        "Amin (nm2)": "Area_min",
    }
)


df = df.drop(
    columns=[
        "CMC 10^3 (mol/L)",
        "Γmax 10^11 (mol/cm2)",
        "C20 10^3 (mol/L)",
        "PC20 (mol/L)",
        "cmc/C20",
        "ΔGmic (KJ/mol)",
        "ΔGads (KJ/mol)",
    ]
)

df = df[df.SMILES != ""]

df.to_csv(PROCESSED_FILE, index=False)
