import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE = "source_data/liu2014a_table_1.csv"
PROCESSED_FILE = "processed_data/liu2014a.csv"

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


df["CMC"] = df["cmc surface tension (mM)"] / 1000
df["pCMC"] = -np.log10(df.CMC)

df["Gamma_max"] = df["106Γmax (mol/m2)"] / 1000000

df = df.rename(
    columns={
        "Surfactants": "identifier",
        "γCMC (mN/m)": "AW_ST_CMC",
        "Amin (nm2/mol)": "Area_min",
    }
)


df = df.drop(
    columns=[
        "cmc surface tension (mM)",
        "cmc conductivity (mM)",
        "cmc fluorescence (mM)",
        "106Γmax (mol/m2)",
    ]
)

df = df[df.SMILES != ""]

df.to_csv(PROCESSED_FILE, index=False)
