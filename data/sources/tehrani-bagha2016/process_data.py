import numpy as np
import pandas as pd
from rdkit import Chem
from pathlib import Path
import bibtexparser
from rdkit.Chem import Descriptors


def get_doi(bibtex_key, bibtex_entries):
    for e in bibtex_entries.entries:
        if e["ID"] == bibtex_key:
            doi = e.get("doi")
            if doi:
                return doi


# Compare to manual transcription
df = pd.read_csv("source_data/tehrani-bagha2016_table_1.csv")
df_maps = pd.read_csv("source_data/mappings.csv").set_index("Surfactant")
bibtex_string = Path("../../CMC_database.bib").read_text(encoding="latin-1")
bib_database = bibtexparser.loads(bibtex_string)

# update the database with generated smiles
new_smiles_list = []
inchi_list = []
reference_keys = []
reference_doi = []
mol_wts = []

for i, row in df.iterrows():
    code = row.Surfactant
    new_smiles = df_maps.loc[code].SMILES

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

df["CMC"] = df["CMC (mM)"] / 1000
df["pCMC"] = -np.log10(df.CMC)

df = df.rename(
    columns={
        "γ_CMC (mN/m)": "AW_ST_CMC",
    }
)
df = df.drop(columns=["CMC (mM)", "−[dγ/dlnC]T"])
df = df[~(df.SMILES == "")]

df.to_csv("processed_data/tehrani-bagha2016.csv", index=False)
