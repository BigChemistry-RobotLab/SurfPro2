import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors


# Compare to manual transcription
df = pd.read_csv("source_data/hao2016_table_2.csv")

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



df = df.rename(
    columns={
        "Compound": "identifier",
        "γ_cmc (mN m-1)": "AW_ST_CMC",
        "CMC (mol L-1)": "CMC",
    }
)

df["pCMC"] = -np.log10(df.CMC)

df = df.drop(
    columns=[
        "D_dls (m2 s-1)",
        "Frumkin model B (m3 mol-1)",
        "Frumkin model ω0 (m2 mol-1)",
        "Frumkin model α",
        "Frumkin model ε (mm N-1)",
        "Frumkin model E %",
    ]
)
df = df[~(df.SMILES == "")]

df.to_csv("processed_data/hao2016.csv", index=False)
