import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE = "source_data/abo-riya2016_table_4.csv"
PROCESSED_FILE = "processed_data/abo-riya2016.csv"

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

df["CMC"] = df["CMCx10-5 (Mol/l)"] / 100000
df["pCMC"] = -np.log10(df.CMC)
df["Gamma_max"] = df["Γmax × 1010 (mol cm-2)"] / 1000000

df = df.rename(
    columns={
        "Compounds": "identifier",
        "Amin (nm2)": "Area_min",
        "γCMC (mN/m)": "AW_ST_CMC",
    }
)


df = df.drop(
    columns=[
        "CMCx10-5 (Mol/l)",
        "ΠCMC (mN/m)",
        "Γmax × 1010 (mol cm-2)",
        "ΔGomic (kJ mol-1)",
        "ΔGa0ds (kJ mol-1)",
    ]
)

df = df[df.SMILES != ""]

df.to_csv(PROCESSED_FILE, index=False)
