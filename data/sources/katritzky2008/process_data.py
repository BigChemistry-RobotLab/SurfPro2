import pandas as pd
from rdkit import Chem
from pathlib import Path
from string import Template
import bibtexparser
from rdkit.Chem import Descriptors

def get_doi(bibtex_key, bibtex_entries):
    for e in bibtex_entries.entries:
        if e["ID"] == bibtex_key:
            doi = e.get("doi")
            if doi:
                return doi


C = "C"
O = "O"
EO = "OCC"
OE = "CCO"
Ph1 = Template("c1cc($chain)ccc1")
Ph2 = Template("c1ccc($chain)cc1")
CF2 = "C(F)(F)"
F = "F"
Am = "C(=O)N"
Cb = "NC(=O)"

translations = {
    "C6EO3": C * 6 + EO * 3 + O,
    "C6EO4": C * 6 + EO * 4 + O,
    "C6EO5": C * 6 + EO * 5 + O,
    "C8EO4": C * 8 + EO * 4 + O,
    "C8EO5": C * 8 + EO * 5 + O,
    "C9EO8": C * 9 + EO * 8 + O,
    "C10EO5": C * 10 + EO * 5 + O,
    "C10EO7": C * 10 + EO * 7 + O,
    "C12EO1": C * 12 + EO * 1 + O,
    "C12EO14": C * 12 + EO * 14 + O,
    "C14EO9": C * 14 + EO * 9 + O,
    "C16EO8": C * 16 + EO * 8 + O,
    "C16EO10": C * 16 + EO * 10 + O,
    "C8PhEO30": Ph1.substitute(chain="C(C)(C)CC(C)(C)(C)") + EO * 30 + O,
    "C8PhEO40": Ph1.substitute(chain="C(C)(C)CC(C)(C)(C)") + EO * 40 + O,
    "C9PhEO2": Ph1.substitute(chain=C * 9) + EO * 2 + O,
    "C9PhEO5": Ph1.substitute(chain=C * 9) + EO * 5 + O,
    "C9PhEO12": Ph1.substitute(chain=C * 9) + EO * 12 + O,
    "H4EO3": 4 * CF2 + C + 3 * OE + C,
    "F4EO3": F + 4 * CF2 + C + 3 * OE + C,
    "H6EO3": 6 * CF2 + C + 3 * OE + C,
    "F6EO3": F + 6 * CF2 + C + 3 * OE + C,
    "C12AmEO3": "CCCCCCCCCCCCC(=O)N(CCOCCOCCO)CCN(CCOCCOCCO)C(=O)CCCCCCCCCCCC",
    "C12AmEO6": "CCCCCCCCCCCCC(=O)N(CCOCCOCCOCCOCCOCCO)CCN(CCOCCOCCOCCOCCOCCO)C(=O)CCCCCCCCCCCC",
    "C12AmEO9": "CCCCCCCCCCCCC(=O)N(CCOCCOCCOCCOCCOCCOCCOCCOCCO)CCN(CCOCCOCCOCCOCCOCCOCCOCCOCCO)C(=O)CCCCCCCCCCCC",
    "F4C3NCOEO2": F + CF2 * 4 + 3 * C + f"({Cb + EO * 2 + O + C}){Cb + EO * 2 + O + C}",
    "F4C3NCOEO3": F + CF2 * 4 + 3 * C + f"({Cb + EO * 3 + O + C}){Cb + EO * 3 + O + C}",
    "F6C3NCOEO2": F + CF2 * 6 + 3 * C + f"({Cb + EO * 2 + O + C}){Cb + EO * 2 + O + C}",
    "F6C3NCOEO3": F + CF2 * 6 + 3 * C + f"({Cb + EO * 3 + O + C}){Cb + EO * 3 + O + C}",
    "F8C3NCOEO2": F + CF2 * 8 + 3 * C + f"({Cb + EO * 2 + O + C}){Cb + EO * 2 + O + C}",
    "F8C3NCOEO3": F + CF2 * 8 + 3 * C + f"({Cb + EO * 3 + O + C}){Cb + EO * 3 + O + C}",
    "Gly4Ol-1": "CCCCCCCCCCCCCCCC=CC(=O)OC(CO)COC(CO)COC(CO)COC(CO)CO",
    "Gly4La-1": "CCCCCCCCCCCC(=O)OCCC(CO)COC(CO)COC(CO)COC(CO)CO",
    "Gly4St-1": "CCCCCCCCCCCCCCCCCC(=O)OCCC(CO)COC(CO)COC(CO)COC(CO)CO",
    "Gly6Ol-1": "CCCCCCCCCCCCCCCC=CC(=O)OC(CO)COC(CO)COC(CO)COC(CO)COC(CO)COC(CO)CO",
    "Gly6La-1": "CCCCCCCCCCCC(=O)OCCC(CO)COC(CO)COC(CO)COC(CO)COC(CO)COC(CO)CO",
    "Gly6St-1": "CCCCCCCCCCCCCCCCCC(=O)OCCC(CO)COC(CO)COC(CO)COC(CO)COC(CO)COC(CO)CO",
    "Gly10Ol-1": "CCCCCCCCCCCCCCCC=CC(=O)OC(CO)COC(CO)COC(CO)COC(CO)COC(CO)COC(CO)COC(CO)COC(CO)COC(CO)COC(CO)CO",
    "Gly10La-1": "CCCCCCCCCCCC(=O)OCCC(CO)COC(CO)COC(CO)COC(CO)COC(CO)COC(CO)COC(CO)COC(CO)COC(CO)COC(CO)CO",
    "Sorb-La-1": "CCCCCCCCCCCC(=O)OC[C@H]([C@@H]1[C@@H]([C@H](CO1)O)O)O",
    "Sorb-Ol-1": r"CCCCCCCC/C=C\CCCCCCCC(=O)OC[C@H]([C@@H]1[C@@H]([C@H](CO1)O)O)O",
    "Sorb-Ol-3": r"CCCCCCCC/C=C\CCCCCCCC(=O)OC[C@H]([C@@H]1[C@@H]([C@H](CO1)O)OC(=O)CCCCCCC/C=C\CCCCCCCC)OC(=O)CCCCCCC/C=C\CCCCCCCC",
    "C8-Lactose": "CCCCCCCC(=O)OC[C@H]1O[C@@H](O[C@H]2[C@H](O)[C@@H](O)[C@H](O)O[C@@H]2CO)[C@H](O)[C@@H](O)[C@H]1O",
    "C8-Lactitol": "CCCCCCCC(=O)OC[C@H]1O[C@@H](O[C@@H]([C@H](O)[C@@H](O)CO)[C@H](O)CO)[C@H](O)[C@@H](O)[C@H]1O",
    "C12-Lactose": "CCCCCCCCCCCC(=O)OC[C@H]1O[C@@H](O[C@H]2[C@H](O)[C@@H](O)[C@H](O)O[C@@H]2CO)[C@H](O)[C@@H](O)[C@H]1O",
    "C12-Lactitol": "CCCCCCCCCCCC(=O)OC[C@H]1O[C@@H](O[C@@H]([C@H](O)[C@@H](O)CO)[C@H](O)CO)[C@H](O)[C@@H](O)[C@H]1O",
    "C16-Lactose": "CCCCCCCCCCCCCCCC(=O)OC[C@H]1O[C@@H](O[C@H]2[C@H](O)[C@@H](O)[C@H](O)O[C@@H]2CO)[C@H](O)[C@@H](O)[C@H]1O",
    "C16-Lactitol": "CCCCCCCCCCCCCCCC(=O)OC[C@H]1O[C@@H](O[C@@H]([C@H](O)[C@@H](O)CO)[C@H](O)CO)[C@H](O)[C@@H](O)[C@H]1O",
    "n-C12-Mpyr": "CCCCCCCCCCCCO[C@@H]1O[C@@H]([C@H]([C@@H]([C@H]1O)O)O[C@H]2O[C@@H]([C@H]([C@@H]([C@H]2O)O)O)CO)CO",
    "C4-OCO-Xyl": "CCCC(OC[C@H]([C@@H]([C@H](CO)O)O)O)=O.CCCC(OC[C@@H]([C@H]([C@@H](CO)O)O)O)=O",
    "C5-OCO-Xyl": "CCCCC(OC[C@H]([C@@H]([C@H](CO)O)O)O)=O.CCCCC(OC[C@@H]([C@H]([C@@H](CO)O)O)O)=O",
    "C6-OCO-Xyl": "CCCCCC(OC[C@H]([C@@H]([C@H](CO)O)O)O)=O.CCCCCC(OC[C@@H]([C@H]([C@@H](CO)O)O)O)=O",
    "C7-OCO-Xyl": "CCCCCCC(OC[C@H]([C@@H]([C@H](CO)O)O)O)=O.CCCCCCC(OC[C@@H]([C@H]([C@@H](CO)O)O)O)=O",
    "C8-OCO-Xyl": "CCCCCCCC(OC[C@H]([C@@H]([C@H](CO)O)O)O)=O.CCCCCCCC(OC[C@@H]([C@H]([C@@H](CO)O)O)O)=O",
    "C9-OCO-Xyl": "CCCCCCCCC(OC[C@H]([C@@H]([C@H](CO)O)O)O)=O.CCCCCCCCC(OC[C@@H]([C@H]([C@@H](CO)O)O)O)=O",
    "C4-O-Xyl": "CCCCOC[C@@H](O)[C@H](O)[C@@H](O)CO.CCCCOC[C@H](O)[C@@H](O)[C@H](O)CO",
    "C5-O-Xyl": "CCCCCOC[C@@H](O)[C@H](O)[C@@H](O)CO.CCCCCOC[C@H](O)[C@@H](O)[C@H](O)CO",
    "C6-O-Xyl": "CCCCCCOC[C@@H](O)[C@H](O)[C@@H](O)CO.CCCCCCOC[C@H](O)[C@@H](O)[C@H](O)CO",
    "C7-O-Xyl": "CCCCCCCOC[C@@H](O)[C@H](O)[C@@H](O)CO.CCCCCCCOC[C@H](O)[C@@H](O)[C@H](O)CO",
    "C8-O-Xyl": "CCCCCCCCOC[C@@H](O)[C@H](O)[C@@H](O)CO.CCCCCCCCOC[C@H](O)[C@@H](O)[C@H](O)CO",
    "C9-O-Xyl": "CCCCCCCCCOC[C@@H](O)[C@H](O)[C@@H](O)CO.CCCCCCCCCOC[C@H](O)[C@@H](O)[C@H](O)CO",
    "C10-O-Xyl": "CCCCCCCCCCOC[C@@H](O)[C@H](O)[C@@H](O)CO.CCCCCCCCCCOC[C@H](O)[C@@H](O)[C@H](O)CO",
    "C11-O-Xyl": "CCCCCCCCCCCOC[C@@H](O)[C@H](O)[C@@H](O)CO.CCCCCCCCCCCOC[C@H](O)[C@@H](O)[C@H](O)CO",
    "C4-S-Xyl": "CCCCSC[C@H]([C@@H]([C@H](CO)O)O)O.CCCCSC[C@@H]([C@H]([C@@H](CO)O)O)O",
    "C5-S-Xyl": "CCCCCSC[C@H]([C@@H]([C@H](CO)O)O)O.CCCCCSC[C@@H]([C@H]([C@@H](CO)O)O)O",
    "C6-S-Xyl": "CCCCCCSC[C@H]([C@@H]([C@H](CO)O)O)O.CCCCCSC[C@@H]([C@H]([C@@H](CO)O)O)O",
    "C8-OCO-Glu": "CCCCCCCCC(=O)OC[C@H]1OC(O)[C@H](O)[C@@H](O)[C@@H]1O",
    "C12-OCO-Glu": "CCCCCCCCCCCCC(=O)OC[C@H]1OC(O)[C@H](O)[C@@H](O)[C@@H]1O",
    "C16-OCO-Glu": "CCCCCCCCCCCCCCCCC(=O)OC[C@H]1OC(O)[C@H](O)[C@@H](O)[C@@H]1O",
    "C18-OCO-Glu": "CCCCCCCCCCCCCCCCCCC(=O)OC[C@H]1OC(O)[C@H](O)[C@@H](O)[C@@H]1O",
    "C12-O-Malt": "C([C@@H]1[C@H]([C@@H]([C@H]([C@H](O1)O)O)O)O[C@@H]2[C@@H]([C@H]([C@@H]([C@H](O2)COC(=O)CCCCCCCCCCC)O)O)O)O",
    "C12H25CONH(C2H4O)4H": "CCCCCCCCCCC(=O)NCCOCCOCCOCCO",
    "C8TGlupyr": "CCCCCCCS[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O",
    "bis(C8GA)": "CCCCCCCCN(CCCNC(=O)[C@H](O)[C@@H](O)[C@H](O)[C@H](O)CO)CCN(CCCCCCCC)CCCNC(=O)[C@H](O)[C@@H](O)[C@H](O)[C@H](O)CO",
    "bis(C12GA)": "CCCCCCCCCCCCN(CCCNC(=O)[C@@H](O)[C@H](O)[C@@H](O)[C@@H](O)CO)CCN(CCCCCCCCCCCC)CCCNC(=O)[C@@H](O)[C@H](O)[C@@H](O)[C@@H](O)CO",
    "bis(C12GH)": "CCCCCCCCCCCCN(CCCNC(=O)[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@@H](O)CO)CCN(CCCCCCCCCCCC)CCCNC(=O)[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@@H](O)CO",
    "bis(C8LA)": "O[C@@H]1[C@@H]([C@H]([C@@H](O[C@@H]1CO)O[C@@]([H])([C@@H]([C@H](C(NCCCN(CCCCCCCC)CCN(CCCCCCCC)CCCNC([C@H](O)[C@@H](O)[C@]([C@@H](CO)O)([H])O[C@H](O[C@@H]2CO)[C@H](O)[C@@H](O)[C@H]2O)=O)=O)O)O)[C@@H](CO)O)O)O",
    "bis(C12LA)": "O[C@@H]1[C@@H]([C@H]([C@@H](O[C@@H]1CO)O[C@@]([H])([C@@H]([C@H](C(NCCCN(CCCCCCCCCCCC)CCN(CCCCCCCCCCCC)CCCNC([C@H](O)[C@@H](O)[C@]([C@@H](CO)O)([H])O[C@H](O[C@@H]2CO)[C@H](O)[C@@H](O)[C@H]2O)=O)=O)O)O)[C@@H](CO)O)O)O",
    "Glupyr-1": "CCCCO[C@H]1O[C@@H]([C@H]([C@@H]([C@H]1O)O)O)COC(CCC(OC[C@H]([C@H]([C@@H]([C@H]2O)O)O)O[C@@H]2OCCCC)=O)=O",
    "Glupyr-2": "CCCCO[C@H]1O[C@@H]([C@H]([C@@H]([C@H]1O)O)O)COC(CCCC(OC[C@H]([C@H]([C@@H]([C@H]2O)O)O)O[C@@H]2OCCCC)=O)=O",
    "Glupyr-3": "CCCCO[C@H]1O[C@@H]([C@H]([C@@H]([C@H]1O)O)O)COC(CCCCCCC(OC[C@H]([C@H]([C@@H]([C@H]2O)O)O)O[C@@H]2OCCCC)=O)=O",
    "Glupyr-4": "CCCCO[C@H]1O[C@@H]([C@H]([C@@H]([C@H]1OC(CCC(O[C@@H]2[C@@H](O)[C@H](O)[C@@H](CO)O[C@@H]2OCCCC)=O)=O)O)O)CO",
    "Glupyr-5": "CCCO[C@H]1O[C@@H]([C@H]([C@@H]([C@H]1OC(CCCCCCC(O[C@@H]2[C@@H](O)[C@H](O)[C@@H](CO)O[C@@H]2OCCCC)=O)=O)O)O)CO",
    "Glupyr-6": "CCCCO[C@H]1O[C@H]([C@H]([C@@H]([C@H]1O)O)O)CO",
    "Glupyr-7": "unknown",
    "C4E1": C * 4 + EO * 1 + O,
    "C4E6": C * 4 + EO * 6 + O,
    "C6E3": C * 6 + EO * 3 + O,
    "C6E6": C * 6 + EO * 6 + O,
    "C9E1": C * 9 + EO * 1 + O,
    "C8E3": C * 8 + EO * 3 + O,
    "C8E6": C * 8 + EO * 6 + O,
    "C8E9": C * 8 + EO * 9 + O,
    "C10E3": C * 10 + EO * 3 + O,
    "C10E4": C * 10 + EO * 4 + O,
    "C10E6": C * 10 + EO * 6 + O,
    "C10E8": C * 10 + EO * 8 + O,
    "C10E9": C * 10 + EO * 9 + O,
    "C11E8": C * 11 + EO * 8 + O,
    "C12E2": C * 12 + EO * 2 + O,
    "C12E3": C * 12 + EO * 3 + O,
    "C12E4": C * 12 + EO * 4 + O,
    "C12E5": C * 12 + EO * 5 + O,
    "C12E6": C * 12 + EO * 6 + O,
    "C12E7": C * 12 + EO * 7 + O,
    "C12E8": C * 12 + EO * 8 + O,
    "C12E9": C * 12 + EO * 9 + O,
    "C12E12": C * 12 + EO * 12 + O,
    "C13E8": C * 13 + EO * 8 + O,
    "C14E6": C * 14 + EO * 6 + O,
    "C14E8": C * 14 + EO * 8 + O,
    "C15E8": C * 15 + EO * 8 + O,
    "C16E6": C * 16 + EO * 6 + O,
    "C16E7": C * 16 + EO * 7 + O,
    "C16E9": C * 16 + EO * 9 + O,
    "C16E12": C * 16 + EO * 12 + O,
    "C8PHE1": "CC(C)(C)CC(C)(C)" + Ph2.substitute(chain=1 * EO + O),
    "C8PHE2": "CC(C)(C)CC(C)(C)" + Ph2.substitute(chain=2 * EO + O),
    "C8PHE3": "CC(C)(C)CC(C)(C)" + Ph2.substitute(chain=3 * EO + O),
    "C8PHE4": "CC(C)(C)CC(C)(C)" + Ph2.substitute(chain=4 * EO + O),
    "C8PHE5": "CC(C)(C)CC(C)(C)" + Ph2.substitute(chain=5 * EO + O),
    "C8PHE6": "CC(C)(C)CC(C)(C)" + Ph2.substitute(chain=6 * EO + O),
    "C8PHE7": "CC(C)(C)CC(C)(C)" + Ph2.substitute(chain=7 * EO + O),
    "C8PHE8": "CC(C)(C)CC(C)(C)" + Ph2.substitute(chain=8 * EO + O),
    "C8PHE9": "CC(C)(C)CC(C)(C)" + Ph2.substitute(chain=9 * EO + O),
    "C8PHE10": "CC(C)(C)CC(C)(C)" + Ph2.substitute(chain=10 * EO + O),
    "IC4E6": "C(C)(C)C" + EO * 6 + O,
    "IC6E6": "C(CC)(CC)C" + EO * 6 + O,
    "IC8E6": "C(CCC)(CCC)C" + EO * 6 + O,
    "IC10E6": "C(CCCC)(CCCC)C" + EO * 6 + O,
    "IC10E9": "C(CCCC)(CCCC)C" + EO * 9 + O,
    "C8GLYCER": C * 8 + "OCC(O)CO",
    "C10DIOL": C * 8 + "C(O)CO",
    "C11DIOL": C * 8 + "C(O)CCO",
    "C12DIOL": C * 10 + "C(O)CO",
    "C15DIOL": C * 12 + "C(O)CCO",
    "C8GLUC": C * 8 + "O[C@H]1[C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)O",
    "C10GLUC": C * 10 + "O[C@H]1[C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)O",
    "C12GLUC": C * 12 + "O[C@H]1[C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)O",
    "C12DELAC": C * 12
    + "NC[C@H](O)[C@@H](O)[C@H](O[C@@H]1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O)[C@H](O)CO",
    "C12MALT": C * 12
    + "O[C@H]1[C@@H]([C@H]([C@@H]([C@H](O1)CO)O[C@@H]2[C@@H]([C@H]([C@@H]([C@H](O2)CO)O)O)O)O)O",
    "C12SUCR": C * 12
    + "(=O)OC[C@@H]1[C@H]([C@@H]([C@H]([C@H](O1)O[C@]2([C@H]([C@@H]([C@H](O2)CO)O)O)CO)O)O)O",
    "C18SUCR": C * 18
    + "(=O)OC[C@@H]1[C@H]([C@@H]([C@H]([C@H](O1)O[C@]2([C@H]([C@@H]([C@H](O2)CO)O)O)CO)O)O)O",
    "C11CONEO": C * 11 + "C(=O)N(CCO)CCO",
    "C9CONE3E": C * 9 + "C(=O)N(CCOCCOCCO)CCOCCOCCO",
    "C9CONE4E": C * 9 + "C(=O)N(CCOCCOCCOCCO)CCOCCOCCOCCO",
    "C11CONE2": C * 11 + "C(=O)N(CCOCCO)CCOCCO",
    "C11CONE3": C * 11 + "C(=O)N(CCOCCOCCO)CCOCCOCCO",
    "C11CONE4": C * 11 + "C(=O)N(CCOCCOCCOCCO)CCOCCOCCOCCO",
    "C12ALAE4": "C[C@H](NCCCCCCCCCCCC)C(=O)OCCOCCOCCOCCO",
    "C12GLYE4": "C(NCCCCCCCCCCCC)C(=O)OCCOCCOCCOCCO",
    "C12SARE4": "C(N(C)CCCCCCCCCCCC)C(=O)OCCOCCOCCOCCO",
    "CF6SE2": "OCCOCCOCCSCC" + CF2 * 6 + F,
    "CF6SE3": "OCCOCCOCCOCCSCC" + CF2 * 6 + F,
    "CF6SE5": "OCCOCCOCCOCCOCCOCCSCC" + CF2 * 6 + F,
    "CF6SE7": "OCCOCCOCCOCCOCCOCCOCCOCCSCC" + CF2 * 6 + F,
    "CF6SESE2": F + CF2 * 6 + "CCSCCOCCSCCOCCO",
    "CF6SE2SE": F + CF2 * 6 + "CCSCCOCCOCCSCCOCCO",
    "CF6SE3SE": F + CF2 * 6 + "CCSCCOCCOCCOCCSCCOCCO",
    "CF6CONE3": "N(CCOCCOCCOC)(CCOCCOCCOC)C(=O)C" + CF2 * 6 + F,
    "CF8CONE3": "N(CCOCCOCCOC)(CCOCCOCCOC)C(=O)C" + CF2 * 8 + F,
    "CF10CONE": "N(CCOC)(CCOC)C(=O)C" + CF2 * 10 + F,
}


# Check for parse errors/canonicalise
canonicalized_translations = {}
for t in translations:
    smiles = translations.get(t)
    if smiles == "unknown":
        continue

    mol = Chem.MolFromSmiles(smiles)
    canon_smiles = Chem.MolToSmiles(mol)
    canonicalized_translations[t] = canon_smiles

    if mol is None:
        print("Invalid SMILES?", t)
        print(smiles)
        print("--------------------")

# Compare to manual transcription
df = pd.read_csv("source_data/katritzky_2008_table_2.csv")
df_ref = pd.read_csv("source_data/reference_key.csv", index_col="ref")
bibtex_string = Path("../../CMC_database.bib").read_text(encoding="latin-1")
bib_database = bibtexparser.loads(bibtex_string)

# update the database with generated smiles
new_smiles_list = []
inchi_list = []
reference_keys = []
reference_doi = []
mol_wts = []

for i, row in df.iterrows():
    code = row.structure_code
    ref = row.original_ref
    ref_key = df_ref.loc[ref][0]
    doi = get_doi(ref_key, bib_database)
    new_smiles = canonicalized_translations.get(code, "")

    mol = Chem.MolFromSmiles(new_smiles)
    smiles = Chem.MolToSmiles(mol)
    inchi = Chem.MolToInchi(mol)
    mw = Descriptors.MolWt(mol)

    new_smiles_list.append(smiles)
    inchi_list.append(inchi)
    reference_doi.append(doi)
    reference_keys.append(ref_key)
    mol_wts.append(mw)

df["SMILES"] = new_smiles_list
df["InChI"] = inchi_list
df["Molecular_Weight"] = mol_wts
df["source_doi"] = "10.1021/ie800954k"
df["reference_doi"] = reference_doi
df["reference_key"] = reference_keys
df["Temp_Celsius"] = 25.0
df = df.rename(columns={"-log(CMC)": "pCMC", "structure_code": "identifier"})

df["CMC"] = 10**-df.pCMC
df = df.drop(columns=["no."])
df = df[~(df.SMILES == "")]

df.to_csv("processed_data/katritzky2008.csv", index=False)
