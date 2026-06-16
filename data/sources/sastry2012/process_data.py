import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE_1 = "source_data/sastry2012_table_1.csv"
SOURCE_FILE_2 = "source_data/sastry2012_table_2.csv"
PROCESSED_FILE = "processed_data/sastry2012.csv"

df1 = pd.read_csv(SOURCE_FILE_1)
df2 = pd.read_csv(SOURCE_FILE_2)

df = pd.concat([df1, df2], axis=0)
df.to_csv("temp.csv")

df["CMC"] = df["CAC (mM)"] / 1000
df["Gamma_max"] = df["Γmax (10^10 mol cm-2)"] / 10**6
df["Area_min"] = df["αs (Å2)"] / 100

replace_columns = {
    "IL": "identifier",
    "γCAC (mN m-1)": "AW_ST_CMC",
    "∏CAC (mN m-1)": "Pi_CMC",
}

drop_columns = [
    "CAC (mM)",
    "Γmax (10^10 mol cm-2)",
    "Γmax err (10^10 mol cm-2)",
    "ΔGoa (kJ mol-1)",
    "ΔGoa err (kJ mol-1)",
    "ΔHoa (kJ mol-1)",
    "ΔHoa err (kJ mol-1)",
    "ΔSoa (J mol-1 K-1)",
    "ΔSoa err (J mol-1 K-1)",
    "αs err (Å2)",
    "β",
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
