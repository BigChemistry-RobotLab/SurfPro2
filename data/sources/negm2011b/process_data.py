import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE = "source_data/negm2011b_table_2.csv"
PROCESSED_FILE = "processed_data/negm2011b.csv"

df = pd.read_csv(SOURCE_FILE)

df["CMC"] = df["CMC  (mM)"] / 1000
df["C20"] = df["Pc20 (mM)"] / 1000 # interpreted as c20 (mM units, magnitude of values)
df["Area_min"] = df["Amin (Ä2)"] / 100

replace_columns = {
    "Compound": "identifier",
    "πCMC (mN m-1)": "Pi_CMC",
}

drop_columns = [
    "CMC  (mM)",
    "Pc20 (mM)",
    "∂γ/∂log",
    "γIT (mN m-1)",
    "Γmax (mol m-2)", # units are incorrect
    "Amin (Ä2)",
    "ΔGmic (kJ mol-1)",
    "ΔGads (kJ mol-1)",
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
