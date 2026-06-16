import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors


def get_doi(bibtex_key, bibtex_entries):
    for e in bibtex_entries.entries:
        if e["ID"] == bibtex_key:
            doi = e.get("doi")
            if doi:
                return doi


df = pd.read_csv("source_data/miyazawa2003.csv")

# update the database with generated smiles
new_smiles_list = []
inchi_list = []
mol_wts = []
for i, row in df.iterrows():
    new_smiles = row.SMILES

    if new_smiles == "?":
        new_smiles_list.append("")
        inchi_list.append("")
        mol_wts.append("")
        continue

    mol = Chem.MolFromSmiles(new_smiles)
    smiles = Chem.MolToSmiles(mol)
    inchi = Chem.MolToInchi(mol)
    mw = Descriptors.MolWt(mol)

    new_smiles_list.append(smiles)
    inchi_list.append(inchi)
    mol_wts.append(mw)


df["SMILES"] = new_smiles_list
df["InChI"] = inchi_list
df["Molecular_Weight"] = mol_wts

df["Gamma_max"] = df["Gamma max (umol / m2)"] / 10**6
df["CMC"] = df["CMC (mM)"] / 1000
df["pCMC"] = -np.log10(df.CMC)

df = df.rename(
    columns={
        "ID in paper": "identifier",
        "gamma_CMC (mN/m)": "AW_ST_CMC",
        "A (nm2)": "Area_min",
        "Temperature (Celsius)": "Temp_Celsius",
    }
)


df = df.drop(
    columns=[
        "Kraft temperature (Celsius)",
        "CMC (mM)",
    ]
)
df = df[~(df.SMILES == "")]

df.to_csv("processed_data/miyazawa2003.csv", index=False)
