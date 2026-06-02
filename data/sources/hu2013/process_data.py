import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE = "source_data/hu2013_table_1.csv"
PROCESSED_FILE = "processed_data/hu2013.csv"

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

df["Gamma_max"] = df["Γmax (μmol/m2)"]/1000000

df = df.rename(
    columns={
        "Compounds": "identifier",
        "T (oC)": "Temp_Celsius",
        "Amin (nm2)": "Area_min",
        "γCMC (mN/m)": "AW_ST_CMC",
        "pC20 (mol/L)": "pC20",
    }
)


df = df.drop(
    columns=[
        "CMC (mmol/L)",
        "Γmax (μmol/m2)",
        "The number of molecules per nm2",
    ]
)

df = df[df.SMILES != ""]

df.to_csv(PROCESSED_FILE, index=False)
