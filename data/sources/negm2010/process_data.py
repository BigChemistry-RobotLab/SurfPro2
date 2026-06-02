import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE = "source_data/neg2010_table_2.csv"
PROCESSED_FILE = "processed_data/negm2010.csv"

df = pd.read_csv(SOURCE_FILE)

df["CMC"] = df["CMC, mM=L"] / 1000
df["C20"] = df["Pc20, mM=L"] / 1000
df["pC20"] = -np.log10(df.C20)

replace_columns = {
    "Compound": "identifier",
    "πcmc, mN=m": "Pi_CMC",
    "Amin, nm2": "Area_min",
}

drop_columns = [
    "Pc20, mM=L",
    "CMC, mM=L",
    "Γmax",
    "ΔGmic, kJ . mol-1",
    "ΔGads, kJ . mol-1",
]

df = df.rename(columns=replace_columns)

df = df.drop(columns=drop_columns)

if "CMC" in df.columns:
    df["pCMC"] = -np.log10(df.CMC)
elif "pCMC" in df.columns:
    df["CMC"] = 10**-df.pCMC

if "pC20" in df.columns:
    df["C20"] = 10**-df.pC20
elif "C20" in df.columns:
    df["pC20"] = -np.log10(df.C20)

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

df = df[df.SMILES != ""]

df.to_csv(PROCESSED_FILE, index=False)
