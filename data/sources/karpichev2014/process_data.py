import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE = "source_data/karpichev2014_table_1.csv"
PROCESSED_FILE = "processed_data/karpichev2014.csv"

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

df = df.rename(
    columns={
        "CMC (M)": "CMC",
        "γCMC (mN/m)": "AW_ST_CMC",
        "Alim (nm2)": "Area_min",
        "p(C20/M)": "pC20",
    }
)

df["C20"] = 10**-df.pC20
df["pCMC"] = -np.log10(df.CMC)

df = df[df.SMILES != ""]

df.to_csv(PROCESSED_FILE, index=False)
