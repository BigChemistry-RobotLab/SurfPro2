import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE = "source_data/mureau2000_table_1.csv"
PROCESSED_FILE = "processed_data/mureau2000.csv"

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


df["CMC"] = df["103 cmc (mol/dm3)"] / 1000
df["pCMC"] = -np.log10(df.CMC)

df["Gamma_max"] = df["106Γ (mol/m2)"] / 1000000
df["Area_min"] = df["102a (nm2/molecule)"] / 100

df = df.rename(
    columns={
        "Surfactant": "identifier",
        "γcmc (mN/m)": "AW_ST_CMC",
    }
)


df = df.drop(
    columns=[
        "Yielda",
        "Yieldb",
        "Solubility (mol/dm-3)",
        "103 cmc (mol/dm3)",
        "-[dγ /d log c]T (mN/m)",
        "106Γ (mol/m2)",
        "102a (nm2/molecule)",
    ]
)

df = df[df.SMILES != ""]

df.to_csv(PROCESSED_FILE, index=False)
