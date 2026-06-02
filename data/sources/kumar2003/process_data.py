import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE = "source_data/kumar2003_table_1.csv"
PROCESSED_FILE = "processed_data/kumar2003.csv"

df = pd.read_csv(SOURCE_FILE)

smiles_list = []
inchi_list = []
mol_wts = []
for i, row in df.iterrows():
    smiles = row.SMILES
    if pd.isna(smiles):
        smiles_list.append("")
        inchi_list.append("")
        mol_wts.append("")

    else:
        mol = Chem.MolFromSmiles(smiles)
        smiles = Chem.MolToSmiles(mol)
        inchi = Chem.MolToInchi(mol)
        mw = Descriptors.MolWt(mol)

        smiles_list.append(smiles)
        inchi_list.append(inchi)
        mol_wts.append(mw)


df["SMILES"] = smiles_list
df["Molecular_Weight"] = mol_wts
df["InChI"] = inchi_list

df["Area_min"] = df["a (Å2)"] / 100

df = df.rename(
    columns={
        "Surfactant": "identifier",
        "cmc (M) (tensiometry)": "CMC",
        "temperature (oC)": "Temp_Celsius",
        "γcmc (mN m-1)": "AW_ST_CMC",
        "Γ (mol m-2)": "Gamma_max",
    }
)

df["pCMC"] = -np.log10(df.CMC)

df = df.drop(
    columns=[
        "cmc (M) (fluorescence)",
        "cmc/C20",
        "a (Å2)"
    ]
)

df = df[df.SMILES != ""]
df.to_csv(PROCESSED_FILE, index=False)
