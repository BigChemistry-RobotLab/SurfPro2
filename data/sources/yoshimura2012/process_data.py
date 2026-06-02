import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE = "source_data/yoshimura2012_table_1.csv"
PROCESSED_FILE = "processed_data/yoshimura2012.csv"

df = pd.read_csv(SOURCE_FILE)

df["CMC"] = df["cmc surface tension (mmol dm-3)"] / 1000
df["Gamma_max"] = df["106Γ (mol m-2)"] / 10**6

replace_columns = {
    "surfactant": "identifier",
    "A (nm2/molecule)": "Area_min",
    "γcmc (mN m-1)": "AW_ST_CMC",
}

drop_columns = [
    "cmc surface tension (mmol dm-3)",
    "cmc conductivity (mmol dm-3)",
    "106Γ (mol m-2)",
    "ΔG°mic (kJ mol-1)",
    "ΔG°ads (kJ mol-1)",
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
