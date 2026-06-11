import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

df = pd.read_csv("source_data/badr2021_table_1.csv")

columns = [
    "Comp.",
    "Temp. °C",
    "CMC/ (mM.L−1)",
    "C20  *10−5 (mol. L−1)",
    "πCMC/ (mN m−1)",
    "Гmax *10−10 (mol. cm−2)",
    "Amin/ A2",
    "CMC/C20",
    "SMILES transcribed",
]

canonical_SMILES = []
inchi_list = []
mol_wts = []
for i, row in df.iterrows():
    smiles = row["SMILES transcribed"]
    mol = Chem.MolFromSmiles(smiles)

    if mol:
        sm = Chem.MolToSmiles(mol)
        inchi = Chem.MolToInchi(mol)
        mw = Descriptors.MolWt(mol)
        canonical_SMILES.append(sm)
        inchi_list.append(inchi)
        mol_wts.append(mw)
    else:
        canonical_SMILES.append("")
        inchi_list.append("")
        mol_wts.append("")


df["SMILES"] = canonical_SMILES
df["Molecular_Weight"] = mol_wts
df["InChI"] = inchi_list
df["CMC"] = df["CMC/ (mM.L−1)"] / 1000
df["pCMC"] = -np.log10(df["CMC/ (mM.L−1)"] / 1000)

df["C20"] = df["C20  *10−5 (mol. L−1)"] / 10**5
df["pC20"] = -np.log10(df["C20"])
df["Gamma_max"] = df["Гmax *10−10 (mol. cm−2)"] / 10**6
df["Area_min"] = df["Amin/ A2"] / 100

df = df.drop(
    columns=[
        "CMC/ (mM.L−1)",
        "C20  *10−5 (mol. L−1)",
        "SMILES transcribed",
        "Amin/ A2",
        "CMC/C20",
        "Гmax *10−10 (mol. cm−2)",
    ]
)

df = df.rename(
    columns={
        "Comp.": "identifier",
        "Temp. °C": "Temp_Celsius",
        "πCMC/ (mN m−1)": "Pi_CMC",
    }
)

df = df[~df.identifier.str.contains("AgNPs")]

df.to_csv("processed_data/badr2021.csv", index=False)
