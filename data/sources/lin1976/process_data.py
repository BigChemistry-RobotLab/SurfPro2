import numpy as np
from pathlib import Path
from rdkit import Chem
import bibtexparser
import pandas as pd
from rdkit.Chem import Descriptors


def get_doi(bibtex_key, bibtex_entries):
    for e in bibtex_entries.entries:
        if e["ID"] == bibtex_key:
            doi = e.get("doi")
            if doi:
                return doi



structs = [
    "CnH2n+1(OCH2CH2)xOSO3Na",
    "CnH2n+1(OCH2CH2)xOSO3Na",
    "CnH2n+1(OCH2CH2)xOSO3Na",
    "CnH2n+1(OCH2CH2)xOSO3Na",
    "CnH2n+1(OCH2CH2)xOSO3Na",
    "CnH2n+1(OCH2CH2)xOSO3Na",
    "CnH2n+1(OCH2CH2)xOSO3Na",
    "CnH2n+1(OCH2CH2)xOSO3Na",
    "CnH2n+1(OCH2CH2)xOSO3Na",
    "CnH2n+1(OCH2CH2)xOSO3Na",
    "CnH2n+1(OCH2CH2)xOSO3Na",
    "CnH2n+1(OCH2CH2)xOSO3Na",
    "CnH2n+1(OCH2CH2)xOSO3Na",
    "CnH2n+1(OCH2CH2)xOSO3Na",
    "CnH2n+1(OCH2CH2)xOSO3Na",
    "CnH2n+1(OCH2CH2)xOSO3Na",
    "CnH2n+1(OCH2CH2)xN(CH3)3Cl",
    "CnH2n+1(OCH2CH2)xN(CH3)3Cl",
    "CnH2n+1(OCH2CH2)xN(CH3)3Cl",
    "CnH2n+1(OCH2CH2)xN(CH3)3Cl",
    "CnH2n+1(OCH2CH2)xN(CH3)3Cl",
    "CnH2n+1(OCH2CH2)xN(CH3)3Cl",
    "CnH2n+1(OCH2CH2)xN(CH3)3Cl",
    "CnH2n+1(OCH2CH2)xNC5H5Cl",
    "CnH2n+1(OCH2CH2)xNC5H5Cl",
    "CnH2n+1(OCH2CH2)xNC5H5Cl",
    "CnH2n+1(OCH2CH2)xNC5H5Cl",
    "CnH2n+1(OCH2CH2)xNC5H5Cl",
    "CnH2n+1(OCH2CH2)xNC5H5Cl",
    "CnH2n+1(OCH2CH2)xNC5H5Cl",
    "CnH2n+1(OCH2CH2)xNC5H5Cl",
    "CnH2n+1(OCH2CH2)xNC5H5Cl",
    "CnH2n+1(OCH2CH2)xNC5H5Cl",
]


n_numbers = [
    12,
    12,
    12,
    12,
    12,
    14,
    16,
    16,
    16,
    16,
    16,
    18,
    18,
    18,
    18,
    18,
    10,
    10,
    10,
    12,
    12,
    12,
    18,
    10,
    10,
    10,
    12,
    12,
    12,
    16,
    16,
    16,
    18,
]

x_numbers = [
    0,
    1,
    2,
    3,
    5,
    0,
    0,
    1,
    2,
    3,
    4,
    0,
    1,
    2,
    3,
    4,
    0,
    1,
    2,
    0,
    1,
    2,
    0,
    0,
    1,
    2,
    0,
    1,
    2,
    0,
    1,
    2,
    0,
]

end_groups = {
    "OSO3Na": "OS(=O)(=O)[O-].[Na+]",
    "N(CH3)3C1": "[N+](C)(C)C.[Cl-]",
    "NC5H5C1": "[n+]1ccccc1.[Cl-]",
}

OCC = "OCC"
C = "C"

df = pd.read_csv("source_data/lin1976_table_1.csv")
ref_df = pd.read_csv("source_data/references.csv").set_index("number")
bibtex_string = Path("../../CMC_database.bib").read_text(encoding="latin-1")
bib_database = bibtexparser.loads(bibtex_string)

new_smiles = []
inchi_list = []
reference_doi = []
mol_wts = []
for i, row in df.iterrows():
    end_group = row["Surfactant"].split("x")[-1]
    ref_num = row.Reference
    ref_key = ref_df.loc[ref_num, "ref"]

    end_group_sm = end_groups[end_group]
    n = row["(n)"]
    x = row["(x)"]
    smiles = "C" * n + "OCC" * x + end_group_sm
    mol = Chem.MolFromSmiles(smiles)
    sm = Chem.MolToSmiles(mol)
    inchi = Chem.MolToInchi(mol)
    mw = Descriptors.MolWt(mol)
    new_smiles.append(sm)
    inchi_list.append(inchi)
    mol_wts.append(mw)
    doi = get_doi(ref_key, bib_database)
    reference_doi.append(doi)

df["SMILES"] = new_smiles
df["InChI"] = inchi_list
df["Molecular_Weight"] = mol_wts

df["CMC"] = df["CMC(moleX1-1)"]
df["pCMC"] = -np.log10(df.CMC)

df["source_doi"] = "10.1016/0021-9797(76)90178-8"
df["reference_doi"] = reference_doi

df = df.drop(columns=["Surfactant", "(n)", "(x)", "CMC(moleX1-1)", "Neff", "Reference"])

df.to_csv("processed_data/lin1976.csv", index=False)
