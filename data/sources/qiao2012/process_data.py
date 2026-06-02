import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors


# Compare to manual transcription
df = pd.read_csv("source_data/qiao2012_table_1.csv")

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

df["Gamma_max"] = df["Γm x 10^-10/mol cm-2"] / 10**6

df = df.rename(
    columns={
        "Surfactants": "identifier",
        "CMC/mol L-1": "CMC",
        "γcmc/mN m-1": "AW_ST_CMC",
        "πCMC (mN m−1)": "Pi_CMC",
        "Am/nm2": "Area_min",
    }
)

df["pCMC"] = -np.log10(df.CMC)

df = df.drop(
    columns=[
        "identifier",
        "Γm x 10^-10/mol cm-2",
    ]
)
df = df[~(df.SMILES == "")]

df.to_csv("processed_data/qiao2012.csv", index=False)
