import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

translations = {
    "Dodecylisopropylolammonium acetate": "CCCCCCCCCCCC[NH2+]CC(C)O.CC(=O)[O-]",
    "Dodecylisopropylolammonium propionate": "CCCCCCCCCCCC[NH2+]CC(C)O.CCC(=O)[O-]",
    "Dodecylisopropylolammonium chloride": "CCCCCCCCCCCC[NH2+]CC(C)O.[Cl-]",
    "Dodecylisopropylolammonium bromide": "CCCCCCCCCCCC[NH2+]CC(C)O.[Br-]",
    "Dodecylmethylisopropylolammonium iodide": "CCCCCCCCCCCC[NH+](C)CC(C)O.[I-]",
    "Dodecylethylisopropylolammonium bromide": "CCCCCCCCCCCC[NH+](CC)CC(C)O.[Br-]",
    "Dodecylpropylisopropylolammonium bromide": "CCCCCCCCCCCC[NH+](CCC)CC(C)O.[Br-]",
}

df = pd.read_csv("source_data/asadov2016_table_2.csv")

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

df["CMC"] = df["CMC x 10^3 (mol dm-3)"] / 1000
df["pCMC"] = -np.log10(df.CMC)
df["Gamma_max"] = df["Γmax x 10^10 (mol cm-2)"] / 10**6
df["Area_min"] = df["Amin x 102 (nm2)"] / 100

df = df.rename(
    columns={
        "Surfactants": "identifier",
        "γCMC (mN m-1)": "AW_ST_CMC",
    }
)
df = df.drop(
    columns=[
        "beta",
        "Γmax x 10^10 (mol cm-2)",
        "CMC x 10^3 (mol dm-3)",
        "DGmic (kJ mol-1)",
        "DGad (kJ mol-1)",
    ]
)

df = df[~(df.SMILES == "")]
df.to_csv("processed_data/asadov2016.csv", index=False)
