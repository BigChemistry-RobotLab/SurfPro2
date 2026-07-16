import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors


# Compare to manual transcription
df = pd.read_csv("source_data/tan2019_table_1.csv")

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

df["CMC"] = df["CMC/10-5 M"] / 10**5
df["pCMC"] = -np.log10(df.CMC)
df["Gamma_max"] = df["Γmax (μmol·m-2)"] / 10**6
df["Area_min"] = df["Αmin (Å2)"] / 100

if "pC20" in df.columns:
    df["C20"] = 10**-df.pC20
elif "C20" in df.columns:
    df["pC20"] = -np.log10(df.C20)

df = df.rename(
    columns={
        "γCMC (mN·m-1)": "AW_ST_CMC",
        "ΠCMC (mN·m-1)": "Pi_CMC",
    }
)


df = df.drop(
    columns=[
        "CMC/10-5 M",
        "CMC/10-5 M err",
        "γCMC (mN·m-1) err",
        "ΠCMC (mN·m-1) err",
        "pC20 err",
        "Γmax (μmol·m-2)",
        "Γmax (μmol·m-2) err",
        "Αmin (Å2)",
        "Αmin (Å2) err",
        "CMC/C20",
        "CMC/C20 err",
        "ΔG0m kJ/mol",
        "ΔG0m kJ/mol err",
        "ΔGa0ds kJ/mol",
        "ΔGa0ds kJ/mol err",
    ]
)
df = df[~(df.SMILES == "")]

df.to_csv("processed_data/tan2019.csv", index=False)
