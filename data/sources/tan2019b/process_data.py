import numpy as np
from rdkit import Chem
import pandas as pd
from rdkit.Chem import Descriptors

Si3 = "C[Si](C)(C)CCCSCCC"
Pro_Si3 = "CCC[Si](C)(C)CCCSCCC"
But_Si3 = "CCCC[Si](C)(C)CCCSCCC"
Et_Si3 = "CC[Si](C)(C)CCCSCCC"
Et2_Si3 = "CC[Si](CC)(C)CCCSCCC"
Et3_Si3 = "CC[Si](CC)(CC)CCCSCCC"
Si4 = "C[Si](C)(C)O[Si](O[Si](C)(C)(C))(O[Si](C)(C)(C))CCCSCCC"
OCC = "OCC"
OC_C_C = "OC(C)C"
O = "O"

translations = {
    "Si3-PG": Si3 + 27 * OCC + 6 * OC_C_C + O,
    "Et-Si3-PG": Et_Si3 + 27 * OCC + 6 * OC_C_C + O,
    "Pro-Si3-PG": Pro_Si3 + 27 * OCC + 6 * OC_C_C + O,
    "But-Si3-PG": But_Si3 + 27 * OCC + 6 * OC_C_C + O,
    "Et2-Si3-PG": Et2_Si3 + 27 * OCC + 6 * OC_C_C + O,
    "Et3-Si3-PG": Et3_Si3 + 27 * OCC + 6 * OC_C_C + O,
    "Si4-PG": Si4 + 27 * OCC + 6 * OC_C_C + O,
}

df_1 = pd.read_csv("source_data/tan2019b_table_1.csv").set_index("code")
df_2 = pd.read_csv("source_data/tan2019b_table_2.csv").set_index("code", drop=False)

# first combine table 1 and table 2 on code names
df = pd.merge(df_1, df_2, left_index=True, right_index=True)

# add in SMILES
smiles_list = []
inchi_list = []
mol_wts = []
for i, row in df.iterrows():
    code = row.code
    smiles = translations.get(code)
    mol = Chem.MolFromSmiles(smiles)
    if mol:
        inchi = Chem.MolToInchi(mol)
        mw = Descriptors.MolWt(mol)
        canon_smiles = Chem.MolToSmiles(mol)
        smiles_list.append(canon_smiles)
        inchi_list.append(inchi)
        mol_wts.append(mw)
    else:
        print("!!!!!!!!!!")
        smiles_list.append("")
        inchi_list.append("")
        mol_wts.append("")

df.index.name = "identifier"
df["SMILES"] = smiles_list
df["Molecular_Weight"] = mol_wts
df["InChI"] = inchi_list
df["CMC"] = df["CMC surface tension M"]
df["pCMC"] = -np.log10(df.CMC)
df["AW_ST_CMC"] = df["γcmc (mN m−1)"]
df["Pi_CMC"] = df["Πcmc (mN m−1)"]
df["pC20"] = df["pC20"]
df["Gamma_max"] = df["Γmax (μmol m−2)"] / 10**6
df["Area_min"] = df["Αmin (Å2)"] / 100
df["Temp_Celsius"] = 25.0

df = df.drop(
    columns=[
        "code",
        "CMC surface tension/10−5 M",
        "CMC fluorescence/10−5 M",
        "I1/I3",
        "CMC surface tension M",
        "CMC fluorescence M",
        "pCMC surface tension M",
        "pCMC fluorescence M",
        "code",
        "γcmc (mN m−1)",
        "Πcmc (mN m−1)",
        "pC20",
        "Γmax (μmol m−2)",
        "Αmin (Å2)",
        "CMC/C20",
        "ΔG0m (kJ/mol)",
        "ΔGa0ds (kJ/mol)",
        "source_doi_x",
        "reference_doi_x",
    ]
)

df = df.rename(
    columns={"source_doi_y": "source_doi", "reference_doi_y": "reference_doi"}
)

if "pC20" in df.columns:
    df["C20"] = 10**-df.pC20
elif "C20" in df.columns:
    df["pC20"] = -np.log10(df.C20)

df.to_csv("processed_data/tan2019b.csv")
