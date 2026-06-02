import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE = "source_data/negm2005_table_2.csv"
PROCESSED_FILE = "processed_data/negm2005.csv"

df = pd.read_csv(SOURCE_FILE)

replace_columns = {
    "Compound": "identifier",
    "CMC, M/L": "CMC",
    "Amin Nm2": "Area_min",
    "πcmc": "Pi_CMC",
    "Pc20": "pC20",
}

drop_columns = [
    "Interfacial tension (mN/m)",
    "E.B. Sec.",
    "Foaming power (mL)",
    "∏max x 10^-9",
    "ΔGacs, kJ/mole",
]

df = df.rename(columns=replace_columns)

df = df.drop(columns=drop_columns)

df["pCMC"] = -np.log10(df.CMC)
df["C20"] = 10**-df.pC20

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


df = df[df.SMILES != ""]

df.to_csv(PROCESSED_FILE, index=False)
