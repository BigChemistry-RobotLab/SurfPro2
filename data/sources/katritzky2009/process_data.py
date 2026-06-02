from pathlib import Path
from rdkit import Chem
import bibtexparser
import pandas as pd
from rdkit.Chem import Descriptors


def canonicalise(smiles):
    mol = Chem.MolFromSmiles(smiles)
    return Chem.MolToSmiles(mol)


def get_doi(bibtex_key, bibtex_entries):
    for e in bibtex_entries.entries:
        if e["ID"] == bibtex_key:
            doi = e.get("doi")
            if doi:
                return doi


df = pd.read_csv("source_data/katritzky2009_table_1.csv")
bibtex_string = Path("../../CMC_database.bib").read_text(encoding="latin-1")
bib_database = bibtexparser.loads(bibtex_string)
names_to_smiles = pd.read_csv("source_data/names_to_smiles.csv").set_index(
    "Chemical name"
)


smiles_list = []
inchi_list = []
reference_keys = []
reference_doi = []
mol_wts = []
for i, row in df.iterrows():
    identifier = row["Chemical name"]
    ref_key = row["ref_key"]
    doi = get_doi(ref_key, bib_database)
    reference_doi.append(doi)
    reference_keys.append(ref_key)

    smiles = names_to_smiles.loc[identifier, "OPSIN SMILES"]
    if pd.isna(smiles):
        smiles = names_to_smiles.loc[identifier, "Handmade SMILES"]

    mol = Chem.MolFromSmiles(smiles)
    smiles = Chem.MolToSmiles(mol)
    inchi = Chem.MolToInchi(mol)
    mw = Descriptors.MolWt(mol)
    smiles_list.append(smiles)
    inchi_list.append(inchi)
    mol_wts.append(mw)

df["SMILES"] = smiles_list
df["Molecular_Weight"] = mol_wts
df["InChI"] = inchi_list
df["source_doi"] = "10.1016/j.compchemeng.2008.09.011"
df["reference_doi"] = reference_doi
df["reference_key"] = reference_keys

df = df.rename(
    columns={
        "1st pCMC Exp.": "pCMC",
        "Chemical name": "identifier",
    }
)

df["CMC"] = 10**-df.pCMC

df = df.drop(
    columns=[
        "No.",
        "References",
        "1st pCMC Predicted model in Table 2",
        "1st pCMC General ANN Predicted",
        "2nd pCMC Exp.",
        "2nd pCMC Predicted model in Table 3",
        "ref_key",
    ]
)

df.to_csv("processed_data/katritzky2009.csv", index=False)
