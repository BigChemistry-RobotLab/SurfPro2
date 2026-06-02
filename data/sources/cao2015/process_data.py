import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE = "source_data/cao2015_table_1.csv"
PROCESSED_FILE = "processed_data/cao2015.csv"

df = pd.read_csv(SOURCE_FILE)

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

df["CMC"] = df["CMC (mmol/L)"] / 1000
df["pCMC"] = -np.log10(df.CMC)

# Units not reasonable - value is too large
#df["Gamma_max"] = df["Γ (mmol/m2)"] / 1000

df = df.rename(
    columns={
        "Surfactant": "identifier",
        "γCMC (mN/m)": "AW_ST_CMC",
        "Amin (nm2)": "Area_min",
    }
)

df = df.drop(
    columns=[
        "CMC (mmol/L)",
        "Γ (mmol/m2)",
    ]
)

df = df[df.SMILES != ""]

df.to_csv(PROCESSED_FILE, index=False)
