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


df = pd.read_csv("source_data/li2012c_table_1.csv")

C = "C"
R1 = "CC"
R2 = "CCOCC"
R3 = "CCOCCOCC"

translations = {
    "8-EO1-8": f"C[N+](C)({C * 8})CC(O)CO{R1}OCC(C[N+](C)({C * 8})C)O.[Br-].[Br-]",
    "10-EO1-10": f"C[N+](C)({C * 10})CC(O)CO{R1}OCC(C[N+](C)({C * 10})C)O.[Br-].[Br-]",
    "12-EO1-12": f"C[N+](C)({C * 12})CC(O)CO{R1}OCC(C[N+](C)({C * 12})C)O.[Br-].[Br-]",
    "14-EO1-14": f"C[N+](C)({C * 14})CC(O)CO{R1}OCC(C[N+](C)({C * 14})C)O.[Br-].[Br-]",
    "16-EO1-16": f"C[N+](C)({C * 16})CC(O)CO{R1}OCC(C[N+](C)({C * 16})C)O.[Br-].[Br-]",
    "8-EO2-8": f"C[N+](C)({C * 8})CC(O)CO{R2}OCC(C[N+](C)({C * 8})C)O.[Br-].[Br-]",
    "10-EO2-10": f"C[N+](C)({C * 10})CC(O)CO{R2}OCC(C[N+](C)({C * 10})C)O.[Br-].[Br-]",
    "12-EO2-12": f"C[N+](C)({C * 12})CC(O)CO{R2}OCC(C[N+](C)({C * 12})C)O.[Br-].[Br-]",
    "14-EO2-14": f"C[N+](C)({C * 14})CC(O)CO{R2}OCC(C[N+](C)({C * 14})C)O.[Br-].[Br-]",
    "16-EO2-16": f"C[N+](C)({C * 16})CC(O)CO{R2}OCC(C[N+](C)({C * 16})C)O.[Br-].[Br-]",
    "8-EO3-8": f"C[N+](C)({C * 8})CC(O)CO{R3}OCC(C[N+](C)({C * 8})C)O.[Br-].[Br-]",
    "10-EO3-10": f"C[N+](C)({C * 10})CC(O)CO{R3}OCC(C[N+](C)({C * 10})C)O.[Br-].[Br-]",
    "12-EO3-12": f"C[N+](C)({C * 12})CC(O)CO{R3}OCC(C[N+](C)({C * 12})C)O.[Br-].[Br-]",
    "14-EO3-14": f"C[N+](C)({C * 14})CC(O)CO{R3}OCC(C[N+](C)({C * 14})C)O.[Br-].[Br-]",
    "16-EO3-16": f"C[N+](C)({C * 16})CC(O)CO{R3}OCC(C[N+](C)({C * 16})C)O.[Br-].[Br-]",
}

# update the database with generated smiles
new_smiles_list = []
inchi_list = []
mol_wts = []
for i, row in df.iterrows():
    code = row.Surfactant
    new_smiles = translations.get(code)

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

df["Gamma_max"] = df["Γcmc (μmol m−2)"] / 1000000
df["Temp_Celsius"] = 20.0
df["CMC"] = df["CMC (mmol dm−3)"] / 1000
df["pCMC"] = -np.log10(df.CMC)

df = df.rename(
    columns={
        "Surfactant": "identifier",
        "CMC (mol/l)": "CMC",
        "γcmc(mN m−1)": "AW_ST_CMC",
        "Acmc (mol m−2)": "Area_min",
    }
)

df = df.drop(
    columns=[
        "CMC (mmol dm−3)",
        "Γcmc (μmol m−2)",
        "G0ads (kJ mol−1)",
        "G0mic (kJ mol−1)",
        "CMC/pC20",
    ]
)
df = df[~(df.SMILES == "")]

df.to_csv("processed_data/li2012c.csv", index=False)
