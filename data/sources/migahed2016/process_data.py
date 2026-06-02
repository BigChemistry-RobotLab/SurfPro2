import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE = "source_data/migahed2016_table_2.csv"
PROCESSED_FILE = "processed_data/migahed2016.csv"

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


df["Gamma_max"] = df["Γmax (mol cm-2)"] * 10**4
df["Area_min"] = df["Amin (A ̊ 2)"] / 100
df["pC20"] = -df["PC20 (M)"]
df["C20"] = 10**-df.pC20

df = df.rename(
    columns={
        "Compound": "identifier",
        "CMC (M)": "CMC",
        "πCMC (mN/m)": "Pi_CMC",
        "γCMC (mN/m)": "AW_ST_CMC",
    }
)

df["pCMC"] = -np.log10(df.CMC)

df = df.drop(
    columns=[
        "γIT (mN/m)",
        "PC20 (M)",
        "dc/ dlogC",
        "Γmax (mol cm-2)",
        "Amin (A ̊ 2)",
        "ΔGmic (kJ mol-1)",
        "ΔGads (kJ mol-1)",
        "Emulsification power sec",
    ]
)

df = df[df.SMILES != ""]

df.to_csv(PROCESSED_FILE, index=False)
