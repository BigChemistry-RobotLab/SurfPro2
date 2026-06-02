import pandas as pd
from rdkit import Chem
from pathlib import Path
import bibtexparser
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


df = pd.read_csv("source_data/li2004_table_1.csv")
identifiers_to_smiles = pd.read_csv("source_data/identifiers_to_smiles.csv").set_index(
    "identifier"
)
df_ref = pd.read_csv("source_data/references.csv", index_col="number")
bibtex_string = Path("../../CMC_database.bib").read_text(encoding="latin-1")
bib_database = bibtexparser.loads(bibtex_string)

# update the database with generated smiles
new_smiles_list = []
reference_keys = []
reference_doi = []
inchi_list = []
mol_wts = []
for i, row in df.iterrows():
    code = row["Structures (hydrophobic-hydrophilic segments)"]
    ref_num = row.ref_no
    ref_key = df_ref.loc[ref_num, "ref_key"]

    new_smiles = identifiers_to_smiles.loc[code].SMILES

    if pd.isna(new_smiles):
        new_smiles_list.append("")
        inchi_list.append("")
        mol_wts.append(None)
    else:
        mol = Chem.MolFromSmiles(new_smiles)
        new_smiles = Chem.MolToSmiles(mol)
        inchi = Chem.MolToInchi(mol)
        mw = Descriptors.MolWt(mol)

        inchi_list.append(inchi)
        new_smiles_list.append(new_smiles)
        mol_wts.append(mw)

    doi = get_doi(ref_key, bib_database)

    reference_doi.append(doi)
    reference_keys.append(ref_key)

df["SMILES"] = new_smiles_list
df["InChI"] = inchi_list
df["Molecular_Weight"] = mol_wts

df["source_doi"] = "10.1016/j.theochem.2004.08.039"
df["reference_doi"] = reference_doi
df["reference_key"] = reference_keys

df["pCMC"] = df["Log10 cmc (exp)"]
df["CMC"] = 10**df.pCMC

df = df.rename(
    columns={
        "Structures (hydrophobic-hydrophilic segments)": "identifier",
    }
)
df = df.drop(
    columns=[
        "No.",
        "NT",
        "m (D)",
        "QC-max (a.u.)",
        "Log10 cmc (exp)",
        "ref_no",
        "Log10 cmc (cal)",
        "Cv-residuals",
        "Counterion",
    ]
)

df = df[~(df.SMILES == "")]

df.to_csv("processed_data/li2004.csv", index=False)
