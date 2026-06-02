import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE = "source_data/lim2012_table_1.csv"
PROCESSED_FILE = "processed_data/lim2012.csv"

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
        "Surfactant": "identifier",
        "∏cmc (mN/m)": "Pi_CMC",
        "CMC mol/L": "CMC",
        "Surface tension CMC (mN/m)": "AW_ST_CMC",
    }
)

df["pCMC"] = -np.log10(df.CMC)

df = df.drop(
    columns=[
        "MW (g/mol)",
        "w.t.%",
        "IFTb (mN/m)",
        "Contact angle (o)",
        "Foam stabilityc (%)",
        "Massd (ng)",
    ]
)

df = df[df.SMILES != ""]

df.to_csv(PROCESSED_FILE, index=False)
