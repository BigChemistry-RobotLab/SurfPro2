import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors


# Compare to manual transcription
df = pd.read_csv("source_data/zhi2013_table_1.csv")
df2 = pd.read_csv("source_data/zhi2013_table_2.csv")
df_names = pd.read_csv("source_data/names_to_smiles.csv").set_index("identifier")

df = pd.concat([df, df2], axis=0)

# update the database with generated smiles
new_smiles_list = []
inchi_list = []
mol_wts = []

for i, row in df.iterrows():
    code = row.Surfactant
    new_smiles = df_names.loc[code].SMILES
    if pd.isna(new_smiles):
        new_smiles_list.append("")
        inchi_list.append("")
        mol_wts.append("")
    else:
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

df["Temp_Celsius"] = df["T (K)"] - 272.15
df["CMC"] = df["cmc (mmol/L)"] / 1000
df["pCMC"] = -np.log10(df.CMC)

df["Gamma_max"] = df["Γmax (mol cm-2)"] * 10000

if "pC20" in df.columns:
    df["C20"] = 10**-df.pC20
elif "C20" in df.columns:
    df["pC20"] = -np.log10(df.C20)

df = df.rename(
    columns={
        "Surfactant": "identifier",
        "γmc(mN/m)": "AW_ST_CMC",
        "Amin (nm2)": "Area_min",
    }
)

df = df.drop(
    columns=[
        "cmc (mmol/L)",
        "cmc/C20",
        "Γmax (mol cm-2)",
        "T (K)",
        "G0mic (kJ/mol)",
        "H0mic (kJ/mol)",
        "S0mic (J/mol)",
        "β",
    ],
)

df = df[df.SMILES != ""]

df.to_csv("processed_data/zhi2013.csv", index=False)
