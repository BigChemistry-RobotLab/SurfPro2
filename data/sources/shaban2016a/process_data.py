import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors


# Compare to manual transcription
df = pd.read_csv("source_data/shaban2016a_table_1.csv")

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

df["CMC"] = df["CMC surface tension (mM·L−1)"] / 1000
df["pCMC"] = -np.log10(df.CMC)
df["Gamma_max"] = df["Гmax ∗ 10−10 (mol·cm−2)"] / 10**6
df["C20"] = df["C20 ∗ 10−5 (mol·L−1)"] / 10**5
df["pC20"] = -np.log10(df["C20"])
df["Area_min"] = df["Amin A2"] / 100

df = df.rename(
    columns={
        "Comp.": "identifier",
        "πCMC (mN·m−1)": "",
        "Amin (nm2)": "Area_min",
        "Temp. °C": "Temp_Celsius",
    }
)


df = df.drop(
    columns=[
        "CMC surface tension (mM·L−1)",
        "CMC conductivity (mM·L−1)",
        "α",
        "C20 ∗ 10−5 (mol·L−1)",
        "Гmax ∗ 10−10 (mol·cm−2)",
        "Amin A2",
        "CMC/C20",
    ]
)
df = df[~(df.SMILES == "")]

df.to_csv("processed_data/shaban2016a.csv", index=False)
