import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE = "source_data/chauhan2014_table_1.csv"
PROCESSED_FILE = "processed_data/chauhan2014.csv"

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

df["CMC"] = df["CMC mM"] / 1000
df["pCMC"] = -np.log10(df.CMC)

df["C20"] = df["C20 (10-4)"] / 10000
df["pC20"] = -np.log10(df.C20)

df["Gamma_max"] = df["Γmax (μmol/m2)"]/1000000

df = df.rename(
    columns={
        "Surfactant": "identifier",
        "γcmc (mN/m)": "AW_ST_CMC",
        "Amin (nm2)": "Area_min",
        "∏cmc (mN/m)": "Pi_CMC",
    }
)


df = df.drop(
    columns=[
        "CMC err mM",
        "CMC mM",
        "β",
        "Γmax (μmol/m2)",
        "C20 (10-4)",
        "ΔG0mic (kJ/mol)",
        "ΔG0ads (kJ/mol)",
    ]
)

df = df[df.SMILES != ""]

df.to_csv(PROCESSED_FILE, index=False)
