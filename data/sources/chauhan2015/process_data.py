import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors


# Compare to manual transcription
df = pd.read_csv("source_data/chauhan2015_table_1.csv")

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


df["CMC"] = df["cmc surface tension mM"] / 1000
df["pCMC"] = -np.log10(df.CMC)
df["Gamma_max"] = df["Gamma_max μmol/m2 (n = 2)"] / 1000000

df = df.rename(
    columns={
        "surfactant": "identifier",
        "g_cmc mN/m": "AW_ST_CMC",
        "Amin nm2 (n = 2)": "Area_min",
        "Pi_cmc mN/m": "Pi_CMC",
    }
)


df = df.drop(
    columns=[
        "cmc conductivity mM",
        "cmc surface tension mM",
        "cmc fluorescence mM",
        "cmc calorimetry mM",
        "cmc err",
        "beta",
        "g_cmc mN/m err",
        "Gamma_max μmol/m2 (n = 3)",
        "Gamma_max μmol/m2 err",
        "Amin nm2 (n  = 3)",
        "Amin nm2 err",
        "C20 (10−4)",
        "Pi_cmc mN/m err",
        "ΔGaods kJ/mol",
        "ΔGaods kJ/mol err",
    ]
)

df = df[~(df.SMILES == "")]

df.to_csv("processed_data/chauhan2015.csv", index=False)
