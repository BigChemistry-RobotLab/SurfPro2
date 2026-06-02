import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors


# Compare to manual transcription
df = pd.read_csv("source_data/zhang1996a_table_2.csv")

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

df["CMC"] = df["CMC x 10^3 (mol/liter)"] / 1000
df["pCMC"] = -np.log10(df.CMC)
df["Gamma_max"] = df["Γ X 10^10 (mol/cm2)"] / 10**6
df["Area_min"] = df["Area/molecule (A2)"] / 100

df = df.rename(
    columns={
        "Surfactant": "identifier",
        "Efficiency pC20": "pC20",
        "Pi_CMC/found (dyn/cm)": "AW_ST_CMC",
    }
)

df = df.drop(
    columns=[
        "CMC x 10^3 (mol/liter)",
        "Γ X 10^10 (mol/cm2)",
        "Area/molecule (A2)",
        "pCMC/calc. (dyn/cm)",
    ]
)

if "pC20" in df.columns:
    df["C20"] = 10**-df.pC20
elif "C20" in df.columns:
    df["pC20"] = -np.log10(df.C20)

df.to_csv("processed_data/zhang1996a.csv", index=False)
