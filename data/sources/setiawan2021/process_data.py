import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

df = pd.read_csv("source_data/setiawan2021.csv")

canonical_smiles = []
inchi_list = []
mol_wts = []
for i, row in df.iterrows():
    sm = row.SMILES
    mol = Chem.MolFromSmiles(sm)
    canon_sm = Chem.MolToSmiles(mol)
    inchi = Chem.MolToInchi(mol)
    mw = Descriptors.MolWt(mol)
    canonical_smiles.append(canon_sm)
    inchi_list.append(inchi)
    mol_wts.append(mw)

df.SMILES = canonical_smiles

df = df.drop(columns=["Comp. ID"])
df = df.rename(columns={"pCMC experiment": "pCMC"})

df["InChI"] = inchi_list
df["CMC"] = 10**-df.pCMC
df["Molecular_Weight"] = mol_wts
df["source_doi"] = "10.1063/5.0051623"
df["reference_doi"] = "10.1063/5.0051623"
df.to_csv("processed_data/setiawan2021.csv", index=False)
