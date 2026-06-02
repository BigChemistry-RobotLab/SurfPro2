import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors


# Compare to manual transcription
df = pd.read_csv("source_data/he2019_table_1.csv")

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


df["CMC"] = df["CMC (mM)"] / 1000
df["pCMC"] = -np.log10(df.CMC)
df["Gamma_max"] = df["Γmax (μmol m−2)"] / 1000000

df = df.rename(
    columns={
        "Surfactants": "identifier",
        "γCMC (mN m−1)": "AW_ST_CMC",
        "πCMC (mN m−1)": "Pi_CMC",
        "Amin (nm2)": "Area_min",
    }
)


df = df.drop(
    columns=[
        "CMC (mM)",
        "Γmax (μmol m−2)",
    ]
)
df = df[~(df.SMILES == "")]

df.to_csv("processed_data/he2019.csv", index=False)
