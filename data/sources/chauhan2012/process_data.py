import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE = "source_data/chauhan2012_table_1.csv"
PROCESSED_FILE = "processed_data/chauhan2012.csv"

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


df["CMC"] = df["CMC (mmol/L)"] / 1000
df["pCMC"] = -np.log10(df.CMC)

df["C20"] = df["C20 (10-4)"] / 10000
df["pC20"] = -np.log10(df.C20)

# Incorrect units? Orders of magnitude higher than other Γmax values
# df["Gamma_max"] = df["τmax (mol/m2)"]

df = df.rename(
    columns={
        "IL": "identifier",
        "γcmc (mN/m)": "AW_ST_CMC",
        "Amin (nm2)": "Area_min",
    }
)


df = df.drop(
    columns=[
        "CMC (mmol/L)",
        "CMC err (mmol/L)",
        "C20 (10-4)",
        "γcmc err (mN/m)",
        "∏CMC (mN/m)",
        "τmax (mol/m2)",
        "τmax err (mol/m2)",
        "Amin err (nm2)",
        "cmc/C20",
        "ΔG0mic (kJ/mol)",
        "ΔG0mic err (kJ/mol)",
        "ΔG0ads (kJ/mol)",
        "ΔG0ads (kJ/mol)",
        "ΔG0ads err (kJ/mol)",
        "α",
    ]
)

df = df[df.SMILES != ""]

df.to_csv(PROCESSED_FILE, index=False)
