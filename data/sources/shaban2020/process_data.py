import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE = "source_data/shaban2020_table_3.csv"
PROCESSED_FILE = "processed_data/shaban2020.csv"

df = pd.read_csv(SOURCE_FILE)

df = df[df["Water type"] == "Double-distilled water"]
df["CMC"] = df["cmc (mmol L-1)"] / 1000

replace_columns = {
    "Surfactant": "identifier",
    "γcmc (mN m-1)": "AW_ST_CMC",
    "Amin (nm2)": "Area_min",
    "pC20 (??M)": "pC20",
}

drop_columns = [
    "Water type",
    "cmc (mmol L-1)",
    "γ IT (mN m-1)",
    "πcmc (mN m-1)",
    "pC20",
    "cmc/pC20",
    "Γmax (?? mol m-2)",
    "ΔG°ads (kJ/mol)",
    "ΔG°mic (kJ/mol)",
    "ΔG°ads-ΔG°mic (kJ/mol)",
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
