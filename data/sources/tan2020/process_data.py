import pandas as pd
import numpy as np
from rdkit import Chem
from rdkit.Chem import Descriptors

df = pd.read_csv("source_data/tan2020_table1.csv")

Si3 = "C[Si](O[Si](C)(C)(C))(O[Si](C)(C)(C))CCCSCCCO"
Si4 = "??"
EO = "CCO"


translations = {
    "Si3EO6": Si3 + EO * 6,
    "Si3EO7": Si3 + EO * 7,
    "Si3EO8": Si3 + EO * 8,
    "Si3EO10": Si3 + EO * 10,
    "Si4EO8": Si4 + EO * 8,
    "Si4EO10": Si4 + EO * 10,
}

inchi_list = []
smiles_list = []
mol_wts = []
for i, row in df.iterrows():
    sm = translations.get(row.code)
    if "?" not in sm:
        mol = Chem.MolFromSmiles(sm)
        canon_sm = Chem.MolToSmiles(mol)
        inchi = Chem.MolToInchi(mol)
        mw = Descriptors.MolWt(mol)
        mol_wts.append(mw)
        smiles_list.append(canon_sm)
        inchi_list.append(inchi)
    else:
        mol_wts.append(None)
        smiles_list.append("")
        inchi_list.append("")

df["SMILES"] = smiles_list
df["InChI"] = inchi_list
df["Molecular_Weight"] = mol_wts
df["CMC"] = df["CMC 10-5M"] * 10**-5
df["AW_ST_CMC"] = df["γcmc(mN m-1)"]
df["Gamma_max"] = df["Γmax(lmol m-2)"] * 1e-6
df["Area_min"] = df["A min(Å2)"] / 100

if "pC20" in df.columns:
    df["C20"] = 10**-df.pC20
elif "C20" in df.columns:
    df["pC20"] = -np.log10(df.C20)

df = df[df.SMILES != ""]

df = df.rename(columns={"code": "identifier"})
df = df.drop(
    columns=[
        "CMC 10-5M",
        "γcmc(mN m-1)",
        "Pi_cmc(mN m-1)",
        "Γmax(lmol m-2)",
        "A min(Å2)",
        "CMC/C20",
        "DG0 mkJ/mol",
        "DG0 adskJ/mol",
    ]
)

df.to_csv("processed_data/tan2020.csv", index=False)
