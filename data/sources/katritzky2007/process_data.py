from string import Template
import pandas as pd
from pathlib import Path
from rdkit import Chem
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


C = "C"
EO = "OCC"
SO4Na = "OS(=O)(=O)[O-]" + ".[Na+]"
CO2K = "C(=O)[O-]" + ".[K+]"
CO2 = "C(=O)O"
SO3Na = "S(=O)(=O)([O-])" + ".[Na+]"
CF4 = "FC(F)(F)C(F)(F)C(F)(F)C(F)(F)"
CF6 = "FC(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)"
CF8 = "FC(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)"
PO4H2 = "OP(=O)(O)(O)"
OH = "O"
nGlupyr = Template(f"C({SO4Na})[C@H]1O[C@H](OC)[C@H](N($R))[C@@H](O)[C@@H]1O")
paraPh = Template("c1cc($chain_1)ccc1($chain_2)")

translations = {
    "C6SO4Na": C * 6 + SO4Na,
    "C7SO4Na": C * 7 + SO4Na,
    "C9SO4Na": C * 9 + SO4Na,
    "C8CO2K": C * 8 + CO2K,
    "C10CO2K": C * 10 + CO2K,
    "C12CO2K": C * 12 + CO2K,
    "C14CO2K": C * 14 + CO2K,
    "C16CO2K": C * 16 + CO2K,
    "C6C(C)SO4Na": C * 6 + C + f"({C * 1})" + SO4Na,
    "C8C(C2)SO4Na": C * 8 + C + f"({C * 2})" + SO4Na,
    "C5C(C5)SO4Na": C * 5 + C + f"({C * 5})" + SO4Na,
    "C11C(C)SO4Na": C * 11 + C + f"({C * 1})" + SO4Na,
    "C6C(C6)SO4Na": C * 6 + C + f"({C * 6})" + SO4Na,
    "C14C(C14)SO4Na": C * 14 + C + f"({C * 14})" + SO4Na,
    "C10PhSO3Na": paraPh.substitute(chain_1=C * 10, chain_2=SO3Na),
    "C12PhSO3Na": paraPh.substitute(chain_1=C * 12, chain_2=SO3Na),
    "C8C(C2)PhSO3Na": paraPh.substitute(
        chain_1=C + f"({C * 8})" + f"({C * 2})", chain_2=SO3Na
    ),
    "C7C(C3)PhSO3Na": paraPh.substitute(
        chain_1=C + f"({C * 7})" + f"({C * 3})", chain_2=SO3Na
    ),
    "C6C(C4)PhSO3Na": paraPh.substitute(
        chain_1=C + f"({C * 6})" + f"({C * 4})", chain_2=SO3Na
    ),
    "C5C(C5)PhSO3Na": paraPh.substitute(
        chain_1=C + f"({C * 5})" + f"({C * 5})", chain_2=SO3Na
    ),
    "C7C(C4)PhSO3Na": paraPh.substitute(
        chain_1=C + f"({C * 7})" + f"({C * 4})", chain_2=SO3Na
    ),
    "C10C(C2)PhSO3Na": paraPh.substitute(
        chain_1=C + f"({C * 10})" + f"({C * 2})", chain_2=SO3Na
    ),
    "C9C(C3)PhSO3Na": paraPh.substitute(
        chain_1=C + f"({C * 9})" + f"({C * 3})", chain_2=SO3Na
    ),
    "C8C(C4)PhSO3Na": paraPh.substitute(
        chain_1=C + f"({C * 8})" + f"({C * 4})", chain_2=SO3Na
    ),
    "C7C(C5)PhSO3Na": paraPh.substitute(
        chain_1=C + f"({C * 7})" + f"({C * 5})", chain_2=SO3Na
    ),
    "C6C(C6)PhSO3Na": paraPh.substitute(
        chain_1=C + f"({C * 6})" + f"({C * 6})", chain_2=SO3Na
    ),
    "C12C(C)PhSO3Na": paraPh.substitute(
        chain_1=C + f"({C * 12})" + f"({C * 1})", chain_2=SO3Na
    ),
    "C11C(C2)PhSO3Na": paraPh.substitute(
        chain_1=C + f"({C * 11})" + f"({C * 2})", chain_2=SO3Na
    ),
    "C10C(C3)PhSO3Na": paraPh.substitute(
        chain_1=C + f"({C * 10})" + f"({C * 3})", chain_2=SO3Na
    ),
    "C9C(C4)PhSO3Na": paraPh.substitute(
        chain_1=C + f"({C * 9})" + f"({C * 4})", chain_2=SO3Na
    ),
    "C8C(C5)PhSO3Na": paraPh.substitute(
        chain_1=C + f"({C * 8})" + f"({C * 5})", chain_2=SO3Na
    ),
    "C7C(C6)PhSO3Na": paraPh.substitute(
        chain_1=C + f"({C * 7})" + f"({C * 6})", chain_2=SO3Na
    ),
    "C10EO2SO4Na": C * 10 + EO * 2 + SO4Na,
    "C12EO4SO4Na": C * 12 + EO * 4 + SO4Na,
    "C14EOSO4Na": C * 14 + EO + SO4Na,
    "C14EO2SO4Na": C * 14 + EO * 2 + SO4Na,
    "C14EO4SO4Na": C * 14 + EO * 4 + SO4Na,
    "C16EO2SO4Na": C * 16 + EO * 2 + SO4Na,
    "C8CO2C2SO3Na": C * 8 + CO2 + C * 2 + SO3Na,
    "C10CO2C2SO3Na": C * 10 + CO2 + C * 2 + SO3Na,
    "C12CO2C2SO3Na": C * 12 + CO2 + C * 2 + SO3Na,
    # ! misleading structure codes and incorrect pCMC values
    "CF4C2C(C3)SO4Na": "",
    "CF6C2C(C3)SO4Na": "",
    "CF8C2C(C3)SO4Na": "",
    "CF4C2C(C5)SO4Na": "",
    "CF6C2C(C5)SO4Na": "",
    "CF8C2C(C5)SO4Na": "",
    "CF4C2C(C7)SO4Na": "",
    "CF6C2C(C7)SO4Na": "",
    "CF8C2C(C7)SO4Na": "",
    "CC(C)C5PhEO10PO4H2": paraPh.substitute(
        chain_1="CC(C)" + C * 5, chain_2=EO * 10 + PO4H2
    ),
    "CC(C)C5PhEO15PO4H2": paraPh.substitute(
        chain_1="CC(C)" + C * 5, chain_2=EO * 15 + PO4H2
    ),
    "CC(C)C5PhEO20PO4H2": paraPh.substitute(
        chain_1="CC(C)" + C * 5, chain_2=EO * 20 + PO4H2
    ),
    "C7C(O)NGlupyrSO4Na": nGlupyr.substitute(R="C(=O)" + C * 7),
    "C11C(O)NGlupyrSO4Na": nGlupyr.substitute(R="C(=O)" + C * 11),
    "C15C(O)NGlupyrSO4Na": nGlupyr.substitute(R="C(=O)" + C * 15),
    "C5PhePhSO3Na": f"c1cccc({SO3Na})c1C(=O)N[C@H](Cc1ccccc1)C(=O)O" + C * 5,
    "C8PhePhSO3Na": f"c1cccc({SO3Na})c1C(=O)N[C@H](Cc1ccccc1)C(=O)O" + C * 8,
    "C10PhePhSO3Na": f"c1cccc({SO3Na})c1C(=O)N[C@H](Cc1ccccc1)C(=O)O" + C * 10,
    "C12PheSO3Na": f"c1cccc({SO3Na})c1C(=O)N[C@H](Cc1ccccc1)C(=O)O" + C * 12,
    "C14PhePhSO3Na": f"c1cccc({SO3Na})c1C(=O)N[C@H](Cc1ccccc1)C(=O)O" + C * 14,
    "C12AlaPhSO3Na": f"c1cccc({SO3Na})c1C(=O)N[C@H](C)C(=O)O" + C * 12,
    "C6SO3Na": C * 6 + SO3Na,
    "C8SO3Na": C * 8 + SO3Na,
    "C10SO3Na": C * 10 + SO3Na,
    "C12SO3Na": C * 12 + SO3Na,
    "C13SO3Na": C * 13 + SO3Na,
    "C14SO3Na": C * 14 + SO3Na,
    "C15SO3Na": C * 15 + SO3Na,
    "C16SO3Na": C * 16 + SO3Na,
    "C17SO3Na": C * 17 + SO3Na,
    "C10C=dCSO3Na": C * 10 + "=C" + SO3Na,
    "C12C=dCSO3Na": C * 12 + "=C" + SO3Na,
    "C14C=dCSO3Na": C * 14 + "=C" + SO3Na,
    "C16C=dCSO3Na": C * 16 + "=C" + SO3Na,
    "C10C(C)SO3Na": C * 10 + C + f"({C * 1})" + SO3Na,
    "C9C(C2)SO3Na": C * 9 + C + f"({C * 2})" + SO3Na,
    "C8C(C3)SO3Na": C * 8 + C + f"({C * 3})" + SO3Na,
    "C7C(C4)SO3Na": C * 7 + C + f"({C * 4})" + SO3Na,
    "C6C(C5)SO3Na": C * 6 + C + f"({C * 5})" + SO3Na,
    "C7C(C7)SO3Na": C * 7 + C + f"({C * 7})" + SO3Na,
    "C7PhSO3Na": paraPh.substitute(chain_1=C * 7, chain_2=SO3Na),
    "C8PhSO3Na": paraPh.substitute(chain_1=C * 8, chain_2=SO3Na),
    "C6C(C2)PhSO3Na": paraPh.substitute(
        chain_1=C + f"({C * 2})" + C * 6, chain_2=SO3Na
    ),
    "C8C(C)PhSO3Na": paraPh.substitute(chain_1=C + f"({C * 1})" + C * 8, chain_2=SO3Na),
    "C7C(C2)PhSO3Na": paraPh.substitute(
        chain_1=C + f"({C * 2})" + C * 7, chain_2=SO3Na
    ),
    "C5C(C4)PhSO3Na": paraPh.substitute(
        chain_1=C + f"({C * 4})" + C * 5, chain_2=SO3Na
    ),
    "C9C(C)PhSO3Na": paraPh.substitute(chain_1=C + f"({C * 1})" + C * 9, chain_2=SO3Na),
    "C10C(C)PhSO3Na": paraPh.substitute(
        chain_1=C + f"({C * 1})" + C * 10, chain_2=SO3Na
    ),
    "C9C(C2)PhSO3Na": paraPh.substitute(
        chain_1=C + f"({C * 2})" + C * 9, chain_2=SO3Na
    ),
    "C8C(C3)PhSO3Na": paraPh.substitute(
        chain_1=C + f"({C * 3})" + C * 8, chain_2=SO3Na
    ),
    "C6C(C5)PhSO3Na": paraPh.substitute(
        chain_1=C + f"({C * 5})" + C * 6, chain_2=SO3Na
    ),
    "C11C(C)PhSO3Na": paraPh.substitute(
        chain_1=C + f"({C * 1})" + C * 11, chain_2=SO3Na
    ),
    "C13C(C)PhSO3Na": paraPh.substitute(
        chain_1=C + f"({C * 1})" + C * 13, chain_2=SO3Na
    ),
    "C8SO4Na": C * 8 + SO4Na,
    "C10SO4Na": C * 10 + SO4Na,
    "C11SO4Na": C * 11 + SO4Na,
    "C12SO4Na": C * 12 + SO4Na,
    "C13SO4Na": C * 13 + SO4Na,
    "C14SO4Na": C * 14 + SO4Na,
    "C15SO4Na": C * 15 + SO4Na,
    "C16SO4Na": C * 16 + SO4Na,
    "C18SO4Na": C * 18 + SO4Na,
    "C8C(C)SO4Na": C * 8 + C + f"({C * 1})" + SO4Na,
    "C12C(C)SO4Na": C * 12 + C + f"({C * 1})" + SO4Na,
    "C11C(C2)SO4Na": C * 11 + C + f"({C * 2})" + SO4Na,
    "C10C(C3)SO4Na": C * 10 + C + f"({C * 3})" + SO4Na,
    "C9C(C4)SO4Na": C * 9 + C + f"({C * 4})" + SO4Na,
    "C7C(C6)SO4Na": C * 7 + C + f"({C * 6})" + SO4Na,
    "C13C(C)SO4Na": C * 13 + C + f"({C * 1})" + SO4Na,
    "C12C(C2)SO4Na": C * 12 + C + f"({C * 2})" + SO4Na,
    "C10C(C4)SO4Na": C * 10 + C + f"({C * 4})" + SO4Na,
    "C7C(C7)SO4Na": C * 7 + C + f"({C * 7})" + SO4Na,
    "C12C(C3)SO4Na": C * 12 + C + f"({C * 3})" + SO4Na,
    "C10C(C5)SO4Na": C * 10 + C + f"({C * 5})" + SO4Na,
    "C8C(C7)SO4Na": C * 8 + C + f"({C * 7})" + SO4Na,
    "C15C(C)SO4Na": C * 15 + C + f"({C * 1})" + SO4Na,
    "C8C(C8)SO4Na": C * 8 + C + f"({C * 8})" + SO4Na,
    "C16C(C)SO4Na": C * 16 + C + f"({C * 1})" + SO4Na,
    "C14C(C3)SO4Na": C * 14 + C + f"({C * 3})" + SO4Na,
    "C12C(C5)SO4Na": C * 12 + C + f"({C * 5})" + SO4Na,
    "C9C(C9)SO4Na": C * 9 + C + f"({C * 9})" + SO4Na,
    "C14C(C4)SO4Na": C * 14 + C + f"({C * 4})" + SO4Na,
    "C13C(C)CSO4Na": C * 13 + C + f"({C * 1})" + C + SO4Na,
    "C12C(C2)CSO4Na": C * 12 + C + f"({C * 2})" + C + SO4Na,
    "C11C(C3)CSO4Na": C * 11 + C + f"({C * 3})" + C + SO4Na,
    "C10C(C4)CSO4Na": C * 10 + C + f"({C * 4})" + C + SO4Na,
    "C9C(C5)CSO4Na": C * 9 + C + f"({C * 5})" + C + SO4Na,
    "C8C(C6)CSO4Na": C * 8 + C + f"({C * 6})" + C + SO4Na,
    "C7C(C7)CSO4Na": C * 7 + C + f"({C * 7})" + C + SO4Na,
    "C12EOSO4Na": C * 12 + EO * 1 + SO4Na,
    "C12EO2SO4Na": C * 12 + EO * 2 + SO4Na,
    "C9C(OH)C2SO3Na": C * 9 + f"({OH})" + C * 2 + SO3Na,
    "C9C(OC)C2SO3Na": C * 9 + C + "(OC)" + C * 2 + SO3Na,
    "C9C(OC2)C2SO3Na": C * 9 + C + "(OCC)" + C * 2 + SO3Na,
    "C9C(OC3)C2SO3Na": C * 9 + C + "(OCCC)" + C * 2 + SO3Na,
    "C9C(OC(C)C)C2SO3Na": C * 9 + C + "(OC(C)C)" + C * 2 + SO3Na,
    "C9C(OC4)C2SO3Na": C * 9 + C + "(OCCCC)" + C * 2 + SO3Na,
    "C9C(OC6)C2SO3Na": C * 9 + C + "(OCCCCCC)" + C * 2 + SO3Na,
    "C9C(OC8)C2SO3Na": C * 9 + C + "(OCCCCCCCC)" + C * 2 + SO3Na,
    "C9C(OCC(C2)C4)C2SO3Na": C * 9 + C + "(OCC(CC)CCCC)" + C * 2 + SO3Na,
    "C9C(OPh)C2SO3Na": C * 9 + C + "(Oc1ccccc1)" + C * 2 + SO3Na,
    "C9C(O)C2SO3Na": C * 9 + C + "(O)" + C * 2 + SO3Na,
    "C11C(OH)C2SO3Na": C * 11 + C + "(O)" + C * 2 + SO3Na,
    "C11C(OC2OH)C2SO3Na": C * 11 + C + "(CCO)" + C * 2 + SO3Na,
    "C11C(EO2)C2SO3Na": C * 11 + C + f"({EO * 2}O)" + C * 2 + SO3Na,
    "C11C(OPh)C2SO3Na": C * 11 + C + "(Oc1ccccc1)" + C * 2 + SO3Na,
    "C11C(OPhCl3)C2SO3Na": "CCCCCCCCCCCC(CCS(=O)(=O)[O-])Oc1cc(Cl)c(Cl)cc1Cl.[Na+]",
    "C11C(N(C)2)C2SO3Na": C * 11 + C + "(N(C)C)" + C * 2 + SO3Na,
    "C11C(NC3)C2SO3Na": C * 11 + C + "(NCCC)" + C * 2 + SO3Na,
    "C11C(NC4)C2SO3Na": C * 11 + C + "(NCCCC)" + C * 2 + SO3Na,
    "C11C(morpholino)C2SO3Na": C * 11 + C + "(N1CCOCC1)" + C * 2 + SO3Na,
    "C11C(piperidino)C2SO3Na": C * 11 + C + "(N1CCCCC1)" + C * 2 + SO3Na,
    "C11C(O)C2SO3Na": C * 11 + C + "(=O)" + C * 2 + SO3Na,
    "C13C(OH)C2SO3Na": C * 13 + C + "(O)" + C * 2 + SO3Na,
    "C13C(OC)C2SO3Na": C * 13 + C + "(OC)" + C * 2 + SO3Na,
    "C13C(OC3)C2SO3Na": C * 13 + C + "(OCCC)" + C * 2 + SO3Na,
    "C13C(OC4)C2SO3Na": C * 13 + C + "(OCCCC)" + C * 2 + SO3Na,
    "C13C(O)C2SO3Na": C * 13 + C + "(=O)" + C * 2 + SO3Na,
    "C15C(OH)C2SO3Na": C * 15 + C + "(O)" + C * 2 + SO3Na,
    "C10EOSO3Na": C * 10 + EO + SO3Na,
    "C10C(C(OH))SO3Na": C * 10 + C + "(CO)" + SO3Na,
    "C12C(C(OH))SO3Na": C * 12 + C + "(CO)" + SO3Na,
    "C6CO2CSO3Na": C * 6 + "OC(=O)C" + SO3Na,
    "C8CO2CSO3Na": C * 8 + "OC(=O)C" + SO3Na,
    "C10CO2CSO3Na": C * 10 + "OC(=O)C" + SO3Na,
    "C14CO2C2SO3Na": C * 14 + "OC(=O)CC" + SO3Na,
    "C10C(CO2C)SO3Na": C * 10 + "C(C(=O)OC)" + SO3Na,
    "C12C(CO2C)SO3Na": C * 12 + "C(C(=O)OC)" + SO3Na,
    "C14C(CO2C)SO3Na": C * 14 + "C(C(=O)OC)" + SO3Na,
    "C14C(CO2C2)SO3Na": C * 14 + "C(C(=O)OCC)" + SO3Na,
    "C14C(CO2C3)SO3Na": C * 14 + "C(C(=O)OCCC)" + SO3Na,
    "C16C(CO2C)SO3Na": C * 16 + "C(C(=O)OC)" + SO3Na,
    "C16C(CO2C2)SO3Na": C * 16 + "C(C(=O)OCC)" + SO3Na,
    "C16C(CO2C3)SO3Na": C * 16 + "C(C(=O)OCCC)" + SO3Na,
    "C16C(CO2C(C)C)SO3Na": C * 16 + "C(C(=O)OC(C)C)" + SO3Na,
    "C4C(C2)CCO2CC(SO3Na)-CO2CC(C2)C4": f"CCCCC(CC)COC(=O)CC({SO3Na})C(=O)OCC(CC)CCCC",
    "C4CO2C(SO3Na)CCO2C4": C * 4 + "OC(=O)" + C + f"({SO3Na})" + C + "C(=O)O" + C * 4,
    "C5CO2C(SO3Na)CCO2C5": C * 5 + "OC(=O)" + C + f"({SO3Na})" + C + "C(=O)O" + C * 5,
    "C6CO2C(SO3Na)CCO2C6": C * 6 + "OC(=O)" + C + f"({SO3Na})" + C + "C(=O)O" + C * 6,
    "C8CO2C(SO3Na)CCO2C8": C * 8 + "OC(=O)" + C + f"({SO3Na})" + C + "C(=O)O" + C * 8,
}

df = pd.read_csv("source_data/table_1.csv")
bibtex_string = Path("../../CMC_database.bib").read_text(encoding="utf-8")
bib_database = bibtexparser.loads(bibtex_string)

smiles_list = []
reference_doi = []
inchi_list = []
mol_wts = []
ref_keys = []
for i, row in df.iterrows():
    code = row["surfactant code"]
    ref_key = row["ref_key"]
    sm = translations.get(code, "")
    doi = get_doi(ref_key, bib_database)
    reference_doi.append(doi)
    ref_keys.append(ref_key)

    mol = Chem.MolFromSmiles(sm)
    smiles = Chem.MolToSmiles(mol)
    inchi = Chem.MolToInchi(mol)
    mw = Descriptors.MolWt(mol)

    smiles_list.append(smiles)
    inchi_list.append(inchi)
    mol_wts.append(mw)

df["SMILES"] = smiles_list
df["Molecular_Weight"] = mol_wts
df["InChI"] = inchi_list
df["source_doi"] = "10.1021/ci600462d"
df["reference_doi"] = reference_doi
df["ref_keys"] = ref_keys
df["pCMC"] = -df["reported experimental log(CMC)"]
df["CMC"] = 10**-df.pCMC

df = df.rename(columns={"surfactant code": "identifier"})
df = df.drop(
    columns=[
        "ref",
        "predicted log(CMC) eq (Table 5)",
        "predicted log(CMC) eq3",
        "corrected experimental log(CMC)",
        "no.",
        "reported experimental log(CMC)",
    ]
)

df = df[~(df.SMILES == "")]
df.to_csv("processed_data/katritzky2007.csv", index=False)
