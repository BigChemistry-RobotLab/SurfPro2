import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE_1 = "source_data/kjellin2001_table_1.csv"
SOURCE_FILE_2 = "source_data/kjellin2001_table_2.csv"
PROCESSED_FILE = "processed_data/kjellin2001.csv"

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


df["CMC"] = df["cmc mean [mM]"] / 1000
df["pCMC"] = -np.log10(df.CMC)

df["Gamma_max"] = df["Γcmc [μmol/m2]"] / 1000000

df = df.rename(
    columns={
        "surfactant": "identifier",
        "Acmc [nm2]": "Area_min",
        "γcmc [mN/m]": "AW_ST_CMC",
    }
)


df = df.drop(
    columns=[
        "cmc lower [mM]",
        "cmc upper [mM]",
        "cmc mean [mM]",
        "Γcmc [μmol/m2]",
        "∆Gcmc0 [kJ/mol]",
    ]
)

df = df[df.SMILES != ""]

df.to_csv(PROCESSED_FILE, index=False)
