import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors


# Compare to manual transcription
df = pd.read_csv("source_data/komorek2004_table_1.csv")

# update the database with generated smiles
new_smiles_list = []
inchi_list = []
mol_wts = []

for i, row in df.iterrows():
    new_smiles = row.SMILES
    mol = Chem.MolFromSmiles(new_smiles)
    smiles = Chem.MolToSmiles(mol)
    inchi = Chem.MolToInchi(mol)
    mw = Descriptors.MolWt(mol)

    new_smiles_list.append(smiles)
    inchi_list.append(inchi)
    mol_wts.append(mw)

df["SMILES"] = new_smiles_list
df["InChI"] = inchi_list
df["Molecular_Weight"] = mol_wts

df["Gamma_max"] = df["106 Γcmc (mol/m2)"] / 1000000
df["Area_min"] = (10**18) * (df["1020 A (m2)"] / 10**20)

if "pC20" in df.columns:
    df["C20"] = 10**-df.pC20
elif "C20" in df.columns:
    df["pC20"] = -np.log10(df.C20)

df = df.rename(
    columns={
        "Surfactant": "identifier",
        "cmc (M)": "CMC",
        "γcmc (mN m−1)": "AW_ST_CMC",
        "πCMC (mN m−1)": "Pi_CMC",
        "Amin (nm2)": "Area_min",
    }
)

df["pCMC"] = -np.log10(df.CMC)

df = df.drop(
    columns=[
        "Krafft temp (oC)",
        "106 Γcmc (mol/m2)",
        "1020 A (m2)",
        "cmc/C20",
        "Gcmc (kJ mol-1)",
        "Gcmc/CH2 (kJ mol-1)",
        "Nagg Fluorescence [surfactant] = 25 × cmc",
        "Nagg Fluorescence [surfactant] = 250 × cmc",
    ]
)
df = df[~(df.SMILES == "")]

df.to_csv("processed_data/komorek2004.csv", index=False)
