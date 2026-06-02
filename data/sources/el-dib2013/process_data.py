import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE = "source_data/el-dib2013_table_2.csv"
PROCESSED_FILE = "processed_data/el-dib2013.csv"

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

# Incorrect units? Orders of magnitude higher than other Γmax values
df["Gamma_max"] = (df["Γmax/ 10^10 mol/cm2"] / 10**10) * 10**4
df["C20"] = df["pC20"]
df["pC20"] = -np.log10(df.C20)

df = df.rename(
    columns={
        "Monomeric surfactants": "identifier",
        "γ/ mN/m": "AW_ST_CMC",
        "Amin/ nm2": "Area_min",
        "πcmc/ mN/m": "Pi_CMC",
        "cmc/ mol/L": "CMC",
    }
)

df["pCMC"] = -np.log10(df.CMC)

df = df.drop(
    columns=[
        "Γmax/ 10^10 mol/cm2",
        "ΔG0mic (kJ/mol)",
        "ΔG0ads/ kJ/mol",
    ]
)

df = df[df.SMILES != ""]

df.to_csv(PROCESSED_FILE, index=False)
