import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE_1 = "source_data/mata2005_table_1.csv"
SOURCE_FILE_2 = "source_data/mata2005_table_2.csv"
PROCESSED_FILE = "processed_data/mata2005.csv"

df1 = pd.read_csv(SOURCE_FILE_1)
df2 = pd.read_csv(SOURCE_FILE_2)
df_names = pd.read_csv("source_data/identifiers_to_compounds.csv").set_index(
    "Surfactants"
)

df = pd.concat([df1, df2], axis=0)

smiles_list = []
inchi_list = []
mol_wts = []
for i, row in df.iterrows():
    smiles = df_names.loc[row.Surfactants].SMILES

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

df["CMC"] = df["CMC (mM)"] / 1000
df["pCMC"] = -np.log10(df.CMC)

df["Temp_Celsius"] = df["Temperature (K)"] - 272.15
df["Area_min"] = df["Area/molecule (A2)"] / 100

df = df.rename(
    columns={
        "Surfactants": "identifier",
        "γCMC (mN m−1)": "AW_ST_CMC",
    }
)

df = df.drop(
    columns=[
        "Area/molecule (A2)",
        "Area/molecule literature (A2)",
        "CMC (mM)",
        "Cπ = 20 (mM)",
        "Nagg",
        "Temperature (K)",
        "ΔGom (kJ mol-1)",
        "ΔH om (kJ mol-1)",
        "ΔSom (kJ mol-1)",
        "Λ0 (cm2 -1 mol-1)",
        "β",
    ]
)

df = df[df.SMILES != ""]

df.to_csv(PROCESSED_FILE, index=False)
