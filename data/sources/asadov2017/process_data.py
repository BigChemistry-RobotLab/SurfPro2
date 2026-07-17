import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

"""
nonyl-(2-hydroxyethyl)ammonium bromide (NMEABr),
nonyl-di(2-hydroxyethyl)ammonium bromide (NDEABr),
nonyl-tri(2-hydroxyethyl)ammonium bromide (NTEABr),
nonyl-(2hydroxyethyl)ammonium iodide (NMEAI),
nonyl-di(2-hydroxyethyl)ammonium iodide (NDEAI)
nonyl-tri(2-hydroxyethyl)ammonium iodide (NTEAI).
"""
C = "C"
CCO = "CCO"

translations = {
    "NMEAB": C*9 + "[NH2+]" + "CCO" + ".[Br-]" ,
    "NDEAB": C*9 + "[NH+]"  + "(CCO)CCO" + ".[Br-]",
    "NTEAB": C*9 + "[N+]"  + "(CCO)(CCO)CCO" + ".[Br-]",
    "NMEAI": C*9 + "[NH2+]"  + "(CCO)" + ".[I-]",
    "NDEAI": C*9 + "[NH+]"  + "(CCO)CCO" + ".[I-]",
    "NTEAI": C*9 + "[N+]"  + "(CCO)(CCO)CCO" + ".[I-]",
}

df = pd.read_csv("source_data/asadov2017_table_1.csv")

smiles_list = []
inchi_list = []
mol_wts = []
for i, row in df.iterrows():
    code = row["Surfactants"]
    sm = translations.get(code, "")

    mol = Chem.MolFromSmiles(sm)
    smiles = Chem.MolToSmiles(mol)
    inchi = Chem.MolToInchi(mol)
    mw = Descriptors.MolWt(mol)
    smiles_list.append(smiles)
    inchi_list.append(inchi)
    mol_wts.append(mw)


df["SMILES"] = smiles_list
df["Molecular_Weight"] = mol_wts
df["InChI"] = inchi_list

df["CMC"] = df["CMC × 103 mol·dm-3"] / 1000
df["pCMC"] = -np.log10(df.CMC)
df["Gamma_max"] = df["Γmax × 1010 mol·cm-2"] / 10**6
df["Area_min"] = df["Amin × 102 nm2"] /100

if "pC20" in df.columns:
    df["C20"] = 10**-df.pC20
elif "C20" in df.columns:
    df["pC20"] = -np.log10(df.C20)

df = df.rename(
    columns={
        "Surfactants": "identifier",
        "γCMC (mN m-1)": "AW_ST_CMC",
        "πCMC mN·m-1": "Pi_CMC",
    }
)
df = df.drop(
    columns=[
        "β",
        "CMC × 103 mol·dm-3",
        "Γmax × 1010 mol·cm-2",
        "ΔGmic kJ·mol-1",
        "ΔGad kJ·mol-1",
    ]
)

df = df[~(df.SMILES == "")]
df.to_csv("processed_data/asadov2017.csv", index=False)
