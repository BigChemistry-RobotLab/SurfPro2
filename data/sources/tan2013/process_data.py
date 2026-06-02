import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE_1 = "source_data/tan2013_table_1.csv"
SOURCE_FILE_2 = "source_data/tan2013_table_2.csv"
SOURCE_FILE_3 = "source_data/tan2013_table_3.csv"
PROCESSED_FILE = "processed_data/tan2013.csv"

df1 = pd.read_csv(SOURCE_FILE_1)
df2 = pd.read_csv(SOURCE_FILE_2)
df3 = pd.read_csv(SOURCE_FILE_3)

# remove repeated CMC measurements at 25 oC
df3 = df3[df3["T (◦C)"] != 25]
df3 = df3.rename(columns={"T (◦C)": "Temp_Celsius"})

df = pd.concat([df1, df2, df3], axis=0)
df["Area_min"] = df["Amin (Å2)"] / 100

# use conductivity measurements for CMC for consistency
df["CMC"] = df["CMC conductivity (mM)"] / 1000
df["Gamma_max"] = df["Γmax (μmol m−2)"]/ 10**6

replace_columns = {
    "Surfactants": "identifier",
    "γCMC (mN m−1)": "AW_ST_CMC",
    "πCMC (mN m−1)": "Pi_CMC",
}

drop_columns = [
    "CMC conductivity (mM)",
    "CMC conductivity err (mM)",
    "CMC fluorescence (mM)",
    "CMC fluorescence err (mM)",
    "CMC surface tension (mM)",
    "CMC surface tension err (mM)",
    "Γmax (μmol m−2)",
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
