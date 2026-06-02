import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors
import bibtexparser
from pathlib import Path


def get_doi(bibtex_key, bibtex_entries):
    for e in bibtex_entries.entries:
        if e["ID"] == bibtex_key:
            doi = e.get("doi")
            if doi:
                return doi


df = pd.read_csv("source_data/su2011_table_1.csv")
bibtex_string = Path("../../CMC_database.bib").read_text(encoding="latin-1")
bib_database = bibtexparser.loads(bibtex_string)

translations = {
    "12-3OH-12 2Cl-": "CCCCCCCCCCCC[N+](C)(C)CC(O)C[N+](C)(C)CCCCCCCCCCCC.[Cl-].[Cl-]",
    "12-3AG-12 2Cl-": "CCCCCCCCCCCC[N+](C)(C)CC(OC(=O)C=C)C[N+](C)(C)CCCCCCCCCCCC.[Cl-].[Cl-]",
    "12’-2-12’ 2Br-": "?",
    "12-3-12 2Cl-": "?",
    "DTAB": "CCCCCCCCCCCC[N+](C)(C)C.[Br-]",
}

# update the database with generated smiles
new_smiles_list = []
inchi_list = []
reference_doi = []
mol_wts = []
for i, row in df.iterrows():
    code = row.identifier
    new_smiles = translations.get(code)
    ref_key = row.ref
    doi = get_doi(ref_key, bib_database)

    if new_smiles == "?":
        new_smiles_list.append("")
        inchi_list.append("")
        mol_wts.append("")
        reference_doi.append("")
        continue

    mol = Chem.MolFromSmiles(new_smiles)
    smiles = Chem.MolToSmiles(mol)
    inchi = Chem.MolToInchi(mol)
    mw = Descriptors.MolWt(mol)

    new_smiles_list.append(smiles)
    inchi_list.append(inchi)
    mol_wts.append(mw)
    reference_doi.append(doi)


df["SMILES"] = new_smiles_list
df["InChI"] = inchi_list
df["Molecular_Weight"] = mol_wts
df["Gamma_max"] = df["106ΓCMC (mol/m2)"] / 10**6
df["Temp_Celsius"] = 25.0

df = df.rename(
    columns={
        "Surfactant": "identifier",
        "CMC (mol/l)": "CMC",
        "γCMC (mN/m)": "AW_ST_CMC",
        "ACMC (nm2/molecule)": "Area-min",
    }
)

df["pCMC"] = -np.log10(df.CMC)

df = df.drop(
    columns=[
        "106ΓCMC (mol/m2)",
        "CMC/C20",
        "ref",
    ]
)
df = df[~(df.SMILES == "")]

df.to_csv("processed_data/su2011.csv", index=False)
