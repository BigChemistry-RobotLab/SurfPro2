import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE_1 = "source_data/nessim2010_table_3.csv"
SOURCE_FILE_2 = "source_data/nessim2010_table_4.csv"
PROCESSED_FILE = "processed_data/nessim2018.csv"

df1 = pd.read_csv(SOURCE_FILE_1)
df2 = pd.read_csv(SOURCE_FILE_2)

# remove repeated CMC values
df1 = df1.drop(columns=["CMC (mol/L)"])
df2["CMC"] = 10 ** -df2["-log cmc mol/L"]

df = pd.concat([df1, df2], axis=0)

df["Gamma_max"] = df["Γmax x 1010 mol/cm2"] / 10**6
df["pC20"] = df["-log PC20 mol/L"]

replace_columns = {
    "Surfactant": "identifier",
    "T°C": "Temp_Celsius",
    "Surface Tension γ (mN/m)": "AW_ST_CMC",
    "Amin nm2": "Area_min",
    "πcmc m/Nm": "Pi_CMC",
}

drop_columns = [
    "Krafft Point Kt",
    "Interfacial Tension (mN/m)",
    "Foam Height (ml)",
    "Foam Stability (min)",
    "Emulsion Stability (sec)",
    "-log cmc mol/L",
    "-log PC20 mol/L",
    "Γmax x 1010 mol/cm2",
]

df = df.rename(columns=replace_columns)

df = df.drop(columns=drop_columns)

if "CMC" in df.columns:
    df["pCMC"] = -np.log10(df.CMC)
elif "pCMC" in df.columns:
    df["CMC"] = 10**-df.pCMC

if "pC20" in df.columns:
    df["C20"] = 10**-df.pC20
elif "C20" in df.columns:
    df["pC20"] = -np.log10(df.C20)

smiles_list = []
inchi_list = []
mol_wts = []
for i, row in df.iterrows():
    smiles = row.SMILES

    if pd.isna(smiles):
        mol = None
        smiles = ""
        inchi = ""
        mw = np.nan
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

df = df[df.SMILES != ""]

df.to_csv(PROCESSED_FILE, index=False)
