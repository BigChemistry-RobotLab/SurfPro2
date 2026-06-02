import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

df = pd.read_csv("source_data/murguia2008_table_1.csv")

smiles_list = []
inchi_list = []
mol_wts = []
for i, row in df.iterrows():
    sm = row.SMILES

    mol = Chem.MolFromSmiles(sm)
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
df["C20"] = df["C20 (mM)"] / 1000
df["pC20"] = df["pC20"]
df["AW_ST_CMC"] = df["cCMC (mN m-1)"]
df["Gamma_max"] = df["Gamma max x 10^6(mol m-2)"] / 10**6

df["Area_min"] = 10**18 * (df["A X 10^20 (m2)"] / 10**20)

df = df.rename(columns={"surfactant code": "identifier"})
df = df.drop(
    columns=[
        "Compound",
        "CMC (mM)",
        "C20 (mM)",
        "cCMC (mN m-1)",
        "pC20",
        "CMC/C20",
        "Gamma max x 10^6(mol m-2)",
        "A X 10^20 (m2)",
    ]
)

df = df[~(df.SMILES == "")]
df.to_csv("processed_data/murguia2008.csv", index=False)
