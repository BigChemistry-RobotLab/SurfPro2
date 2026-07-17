import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE = "source_data/aiad2018_table_1.csv"
PROCESSED_FILE = "processed_data/aiad2018.csv"

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

df["CMC"] = df["CMC M x 10^-4"] / 10000
df["pCMC"] = -np.log10(df.CMC)

df["Area_min"] = df["Amin (A2)"] / 100
df["Gamma_max"] = df["Γmax 10^11 (mol/cm2)"] / 10**7

if "pC20" in df.columns:
    df["C20"] = 10**-df.pC20
elif "C20" in df.columns:
    df["pC20"] = -np.log10(df.C20)

df = df.rename(
    columns={
        "Compound": "identifier",
        "Pi_cmc mN/m": "Pi_CMC",
    }
)


df = df.drop(
    columns=[
        "CMC M x 10^-4",
        "Γmax 10^11 (mol/cm2)",
    ]
)

df = df[df.SMILES != ""]

df.to_csv(PROCESSED_FILE, index=False)
