import numpy as np
from string import Template
import pandas as pd
from pathlib import Path
from rdkit import Chem
import bibtexparser
from rdkit.Chem import Descriptors

df = pd.read_csv("source_data/quagliotto2005_table_2.csv")
df_mapping = pd.read_csv("source_data/smiles_mapping.csv").set_index("compound_id")
bibtex_string = Path("../../CMC_database.bib").read_text(encoding="utf-8")
bib_database = bibtexparser.loads(bibtex_string)


smiles_list = []
reference_doi = []
inchi_list = []
mol_wts = []
ref_keys = []
for i, row in df.iterrows():
    id = row.compd
    if id in df_mapping.index:
        smiles = df_mapping.loc[id].SMILES

        mol = Chem.MolFromSmiles(smiles)
        smiles = Chem.MolToSmiles(mol)
        inchi = Chem.MolToInchi(mol)
        mw = Descriptors.MolWt(mol)

        smiles_list.append(smiles)
        inchi_list.append(inchi)
        mol_wts.append(mw)

    else:
        smiles_list.append("")
        inchi_list.append("")
        mol_wts.append("")


df["SMILES"] = smiles_list
df["Molecular_Weight"] = mol_wts
df["InChI"] = inchi_list

df["CMC"] = df["cmc surface tension (a) (mM)"] / 1000
df["pCMC"] = -np.log10(df.CMC)
# Incorrect units in paper?
# df["Gamma_max"] = df["Γmax (mol cm-2)"] * 1000
df["Area_min"] = df["Amin (Å2)"] / 10

df = df.drop(
    columns=[
        "compd",
        "cmc surface tension (a) (mM)",
        " cmcb conductivity (b) (mM)",
        "ratioc b/a",
        "cmc/C20",
        "Γmax (mol cm-2)",
    ]
)
df = df.rename(
    columns={
        "γcmc (mN/m)": "AW_ST_CMC",
    }
)
df = df[df.SMILES != ""]
df.to_csv("processed_data/quagliotto2005.csv", index=False)
