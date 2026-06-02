import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE = "source_data/hilal2021_table_1.csv"
PROCESSED_FILE = "processed_data/hilal2021.csv"

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

df["CMC"] = df["CMC mM"] / 1000
df["pCMC"] = -np.log10(df.CMC)

df["Gamma_max"] = df["106Γmax mol/m2"] / 10**6

df = df.rename(
    columns={
        "Surfactant": "identifier",
        "γCMC mN/m": "AW_ST_CMC",
        "Πcmc mN/m": "Pi_CMC",
        "Amin nm2": "Area_min",
    }
)


df = df.drop(
    columns=[
        "CMC mM",
        "106Γmax mol/m2",
        "CMC/C20",
        "Foam0 min mL",
        "Foam10 min mL",
        "Foam stability V10/V0 *100  %",
    ]
)

df = df[df.SMILES != ""]

df.to_csv(PROCESSED_FILE, index=False)
