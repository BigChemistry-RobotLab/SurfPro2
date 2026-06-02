import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE = "source_data/hegazy2016_table_5.csv"
PROCESSED_FILE = "processed_data/hegazy2016.csv"

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

df["CMC"] = df["CMC surface tension (mM)"] / 1000
df["pCMC"] = -np.log10(df.CMC)

df["Gamma_max"] = df["Γmax 9 10-11 surface tension (mol cm-2)"] / 10**7

df = df.rename(
    columns={
        "Inhibitor name": "identifier",
        "γCMC surface tension (mN m-1)": "AW_ST_CMC",
        "πCMC surface tension (mN m-1)": "Pi_CMC",
        "Amin surface tension (nm2)": "Area_min",
    }
)


df = df.drop(
    columns=[
        "CMC surface tension (mM)",
        "Γmax 9 10-11 surface tension (mol cm-2)",
        "CMC conductivity (mM)",
        "β",
        "ΔGomic conductivity (kJ mol-1)",
    ]
)

df = df[df.SMILES != ""]

df.to_csv(PROCESSED_FILE, index=False)
