import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE = "source_data/aveyard1998_table_1.csv"
PROCESSED_FILE = "processed_data/aveyard1998.csv"

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

df["CMC"] = df["cmc (mM)"] / 1000
df["pCMC"] = -np.log10(df.CMC)

df["Area_min"] = df["Acmc (Å2)"] / 100

df = df.rename(
    columns={
        "surfactant": "identifier",
        "πcmc (mN/m)": "Pi_CMC",
    }
)


df = df.drop(
    columns=[
        "cmc (mM)",
        "Acmc (Å2)",
        "∆adsμ° (kJ/mol)",
    ]
)

df = df[df.SMILES != ""]

df.to_csv(PROCESSED_FILE, index=False)
