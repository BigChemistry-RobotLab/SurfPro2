import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE = "source_data/sarikaya2019_table_1.csv"
PROCESSED_FILE = "processed_data/sarikaya2019.csv"

df = pd.read_csv(SOURCE_FILE)

df = df[(df["Mole frac. of CTAB"] == 1.0) | (df["Mole frac. of CTAB"] == 0.0)]

df["Temp_Celsius"] = df["Temperature K"] - 273.15
df["CMC"] = df["CMCexp"] / 1000  # inferred from the publication text

replace_columns = {}

drop_columns = [
    "Temperature K",
    "Mole frac. of CTAB",
    "αm",
    "g1",
    "CMCexp",
    "CMCideal",
    "Xm1",
    "Xideal1",
    "βm",
    "f1",
    "f2",
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

    if pd.isna(smiles):
        mol = None
        smiles = ""
        inchi = ""
        mw = np.nan
    else:
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
