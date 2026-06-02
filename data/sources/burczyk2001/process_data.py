import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

C = "C"
OLEYL = r"CCCCCCCC\C=C/CCCCCCCC"
translations = {
    "C10-MGA": f"{C * 10}N(C)C([C@H](O)[C@@H](O)[C@H](O)[C@H](O)CO)=O",
    "C12-MGA": f"{C * 12}N(C)C([C@H](O)[C@@H](O)[C@H](O)[C@H](O)CO)=O",
    "C14-MGA": f"{C * 14}N(C)C([C@H](O)[C@@H](O)[C@H](O)[C@H](O)CO)=O",
    "C16-MGA": f"{C * 16}N(C)C([C@H](O)[C@@H](O)[C@H](O)[C@H](O)CO)=O",
    "C18-MGA": f"{C * 18}N(C)C([C@H](O)[C@@H](O)[C@H](O)[C@H](O)CO)=O",
    "C10-MLA": f"O[C@@H]1[C@@H]([C@H]([C@@H](O[C@@H]1CO)O[C@@]([H])([C@@H]([C@H](C(N(C){C * 10})=O)O)O)[C@@H](CO)O)O)O",
    "C12-MLA": f"O[C@@H]1[C@@H]([C@H]([C@@H](O[C@@H]1CO)O[C@@]([H])([C@@H]([C@H](C(N(C){C * 12})=O)O)O)[C@@H](CO)O)O)O",
    "C14-MLA": f"O[C@@H]1[C@@H]([C@H]([C@@H](O[C@@H]1CO)O[C@@]([H])([C@@H]([C@H](C(N(C){C * 14})=O)O)O)[C@@H](CO)O)O)O",
    "C16-MLA": f"O[C@@H]1[C@@H]([C@H]([C@@H](O[C@@H]1CO)O[C@@]([H])([C@@H]([C@H](C(N(C){C * 16})=O)O)O)[C@@H](CO)O)O)O",
    "C18-MLA": f"O[C@@H]1[C@@H]([C@H]([C@@H](O[C@@H]1CO)O[C@@]([H])([C@@H]([C@H](C(N(C){C * 18})=O)O)O)[C@@H](CO)O)O)O",
    "OL-MGA": f"{OLEYL}N(C)C([C@H](O)[C@@H](O)[C@H](O)[C@H](O)CO)=O",
    "OL-MLA": f"O[C@@H]1[C@@H]([C@H]([C@@H](O[C@@H]1CO)O[C@@]([H])([C@@H]([C@H](C(N(C){OLEYL})=O)O)O)[C@@H](CO)O)O)O",
}

df = pd.read_csv("source_data/burczyk2001_table_3.csv")

smiles_list = []
inchi_list = []
mol_wts = []
for i, row in df.iterrows():
    code = row["Surfactant"]
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

df["Gamma_max"] = df["10^6 Γmax (mol/m2)"] / 1000000
df["Area_min"] = (df["10^20 Amin (m^2)"] / 10**20) * 10**18

df = df.rename(
    columns={
        "Surfactant": "identifier",
        "CMC (mol dm^-3)": "CMC",
        "∏cmc (mN/m)": "Pi_CMC",
    }
)

df["pCMC"] = -np.log10(df.CMC)

df = df.drop(
    columns=[
        "10^6 Γmax (mol/m2)",
        "10^20 Amin (m^2)",
        "-ΔG0cmc kJ/mol",
        "-ΔG0cmc/CH2",
        "-ΔG0ads kJ/mol",
        "-ΔG0ads/CH2",
    ]
)

df = df[~(df.SMILES == "")]
df.to_csv("processed_data/burczyk2001.csv", index=False)
