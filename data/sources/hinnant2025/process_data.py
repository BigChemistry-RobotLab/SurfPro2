import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE = "source_data/ao5c01726_si_002.xlsx"  # Multiple source files can be provided and merged during processing.
PROCESSED_FILE = "processed_data/hinnant2025.csv"


# Load in data
sheets = ["SMILES Individual", "Calculated CMC"]

df_names = pd.read_excel(
    SOURCE_FILE, sheet_name="SMILES Individual", header=1
).T.reset_index(names=["identifier"])

df_cmc = (
    pd.read_excel(SOURCE_FILE, sheet_name="Calculated CMC", header=2)
    .T.reset_index(names=["identifier"])
    .rename(columns={0: "CMC/ wt%"})
)


df = pd.merge(df_cmc, df_names, left_on="identifier", right_on="identifier", how="left")
# remove entries without SMILES
df = df[~df[0].isna()]

# remove entries with more than one SMILES
df = df[df[1].isna()].dropna(axis=1)
df = df.rename(columns={0: "SMILES"})

# Add in temperature (see 10.1016/j.colsurfa.2023.132533)
df["Temp_Celsius"] = 22.5

# The remainder of this script can remain untouched.


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

# Convert CMC values from wt%
# Assuming a density of 1000 g/L (water)
# M = 1000 g/L x (wt% / 100) / Mr/ g/mol
df["CMC"] = ((df["CMC/ wt%"] / 100) * 1000) / df["Molecular_Weight"]

if "CMC" in df.columns:
    df["pCMC"] = -np.log10(df.CMC)
elif "pCMC" in df.columns:
    df["CMC"] = 10**-df.pCMC

df = df.drop(columns=["CMC/ wt%"])

df["source_doi"] = "10.1021/acsomega.5c01726"
df["reference_doi"] = "10.1016/j.colsurfa.2023.132533"

df.to_csv(PROCESSED_FILE, index=False)
