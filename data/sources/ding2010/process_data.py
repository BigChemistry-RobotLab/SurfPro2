import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE = "source_data/ding2010_table_1.csv"
PROCESSED_FILE = "processed_data/ding2010.csv"

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

df["CMC"] = df["cmc (mmol/L)"] / 1000
df["pCMC"] = -np.log10(df.CMC)

df["C20"] = 10**-df.pC20

# units give too large values - removed
#df["Gamma_max"] = df["106 Γmax (mol/cm2)"] / 10**6

df = df.rename(
    columns={
        "Surfactant": "identifier",
        "Amin (nm2)": "Area_min",
        "γcmc (mN/m)": "AW_ST_CMC",
    }
)


df = df.drop(
    columns=[
        "Krafft point (oC)",
        "cmc (mmol/L)",
        "106 Γmax (mol/cm2)",
        "cmc/C20",
    ]
)

df = df[df.SMILES != ""]

df.to_csv(PROCESSED_FILE, index=False)
