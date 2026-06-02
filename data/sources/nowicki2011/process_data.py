import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors


# Compare to manual transcription
df = pd.read_csv("source_data/nowicki2011_joined.csv")

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

df["Gamma_max"] = df["106 Γcmc (mol/m2)"] / 10**6
df["Area_min"] = df["Acmc (A ̊ 2)"] / 100

df = df.rename(
    columns={
        "Compound": "identifier",
        "CMC (mol/L)": "CMC",
        "Temp_Celsius_CMC": "Temp_Celsius",
        "γcmc (mN/m)": "AW_ST_CMC",
        "  pC20": "pC20",
    }
)

df["pCMC"] = -np.log10(df.CMC)


df = df.drop(
    columns=[
        "106 Γcmc (mol/m2)",
        "Acmc (A ̊ 2)",
        "ΔGcmc (kJ/mol)",
        "C_cmc_kraft (mol/L)",
        "Krafft point (°C)",
    ]
)
df = df[~(df.SMILES == "")]

df.to_csv("processed_data/nowicki2011.csv", index=False)
