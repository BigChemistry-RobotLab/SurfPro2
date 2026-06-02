import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE = "source_data/bhadani2015_table_1.csv"
PROCESSED_FILE = "processed_data/bhadani2015.csv"

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

df["CMC"] = df["CMC surface tension (mM)"] / 1000
df["pCMC"] = -np.log10(df.CMC)

df["Gamma_max"] = df["106 Γmax (mol/m2)"] / 1000000
df["pC20"] = -np.log10(df["C20 (M)"])

df = df.rename(
    columns={
        "Surfactant": "identifier",
        "γCMC (mN/m)": "AW_ST_CMC",
        "C20 (M)": "C20",
        "Amin (nm2)": "Area_min",
    }
)


df = df.drop(
    columns=[
        "CMC surface tension (mM)",
        "CMC surface tension err (mM)",
        "CMC conductivity (mM)",
        "CMC conductivity err (mM)",
        "CMC fluorescence (mM)",
        "CMC fluorescence err (mM)",
        "γCMC err (mN /m)",
        "106 Γmax (mol/m2)",
        "106 Γmax err (mol /m2)",
        "Amin err (nm2)",
    ]
)

df = df[df.SMILES != ""]

df.to_csv(PROCESSED_FILE, index=False)
