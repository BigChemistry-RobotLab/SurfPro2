import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

df = pd.read_csv("source_data/rahimov_2021_table1.csv", skiprows=[1])

canonical_smiles = []
inchi_list = []
mol_wts = []
for i, row in df.iterrows():
    smiles = row.SMILES
    mol = Chem.MolFromSmiles(smiles)

    if mol:
        sm = Chem.MolToSmiles(mol)
        inchi = Chem.MolToInchi(mol)
        mw = Descriptors.MolWt(mol)
        canonical_smiles.append(sm)
        mol_wts.append(mw)
        inchi_list.append(inchi)
    else:
        mol_wts.append(None)
        inchi_list.append("")
        canonical_smiles.append("")

df["SMILES"] = canonical_smiles
df["InChI"] = inchi_list
df["Molecular_Weight"] = mol_wts
df["CMC"] = df["CMCb × 10^4  mol dm−3 (surface tension)"] / 10000
df["pCMC"] = -np.log10(df["CMC"])
df["Area_min"] = df["Amin × 102  nm2"] / 100
df["AW_ST_CMC"] = df["γCMC  mN m−1"]
df["Pi_CMC"] = df["πCMC  mN m−1"]

df = df.drop(
    columns=[
        "CMCb × 10^4  mol dm−3 (surface tension)",
        "CMCc × 104  mol dm−3 (conductivity)",
        "Amin × 102  nm2",
        "γCMC  mN m−1",
        "πCMC  mN m−1",
    ]
)

df.to_csv("processed_data/rahimov2021.csv", index=False)
