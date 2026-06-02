import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors


C = "C"
skeleton = "{tail}OC(=O)[C@@H]({R1})NC(=O)c1ccccc1S(=O)(=O)[O-].[Na+]"
CH2Ph = "Cc1ccccc1"

translations = {
    "3a": skeleton.format(tail=C * 5, R1=CH2Ph),
    "3b": skeleton.format(tail=C * 8, R1=CH2Ph),
    "3c": skeleton.format(tail=C * 10, R1=CH2Ph),
    "3d": skeleton.format(tail=C * 12, R1=CH2Ph),
    "3e": skeleton.format(tail=C * 14, R1=CH2Ph),
    "4d": skeleton.format(tail=C * 12, R1=C),
    "N–C12H25–Phe": "",
    "N–C12H25–Ala22": "",
    "C12H25–C6H4–SO3Na23": "",
}

df = pd.read_csv("source_data/baczko_table_2.csv")

smiles_list = []
inchi_list = []
mol_wts = []
for t in translations:
    smiles = translations[t]

    mol = Chem.MolFromSmiles(smiles)

    if mol:
        mw = Descriptors.MolWt(mol)
        new_smiles = Chem.MolToSmiles(mol)
        inchi = Chem.MolToInchi(mol)
        smiles_list.append(new_smiles)
        inchi_list.append(inchi)
        mol_wts.append(mw)
    else:
        smiles_list.append("")
        inchi_list.append("")
        mol_wts.append("")

df["SMILES"] = smiles_list
df["Molecular_Weight"] = mol_wts

df["pCMC"] = -np.log10(df["CMC (mmol/L)"] / 1000)
df["CMC"] = df["CMC (mmol/L)"] / 1000

df["InChI"] = inchi_list
df["Area_min"] = df[" a_s per molecule (A2)"] / 100

df = df[df.SMILES != ""]

df = df.rename(
    columns={
        "γmin (mN/m)": "AW_ST_CMC",
    }
)

df = df.drop(
    columns=[
        "Solubility in H2O (mmol/L)",
        "NC",
        "CMC (mmol/L)",
        "Entry",
        "Compounds",
        " a_s per molecule (A2)",
    ]
)

df.to_csv("processed_data/baczko2004.csv", index=False)
