import bibtexparser
import pandas as pd
from pathlib import Path
from rdkit import Chem
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

    for e in bib_database.entries:
        if e["ID"] == bibtex_key:
            doi = e.get("isbn")
            if doi:
                return doi


C = "C"
OC2H4 = "OCC"
OC3H6 = "OCCC"
OH = "O"

translations = {
    "C6H13[(OC2H4)6OH]": C * 6 + OC2H4 * 6 + OH,
    "C10H21[(OC2H4)6OH]": C * 10 + OC2H4 * 6 + OH,
    "C10H21[(OC2H4)8OH]": C * 10 + OC2H4 * 8 + OH,
    "C12H25[(OC2H4)3OH]": C * 12 + OC2H4 * 3 + OH,
    "C12H25[(OC2H4)4OH]": C * 12 + OC2H4 * 4 + OH,
    "C12H25[(OC2H4)5OH]": C * 12 + OC2H4 * 5 + OH,
    "C12H25[(OC2H4)6OH]": C * 12 + OC2H4 * 6 + OH,
    "C12H25[(OC2H4)7OH]": C * 12 + OC2H4 * 7 + OH,
    "C12H25[(OC2H4)8OH]": C * 12 + OC2H4 * 8 + OH,
    "C12H25[(OC2H4)9OH]": C * 12 + OC2H4 * 9 + OH,
    "C12H25[(OC2H4)12OH]": C * 12 + OC2H4 * 12 + OH,
    "C13H27[(OC2H4)8OH]": C * 13 + OC2H4 * 8 + OH,
    "C14H29[(OC2H4)8OH]": C * 14 + OC2H4 * 8 + OH,
    "C15H31[(OC2H4)8OH]": C * 15 + OC2H4 * 8 + OH,
    "C16H33[(OC2H4)6OH]": C * 16 + OC2H4 * 6 + OH,
    "C16H33[(OC2H4)7OH]": C * 16 + OC2H4 * 7 + OH,
    "C16H33[(OC2H4)9OH]": C * 16 + OC2H4 * 9 + OH,
    "C16H33[(OC2H4)12OH]": C * 16 + OC2H4 * 12 + OH,
    "p-t-C8H17C6H4[(OC2H4)7OH]": "CC(C)(C)CC(C)(C)c1ccc(OCCOCCOCCOCCOCCOCCOCCO)cc1",
    "p-t-C8H17C6H4[(OC2H4)8OH]": "CC(C)(C)CC(C)(C)c1ccc(OCCOCCOCCOCCOCCOCCOCCOCCO)cc1",
    "p-t-C8H17C6H4[(OC2H4)9OH]": "CC(C)(C)CC(C)(C)c1ccc(OCCOCCOCCOCCOCCOCCOCCOCCOCCO)cc1",
    "p-t-C8H17C6H4[(OC2H4)10OH]": "CC(C)(C)CC(C)(C)c1ccc(OCCOCCOCCOCCOCCOCCOCCOCCOCCOCCO)cc1",
    "C12H25[(OC2H4)3(OC3H6)6OH]": C * 12 + OC2H4 * 3 + OC3H6 * 6 + OH,
    "C12H25[(OC2H4)4(OC3H6)5OH]": C * 12 + OC2H4 * 4 + OC3H6 * 5 + OH,
    "C12H25[(OC2H4)5(OC3H6)4OH]": C * 12 + OC2H4 * 5 + OC3H6 * 4 + OH,
    "C8H17[CHOHCH2OH]": "ambiguous",
    "C8H17[CHOHCH2CH2OH]": "ambiguous",
    "C10H21[CHOHCH2OH]": "ambiguous",
    "C10H21[CHOHCH2CH2OH]": "ambiguous",
    "C12H25[CHOHCH2CH2OH]": "ambiguous",
}

df = pd.read_csv("source_data/wang2005a_table_1.csv")
bibtex_string = Path("../../CMC_database.bib").read_text(encoding="latin-1")
bib_database = bibtexparser.loads(bibtex_string)

smiles_list = []
inchi_list = []
reference_doi = []
ref_keys = []
mol_wts = []
for i, row in df.iterrows():
    code = row["Structure (Tail [Head])"]
    ref_key = row["source"]
    sm = translations.get(code, "")

    if sm != "ambiguous":
        mol = Chem.MolFromSmiles(sm)
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

    if ref_key == "measured":
        reference_doi.append("10.1081/DIS-200054572")
    else:
        doi = get_doi(ref_key, bib_database)
        reference_doi.append(doi)

    ref_keys.append(ref_key)

df["SMILES"] = smiles_list
df["Molecular_Weight"] = mol_wts
df["InChI"] = inchi_list
df["Temp_Celsius"] = 25.0

df = df.rename(
    columns={"Structure (Tail [Head])": "identifier", "γobs.0/ mN.m-1": "AW_ST_CMC"}
)
df = df.drop(columns=["NO", " DHf/  kJ.mol-1 ", "KH0  ", "  γcal.0/  mN.m-1", "source"])
df = df[df.SMILES != ""]

df.to_csv("processed_data/wang2005a.csv", index=False)
