import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE = "source_data/lim2015_table_2.csv"
PROCESSED_FILE = "processed_data/lim2015.csv"

df = pd.read_csv(SOURCE_FILE)

replace_columns = {
    "Surfactant": "identifier",
    "CMC (mol/L)": "CMC",
}

drop_columns = [
    "MW (g/mol)",
    "Surface tensiona (mN/m)",
    "Contact angleb (o)",
    "Viscosity (cP)",
    "IFTd (mN/m)",
    "Foam stabilitye (%)",
    "Emulsion stability (1/V) 1 wt% T",
    "Emulsion stability (1/V) 1 wt% B",
    "Emulsion stability (1/V) 3 wt% T",
    "Emulsion stability (1/V) 3 wt% B",
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
