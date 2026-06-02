import numpy as np
import json
import pandas as pd
from pathlib import Path
from rdkit import Chem
import bibtexparser
from rdkit.Chem import Descriptors

def get_doi(bibtex_key, bibtex_entries):
    for e in bib_database.entries:
        if e["ID"] == bibtex_key:
            doi = e.get("doi")
            if doi:
                return doi


names_to_id = json.loads(Path("source_data/names_to_identifiers.json").read_text(encoding="utf-8"))
refs = pd.read_csv("source_data/references.csv")
refs = refs.set_index("ref")
bibtex_string = Path("../../CMC_database.bib").read_text(encoding="latin-1")
bib_database = bibtexparser.loads(bibtex_string)

df = pd.read_csv("source_data/gaudin2016_table_2.csv")

smiles_list = []
inchi_list = []
reference_keys = []
reference_doi = []
mol_wts = []
for i, row in df.iterrows():
    entry = names_to_id.get(row.molecule)

    ref = row.ref
    ref_key = refs.loc[ref][0]
    doi = get_doi(ref_key, bib_database)

    reference_doi.append(doi)
    reference_keys.append(ref_key)

    if entry is None:
        print("Missed",row.molecule)
        smiles_list.append("")
        inchi_list.append("")
        mol_wts.append("")
        continue

    sm = entry.get("SMILES", "")
    mol = Chem.MolFromSmiles(sm)

    if mol is None:
        smiles_list.append("")
        inchi_list.append("")
        mol_wts.append("")
    else:
        mw = Descriptors.MolWt(mol)
        new_sm = Chem.MolToSmiles(mol)
        inchi = Chem.MolToInchi(mol)
        smiles_list.append(new_sm)
        inchi_list.append(inchi)
        mol_wts.append(mw)

df["SMILES"] = smiles_list
df["Molecular_Weight"] = mol_wts
df["InChI"] = inchi_list
df["pCMC"] = -np.log10(df["CMC (mM)"] / 1000)
df["CMC"] = df["CMC (mM)"] / 1000
df["source_doi"] = "10.1021/acs.iecr.6b02890"
df["reference_doi"] = reference_doi
df = df.rename(columns={"molecule": "identifier", "T (°C)": "Temp_Celsius"})
df = df.drop(columns=["set", "CMC (mM)", "log CMC (M)"])
df = df[~(df.SMILES=="")]

df.to_csv("processed_data/gaudin2016.csv", index=False)
