import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE = "source_data/lakra2014_table_1.csv"
PROCESSED_FILE = "processed_data/lakra2014.csv"

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

df["CMC"] = df["CMC (mM)"] / 1000
df["pCMC"] = -np.log10(df.CMC)

df["Gamma_max"] = df["Γmax 10^6 (mol/m2)"] / 10**6
df["Area_min"] = df["Amin 10^20 (m2/mol)"] / 100

df = df.rename(
    columns={
        "Surfactant": "identifier",
        "∏cmc (mN/m)": "Pi_CMC",
    }
)


df = df.drop(
    columns=[
        "CMC (mM)",
        "Cideal (mM)",
        "α",
        "I1/I3",
        "Nagg",
        "Ksv (10^-3 L/mol)",
        "ΔGmo (kJ/mol)",
        "ΔGads (kJ/mol)",
        "ΔGmin (kJ/mol)",
        "Γmax 10^6 (mol/m2)",
        "Amin 10^20 (m2/mol)",
    ]
)

df = df[df.SMILES != ""]

df.to_csv(PROCESSED_FILE, index=False)
