import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE_1 = "source_data/kuznetsova2009_table_1.csv"
SOURCE_FILE_2 = "source_data/kuznetsova2009_table_2.csv"
PROCESSED_FILE = "processed_data/kuznetsova2020.csv"

df1 = pd.read_csv(SOURCE_FILE_1)
df2 = pd.read_csv(SOURCE_FILE_2)

df = pd.concat([df1, df2], axis=0)
df.to_csv("temp.csv")

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

df["CMC"] = df["CMC tensiometry/ mM"] / 1000
df["pCMC"] = -np.log10(df.CMC)

df["Gamma_max"] = df["106Γmax/ mol/m2"] / 1000000

df = df.rename(
    columns={
        "Amphiphile": "identifier",
        "Amin/ nm2": "Area_min",
    }
)


df = df.drop(
    columns=[
        "CMC tensiometry/ mM",
        "CMC conductometry/ mM",
        "CMC fluorimetry/ mM",
        "106Γmax/ mol/m2",
        "-ΔGm/ kJ/mol",
        "-ΔGad/ J/mol",
        "P",
    ]
)

df = df[df.SMILES != ""]

df.to_csv(PROCESSED_FILE, index=False)
