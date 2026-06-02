import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE = "source_data/barry1978_table_3.csv"
PROCESSED_FILE = "processed_data/barry1978.csv"

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

df["CMC"] = df["CMC/ mM"] / 1000
df["pCMC"] = -np.log10(df.CMC)
df["Temp_Celsius"] = df["Temperature/ K"] - 273.15

df = df.rename(
    columns={
        "Surfactant": "identifier",
    }
)


df = df.drop(columns=["CMC/ mM", "α", "ΔGo/ Kcal/mol"])

df = df[df.SMILES != ""]

df.to_csv(PROCESSED_FILE, index=False)
