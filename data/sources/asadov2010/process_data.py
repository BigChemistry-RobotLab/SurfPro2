import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors


# Compare to manual transcription
df = pd.read_csv("source_data/asadov2010_table_2.csv")

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

df["CMC"] = df[" CMC X 10^2 (mol dm-3)"] / 100
df["pCMC"] = -np.log10(df.CMC)
df["Gamma_max"] = df["  Γmax x 10^10  (mol cm-2)"] / 10**6
df["Area_min"] = df["  Amin x 10^2  (nm2)"] / 100
df["C20"] = 10 ** -df["  pC20"]

df = df.rename(
    columns={
        "Surfactants": "identifier",
        " T °C": "Temp_Celsius",
        "structure_code": "identifier",
        "  gamma_CMC  (mN m-1)": "AW_ST_CMC",
        "  pC20": "pC20",
    }
)


df = df.drop(
    columns=[
        "  pCMC  (mN m-1)",
        " CMC X 10^2 (mol dm-3)",
        "  Γmax x 10^10  (mol cm-2)",
        "  Amin x 10^2  (nm2)",
    ]
)
df = df[~(df.SMILES == "")]

df.to_csv("processed_data/asadov2010.csv", index=False)
