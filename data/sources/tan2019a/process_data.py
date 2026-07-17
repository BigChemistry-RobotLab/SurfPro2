import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

Si3 = "C[Si](O[Si](C)(C)(C))(O[Si](C)(C)(C))CCS"
Si4D = "[Si](O[Si](C)(O[Si](C)(C)(C))(O[Si](C)(C)(C)))(C)(C)CCS"
Et_Si3 = "C[Si](O[Si](CC)(CC)(CC))(O[Si](CC)(CC)(CC))CCS"
Si4 = "[Si](O[Si](C)(C)(C))(O[Si](C)(C)(C))(O[Si](C)(C)(C))CCS"
i_Pr_Si3 = "C[Si](O[Si](C(C)C)(C(C)C)(C(C)C))(O[Si](C(C)C)(C(C)C)(C(C)C))CCS"
CCO = "CCO"
C = "C"

translations = {
    "Si3-EO16": Si3 + CCO * 16,
    "Si4D-EO16": Si4D + CCO * 16,
    "Et-Si3-EO16": Et_Si3 + CCO * 16,
    "Si4-EO16": Si4 + CCO * 16,
    "i-Pr-Si3-EO16": i_Pr_Si3 + CCO * 16,
}

df = pd.read_csv("source_data/tan2019a_table_1.csv")

smiles_list = []
inchi_list = []
mol_wts = []
for i, row in df.iterrows():
    code = row.code
    smiles = translations.get(code)
    mol = Chem.MolFromSmiles(smiles)
    if mol:
        inchi = Chem.MolToInchi(mol)
        canon_smiles = Chem.MolToSmiles(mol)
        mw = Descriptors.MolWt(mol)
        smiles_list.append(canon_smiles)
        inchi_list.append(inchi)
        mol_wts.append(mw)
    else:
        print("!!!!!!")
        smiles_list.append("")
        inchi_list.append("")
        mol_wts.append("")

df["SMILES"] = smiles_list
df["Molecular_Weight"] = mol_wts
df["InChI"] = inchi_list
df["CMC"] = df["CMC mM"] / 1000
df["pCMC"] = -np.log10(df["CMC mM"] / 1000)

df["Gamma_max"] = df["Γmax (μmol m−2)"] / 10**6
df["Area_min"] = df["Amin  (Å2)"] / 100

if "pC20" in df.columns:
    df["C20"] = 10**-df.pC20
elif "C20" in df.columns:
    df["pC20"] = -np.log10(df.C20)

df = df.rename(
    columns={
        "γCMC  (mN m−1)": "AW_ST_CMC",
        "ΠCMC  (mN m−1)": "Pi_CMC",
        "code": "identifier",
    }
)
df = df.drop(columns=["CMC /C20", "ΔG0  m  kJ mol−1", "ΔG0  ads  kJ mol−1"])

df.to_csv("processed_data/tan2019a.csv", index=False)
