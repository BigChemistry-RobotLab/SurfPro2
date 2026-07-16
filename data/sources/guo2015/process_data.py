import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE_1 = "source_data/guo2015_table_1.csv"
SOURCE_FILE_2 = "source_data/guo2015_table_2.csv"
PROCESSED_FILE = "processed_data/guo2015.csv"

df1 = pd.read_csv(SOURCE_FILE_1)
df2 = pd.read_csv(SOURCE_FILE_2)

df = pd.concat([df1, df2], axis=0)

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

df["Gamma_max"] = df["Γmax (μmol/m2)"] / 10**6

df["Temp_Celsius"] = df["T (K)"] - 272.15

df = df.rename(
    columns={
        "SAA": "identifier",
        "γCMC (mN/m)": "AW_ST_CMC",
        "Amin (nm2)": "Area_min",
        "pC20 (mol/L)": "pC20",
    }
)

df["C20"] = 10**-df.pC20


df = df.drop(
    columns=[
        "T (K)",
        "Krafft point (oC)",
        "CMC (mmol/L)",
        "Γmax (μmol/m2)",
    ]
)

df = df[df.SMILES != ""]

df.to_csv(PROCESSED_FILE, index=False)
