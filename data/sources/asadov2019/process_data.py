import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

C = "C"

translations = {
    "C8C5C8[iso-Pr(OH)]": f"{C * 8}[NH+](CC(C)O){C * 5}[NH+](CC(C)O){C * 8}.[Br-].[Br-]",
    "C9C5C9[iso-Pr(OH)]": f"{C * 9}[NH+](CC(C)O){C * 5}[NH+](CC(C)O){C * 9}.[Br-].[Br-]",
    "C12C5C12[iso-Pr(OH)]": f"{C * 12}[NH+](CC(C)O){C * 5}[NH+](CC(C)O){C * 12}.[Br-].[Br-]",
    "C16C5C16[iso-Pr(OH)]": f"{C * 16}[NH+](CC(C)O){C * 5}[NH+](CC(C)O){C * 16}.[Br-].[Br-]",
    "C8C5C8[iso-Pr(OH)]2": f"{C * 8}[N+](CC(C)O)(CC(C)O){C * 5}[N+](CC(C)O)(CC(C)O){C * 8}.[Br-].[Br-]",
    "C9C5C9[iso-Pr(OH)]2": f"{C * 9}[N+](CC(C)O)(CC(C)O){C * 5}[N+](CC(C)O)(CC(C)O){C * 9}.[Br-].[Br-]",
    "C12C5C12[iso-Pr(OH)]2": f"{C * 12}[N+](CC(C)O)(CC(C)O){C * 5}[N+](CC(C)O)(CC(C)O){C * 12}.[Br-].[Br-]",
    "C16C5C16[iso-Pr(OH)]2": f"{C * 16}[N+](CC(C)O)(CC(C)O){C * 5}[N+](CC(C)O)(CC(C)O){C * 15}.[Br-].[Br-]",
}

df = pd.read_csv("source_data/asadov2019_table_1.csv")

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

df["CMC"] = df["CMC ×104 mol dm―3"] / 10000
df["pCMC"] = -np.log10(df.CMC)
df["Gamma_max"] = df["Γmax×1010 n=2 molcm―2"] / 10**6
df["Area_min"] = df["Amin×102 n=2 nm2"] / 100

df = df.rename(
    columns={
        "Surfactants": "identifier",
        "γCMC mN·m―1": "AW_ST_CMC",
        "πCMC mN m―1": "Pi_CMC",
    }
)
df = df.drop(
    columns=[
        "CPC ×104 mol dm―3",
        "CMC ×104 mol dm―3",
        "Γmax×1010 n=2 molcm―2",
        "Γmax×1010 n=3 molcm―2",
        "Amin×102 n=2 nm2",
        "Amin×102 n=3 nm2",
    ]
)

df = df[~(df.SMILES == "")]
df.to_csv("processed_data/asadov2019.csv", index=False)
