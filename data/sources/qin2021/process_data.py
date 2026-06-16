import json
import numpy as np
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


json_text = Path("source_data/name_smiles_mapping_based_on_cmc_edited.json").read_text()
translations = json.loads(json_text)

df = pd.read_csv("source_data/qin2021_table_S1.csv")
ref_df = pd.read_csv("source_data/qin2021_ref_mapping.csv")
bibtex_string = Path("../../CMC_database.bib").read_text(encoding="latin-1")
bib_database = bibtexparser.loads(bibtex_string)

smiles_list = []
inchi_list = []
dois = []
mol_wts = []
for i, row in df.iterrows():
    name = row.Surfactant
    ref_no = row.Ref
    smiles = translations.get(name, [""])[0]
    ref_key = ref_df[ref_df.reference == ref_no].key.iloc[0]
    doi = get_doi(ref_key, bib_database)

    dois.append(doi)
    mol = Chem.MolFromSmiles(smiles)

    if mol:
        sm = Chem.MolToSmiles(mol)
        inchi = Chem.MolToInchi(mol)
        mw = Descriptors.MolWt(mol)
        smiles_list.append(sm)
        inchi_list.append(inchi)
        mol_wts.append(mw)
    else:
        smiles_list.append("")
        inchi_list.append("")
        mol_wts.append("")

df["SMILES"] = smiles_list
df["Molecular_Weight"] = mol_wts
df["InChI"] = inchi_list
df["source_doi"] = "10.1021/acs.jpcb.1c05264"
df["reference_doi"] = dois
df["pCMC"] = -np.log10(df["Experimental CMC (M)"])
df.loc[df["Temperature (°C)"] == "room temperature", "Temperature (°C)"] = ""

df = df.rename(
    columns={
        "Surfactant": "identifier",
        "Experimental CMC (M)": "CMC",
        "Temperature (°C)": "Temp_Celsius",
    }
)
df = df.drop(
    columns=["Experimental log CMC (uM)", "Predicted log CMC (uM)", "Train/Test", "Ref"]
)

df.to_csv("processed_data/qin2021.csv", index=False)
