import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE = "source_data/badr2010_table_1.csv"
PROCESSED_FILE = "processed_data/badr2010.csv"

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

df["CMC"] = df["cmc (mmol/dm3)"] / 10000
df["pCMC"] = -np.log10(df.CMC)

df["Gamma_max"] = df["Γcmc (10^6 mol/m2)"] / 1000000

df = df.rename(
    columns={
        "compound": "identifier",
        "γcmc (mN/m)": "AW_ST_CMC",
        "Acmc (nm2/mol)": "Area_min",
    }
)


df = df.drop(
    columns=[
        "cmc (mmol/dm3)",
        "Γcmc (10^6 mol/m2)",
        "Foam 0 min (mL)",
        "Foam 10 min (min)",
        "Foam stability V10min/V0minx100% (%)",
    ]
)

df = df[df.SMILES != ""]

df.to_csv(PROCESSED_FILE, index=False)
