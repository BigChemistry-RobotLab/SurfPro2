import numpy as np
from pathlib import Path
from rdkit import Chem
import bibtexparser
import pandas as pd
from rdkit.Chem import Descriptors
import pandas as pd

df = pd.read_csv("source_data/ricardo2023_table_s6.csv")
df_ref = pd.read_csv("source_data/ChemEngSci_2023_265_118208_refs.csv").set_index(
    "number"
)

smiles_list = []
inchi_list = []
reference_doi = []
mol_wts = []
for i, row in df.iterrows():
    idx = row.Reference
    doi = df_ref.loc[idx].doi

    smiles = row.SMILES

    if doi == "n.d.":
        smiles_list.append("")
        inchi_list.append("")
        mol_wts.append("")
        reference_doi.append("")
        continue

    mol = Chem.MolFromSmiles(smiles)

    if mol is None:
        smiles_list.append("")
        inchi_list.append("")
        mol_wts.append("")
        reference_doi.append("")
    else:
        smiles = Chem.MolToSmiles(mol)
        inchi = Chem.MolToInchi(mol)
        mw = Descriptors.MolWt(mol)

        smiles_list.append(smiles)
        inchi_list.append(inchi)
        mol_wts.append(mw)
        reference_doi.append(doi)

df["SMILES"] = smiles_list
df["Molecular_Weight"] = mol_wts
df["InChI"] = inchi_list
df["source_doi"] = "10.1016/j.ces.2022.118208"
df["reference_doi"] = reference_doi

df = df.rename(
    columns={
        "STCMC (mN/m)": "AW_ST_CMC",
    }
)

df = df.drop(columns=["Number", "Reference"])

df = df[df.SMILES != ""]

df.to_csv("processed_data/ricardo2023.csv", index=False)
