import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors


df = pd.read_csv("source_data/pinazo2009_table_1.csv")

LYSINE = "C(CCN)C[C@@H](C(=O)O)N"
C12 = "CCCCCCCCCCCC"
C14 = "CCCCCCCCCCCCCC"

translations = {
    "LGG12": [
        f"C(CCN(C(O)CO{C12})C(O)CO)C[C@@H](C(=O)O)N",
        f"C(CCN(C(O{C12})CO)C(O)CO)C[C@@H](C(=O)O)N",
    ],
    "LGG14": [
        f"C(CCN(C(O)CO{C14})C(O)CO)C[C@@H](C(=O)O)N",
        f"C(CCN(C(O{C14})CO)C(O)CO)C[C@@H](C(=O)O)N",
    ],
    "LGGdi12": [
        f"C(CCN(C(O)CO{C12})C(O)CO{C12})C[C@@H](C(=O)O)N",
        f"C(CCN(C(O{C12})CO)C(O)CO{C12})C[C@@H](C(=O)O)N",
        f"C(CCN(C(O{C12})CO)C(O{C12})CO)C[C@@H](C(=O)O)N",
        f"C(CCN(C(O)CO)C(O{C12})CO{C12})C[C@@H](C(=O)O)N",
    ],
    "LGGdi14": [
        f"C(CCN(C(O)CO{C14})C(O)CO{C14})C[C@@H](C(=O)O)N",
        f"C(CCN(C(O{C14})CO)C(O)CO{C14})C[C@@H](C(=O)O)N",
        f"C(CCN(C(O{C14})CO)C(O{C14})CO)C[C@@H](C(=O)O)N",
        f"C(CCN(C(O)CO)C(O{C14})CO{C14})C[C@@H](C(=O)O)N",
    ],
}

# update the database with generated smiles
new_smiles_list = []
inchi_list = []
reference_keys = []
reference_doi = []
mol_wts = []

for i, row in df.iterrows():
    code = row.compound
    new_smiles = ".".join(translations.get(code))

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

df["CMC"] = df["cac surface tension (mM)"] / 1000
df["pCMC"] = -np.log10(df.CMC)
df["Gamma_max"] = df["Γmax ( 106 mol/m2)"] / 10**6
df["Area_min"] = df["Amin (nm2)"]

df = df.rename(
    columns={
        "compound": "identifier",
        "γmin (mN/m)": "AW_ST_CMC",
        "Amin (nm2)": "Area_min",
    }
)

df = df.drop(
    columns=[
        "standard_deviation",
        "Γmax ( 106 mol/m2)",
        "standard_deviation",
        "standard_deviation",
        "cac conductivity (mM)",
        "standard_deviation",
        "cac ion chloride (mM)",
    ]
)

df.to_csv("processed_data/pinazo2009.csv", index=False)
