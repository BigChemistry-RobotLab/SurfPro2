import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

df = pd.read_csv("source_data/Guo2011-with-images.csv")

smiles_list = []
inchi_list = []
mol_wts = []
for i, row in df.iterrows():
    sm = row.SMILES
    if sm == "not digitised":
        smiles_list.append("")
        inchi_list.append("")
        mol_wts.append("")
        continue

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
df["source_doi"] = "10.1016/j.chemosphere.2011.05.031"
df["pCMC"] = df["−logCMC_exp"]
df["CMC"] = 10**-df.pCMC

df = df.rename(
    columns={
        "Ref_CMC": "reference_doi",
        "Surfactant_Type.1": "Surfactant_Type",
        "Surfactant_Type": "Surfactant_Type_partial",
    }
)
df = df.drop(
    columns=[
        "ID",
        "Tail_1",
        "Tail_2",
        "Ion_1",
        "Ion_2",
        "Spacer",
        "−logCMC_exp",
        "−logCMC_calc",
        "Note",
    ]
)

df = df[~(df.SMILES == "")]
df = df.round({"Molecular_Weight": 2})
df.to_csv("processed_data/guo2011.csv", index=False)
