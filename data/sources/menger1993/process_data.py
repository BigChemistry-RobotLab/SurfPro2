import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE = "source_data/menger1993_table_1.csv"
PROCESSED_FILE = "processed_data/menger1993.csv"

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
        "compd": "identifier",
        "cmc (M)": "CMC",
        "temp (oC)": "Temp_Celsius",
        "ST at CMC (dynes/cm)": "AW_ST_CMC",
    }
)

df["pCMC"] = -np.log10(df.CMC)


df = df.drop(
    columns=[
        "comments",
    ]
)

df = df[df.SMILES != ""]
df.to_csv(PROCESSED_FILE, index=False)
