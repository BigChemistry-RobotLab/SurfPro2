import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE = "source_data/hussain2017.csv"
PROCESSED_FILE = "processed_data/hussain2017.csv"

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

df["Gamma_max"] = df["Γmax x 106 (mol m-2)"] / 1000000

df = df.rename(
    columns={
        "Surfactant": "identifier",
        "CMC (mol L-1)": "CMC",
        "γCMC (mN m-1)": "AW_ST_CMC",
        "πCMC (mN m-1)": "Pi_CMC",
        "Amin (nm2)": "Area_min",
    }
)

df["pCMC"] = -np.log10(df.CMC)

df = df.drop(
    columns=[
        "Γmax x 106 (mol m-2)",
    ]
)

df = df[df.SMILES != ""]

df.to_csv(PROCESSED_FILE, index=False)
