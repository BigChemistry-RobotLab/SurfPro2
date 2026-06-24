import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors


# Compare to manual transcription
df = pd.read_csv("source_data/tawfik2015_table_1.csv")

# update the database with generated smiles
new_smiles_list = []
inchi_list = []
reference_keys = []
reference_doi = []
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

df["CMC"] = df["CMC (mM)"] / 1000
df["pCMC"] = -np.log10(df.CMC)

# Assume units are mol/cm2
df["Gamma_max"] = df["Γmax 10^-11"] / 10**11
df["Area_min"] = df["Amin"]

df = df.rename(
    columns={
        "Compound": "identifier",
        "T (oC)": "Temp_Celsius",
        "pi_cmc (mN m-1)": "Pi_CMC",
        "  gamma_CMC  (mN m-1)": "AW_ST_CMC",
        "Pc20 (M/L)": "pC20",
    }
)


df = df.drop(
    columns=[
        "CMC (mM)",
        "Γmax 10^-11",
        "Amin",
    ]
)

if "pC20" in df.columns:
    df["C20"] = 10**-df.pC20
elif "C20" in df.columns:
    df["pC20"] = -np.log10(df.C20)

df = df[~(df.SMILES == "")]

df.to_csv("processed_data/tawfik2015.csv", index=False)
