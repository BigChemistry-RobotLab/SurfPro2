import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE = "source_data/bhadani2011_table_1.csv"
PROCESSED_FILE = "processed_data/bhadani2011.csv"

df = pd.read_csv(SOURCE_FILE)

df["CMC"] = df["cmc (mM)"]/1000
df["Gamma_max"]= df["106Γmax n = 2 (mol/m2)"]/10**6

replace_columns = {
    "surfactant": "identifier",
    "Amin n=2 (nm2)": "Area_min",
    "γcmc mN/m": "AW_ST_CMC",
    "C20 (M)": "C20",
}

drop_columns = [
    "cmc (mM)",
    "cmc err (mM)",
    "β",
    "γcmc err mN/m",
    "106Γmax n = 2 (mol/m2)",
    "106Γmax n =2 err (mol/m2)",
    "106Γmax n = 3 (mol/m2)",
    "106Γmax n =3 err (mol/m2)",
    "Amin n=2 err (nm2)",
    "Amin n=3 (nm2)",
    "Amin n=3 err (nm2)",
    "ΔG°mic kJmol-1",
    "ΔG°mic err kJmol-1",
    "ΔG°ads kJmol-1",
    "ΔG°ads err kJmol-1",
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
