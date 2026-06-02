import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors


# Compare to manual transcription
df = pd.read_csv("source_data/song2013a_table_1.csv")

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

df["CMC"] = df["Surface Tension CMC (mM)"] / 1000
df["pCMC"] = -np.log10(df.CMC)
df["Gamma_max"] = df["Surface Tension Γmax10-10 (mol/cm2)"] / 10**6

df = df.rename(columns={"Surface Tension γCMC (mN/m)": "AW_ST_CMC"})

df = df.drop(
    columns=[
        "identifier",
        "Surface Tension CMC (mM)",
        "Surface Tension Γmax10-10 (mol/cm2)",
        "Surface Tension Amin (A ̊ 2)",
        "Conductivity CMC (mM)",
        "Conductivity β",
        "Conductivity Gmic  0 (kJ/mol)",
    ]
)

df.to_csv("processed_data/song2013a.csv", index=False)
