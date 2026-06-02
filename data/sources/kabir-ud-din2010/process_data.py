import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE = "source_data/kabir-ud-din2010_table_1.csv"
PROCESSED_FILE = "processed_data/kabir-ud-din2010.csv"

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

df["CMC"] = df["cmc 10^3/ M"] / 1000
df["pCMC"] = -np.log10(df.CMC)

df["Temp_Celsius"] = df["T/ K"] - 272.15


df = df.drop(
    columns=[
        "cmc 10^3/ M",
        "α",
        "Nagg",
        "∆G0m (kJ/mol)",
        "∆G0m;tail (kJ/mol)",
        "∆G0m;trans (kJ/mol)",
        "∆H0m (kJ/mol)",
        "∆S0m (kJ/K.mol)",
        "T/ K"
    ]
)

df = df[df.SMILES != ""]
df = df[df["φDO"] == 0.0]
df = df.drop(columns=["φDO"])
df.to_csv(PROCESSED_FILE, index=False)
