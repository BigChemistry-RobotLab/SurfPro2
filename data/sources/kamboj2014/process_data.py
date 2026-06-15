import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE = "source_data/kamboj2014_table_1.csv"
PROCESSED_FILE = "processed_data/kamboj2014.csv"

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

df["CMC"] = df["cmc mM"] / 1000
df["pCMC"] = -np.log10(df.CMC)

df["Gamma_max"] = df["106 Γmax mol/m2"] / 1000000
df["C20"] = df["C20 х 10-4"] / 10000
df["pC20"] = -np.log10(df.C20)

df = df.rename(
    columns={
        "Surfactant": "identifier",
        "γCMC mM mN/m": "AW_ST_CMC",
        "πcmc mN/m": "Pi_CMC",
        "Amin nm2": "Area_min",
    }
)


df = df.drop(
    columns=[
        "cmc mM",
        "β",
        "106 Γmax mol/m2",
        "ΔG◦mic KJ/mol",
        "ΔG◦ ads KJ/mol",
        "cmc/C20",
        "C20 х 10-4",
    ]
)

df = df[df.SMILES != ""]

df.to_csv(PROCESSED_FILE, index=False)
