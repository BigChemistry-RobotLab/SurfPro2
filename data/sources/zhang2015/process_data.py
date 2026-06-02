import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

df = pd.read_csv("source_data/zhang2015_table_1.csv")

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
df["CMC"] = df["CMC (mmol L 1)"] / 1000
df["pCMC"] = -np.log10(df.CMC)
df["Gamma_max"] = df["Gm (10 6 mol m 2)"] / 1000000
df["Area_min"] = df["A0 (A ̊2)"] / 100
df["Temp_Celsius"] = 25.0

df = df.rename(
    columns={
        "Parameters": "identifier",
    }
)


df = df.drop(
    columns=[
        "CMC (mmol L 1)",
        "Gm (10 6 mol m 2)",
        "A0 (A ̊2)",
    ]
)
df = df[~(df.SMILES == "")]

df.to_csv("processed_data/zhang2015.csv", index=False)
