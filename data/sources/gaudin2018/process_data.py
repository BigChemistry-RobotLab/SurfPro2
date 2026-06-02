from rdkit import Chem
import pandas as pd
import json
from pathlib import Path
import bibtexparser
from rdkit.Chem import Descriptors


def canonicalise(smiles):
    mol = Chem.MolFromSmiles(smiles)
    return Chem.MolToSmiles(mol)


def get_doi(bibtex_key, bibtex_entries):
    for e in bib_database.entries:
        if e["ID"] == bibtex_key:
            doi = e.get("doi")
            if doi:
                return doi


df = pd.read_csv("source_data/gaudin2018_table_2.csv")
ref_df = pd.read_csv("source_data/ref_keys.csv").set_index("ref_no")
bibtex_string = Path("../../CMC_database.bib").read_text(encoding="utf-8")
bib_database = bibtexparser.loads(bibtex_string)

manual_translations = json.loads(Path("source_data/manual_names.json").read_text())

automatic_translations = json.loads(
    Path("source_data/names_to_identifiers.json").read_text()
)

smiles_list = []
inchi_list = []
reference_doi = []
ref_keys = []
mol_wts = []
for i, row in df.iterrows():
    name = row.Surfactant
    manual_smiles = manual_translations.get(name)
    auto_smiles = automatic_translations.get(name)

    ref_no = row["Reference"]
    ref_key = ref_df.loc[ref_no].iloc[0]
    doi = get_doi(ref_key, bib_database)
    if doi is None:
        print(ref_key)
    reference_doi.append(doi)
    ref_keys.append(ref_key)

    if manual_smiles:
        mol = Chem.MolFromSmiles(manual_smiles.get("SMILES"))
        sm = Chem.MolToSmiles(mol)
        mw = Descriptors.MolWt(mol)
        inchi = Chem.MolToInchi(mol)
        smiles_list.append(sm)
        inchi_list.append(inchi)
        mol_wts.append(mw)
    elif auto_smiles:
        mol = Chem.MolFromSmiles(auto_smiles.get("SMILES"))
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
df["InChI"] = inchi_list
df["Molecular_Weight"] = mol_wts
df["source_doi"] = "10.1016/j.jcis.2018.01.051"
df["reference_doi"] = reference_doi
df["ref_keys"] = ref_keys

df["Temp_Celsius"] = df[" T(K)"] - 272.15
df = df.rename(columns={"γCMC (mN/m)": "AW_ST_CMC"})
df = df.drop(columns=[" T(K)", "Set", "Reference"])

df.to_csv("processed_data/gaudin2018.csv", index=False)
