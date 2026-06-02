import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors


# Compare to manual transcription
df = pd.read_csv("source_data/viscardi2000_table_1.csv")

df = df.drop_duplicates(subset="compd", keep="first")

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

df["CMC"] = df["cmc surface tension (mM)"] / 1000
df["pCMC"] = -np.log10(df.CMC)
df["Gamma_max"] = df["Γc (mol/Å2) (×10-10)"] / 10**10
df["Area_min"] = df["Aminc (Å2)"] / 100

df = df.rename(
    columns={
        "compd": "identifier",
        "T °C": "Temp_Celsius",
        "structure_code": "identifier",
        "γlim surface tension (mN/m)": "AW_ST_CMC",
        "pC20c": "pC20",
    }
)


df = df.drop(
    columns=[
        "cmc conductivity (mM)",
        "β conductivity (%)",
        "β surface tension (%)",
        "cmc surface tension (mM)",
        "Γc (mol/Å2) (×10-10)",
        "C20c (mM)",
        "cmc/C20c",
    ]
)

if "pC20" in df.columns:
    df["C20"] = 10**-df.pC20
elif "C20" in df.columns:
    df["pC20"] = -np.log10(df.C20)

df = df[~(df.SMILES == "")]

df.to_csv("processed_data/viscardi2000.csv", index=False)
