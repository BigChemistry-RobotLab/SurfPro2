import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors


# Compare to manual transcription
df = pd.read_csv("source_data/palkowski2014_table_3.csv")
df_names = pd.read_csv("source_data/code_to_smiles.csv").set_index("no")

# update the database with generated smiles
new_smiles_list = []
inchi_list = []
mol_wts = []

for i, row in df.iterrows():
    code = row.no
    new_smiles = df_names.loc[code].SMILES

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

df["pCMC"] = df["-lgCMC"]
df["CMC"] = 10**-df.pCMC

df["Gamma_max"] = df["Γ 106"] / 10**6
df["Area_min"] = 10**18 * (df["A 1020"] / 10**20)

df = df.rename(
    columns={
        "no": "identifier",
        "γCMC": "AW_ST_CMC",
    }
)


df = df.drop(
    columns=[
        "n",
        "R",
        "-lgCMC",
        "Γ 106",
        "A 1020",
        "ΔGads",
        "MIC (mM/L)",
        "Class",
    ]
)
df = df[~(df.SMILES == "")]

df.to_csv("processed_data/palkowski2014.csv", index=False)
