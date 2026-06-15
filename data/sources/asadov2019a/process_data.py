import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors


# Compare to manual transcription
df = pd.read_csv("source_data/asadov2019a_table_1.csv")

C14H29 = "CCCCCCCCCCCCCC"
R1 = "H"
R2 = "C"
R3 = "CCO"
R4 = "CC(C)O"

translations = {
    "C14MEA": C14H29 + f"[NH2+]{R3}.[Br-]",
    "C14DEA": C14H29 + f"[NH+]({R3}){R3}.[Br-]",
    "C14TEA": C14H29 + f"[N+]({R3})({R3}){R3}.[Br-]",
    "C14MEtA": C14H29 + f"[NH+]({R2}){R3}.[Br-]",
    "C14MDtA": C14H29 + f"[N+]({R2})({R3}){R3}.[Br-]",
    "C14DEIPA": C14H29 + f"[N+]({R3})({R3}){R4}.[Br-]",
    "C14EDIPA": C14H29 + f"[N+]({R3})({R4}){R4}.[Br-]",
    "C14TIPA": C14H29 + f"[N+]({R4})({R4}){R4}.[Br-]",
}

# update the database with generated smiles
new_smiles_list = []
inchi_list = []
reference_keys = []
reference_doi = []
mol_wts = []

for i, row in df.iterrows():
    new_smiles = translations.get(row.Surfactants)
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
df["CMC"] = df["CMC × 104 mol·dm-3"] / 10000
df["pCMC"] = -np.log10(df.CMC)
df["Gamma_max"] = df["Γmax × 1010 mol·cm-2"] / 10**6
df["Area_min"] = df["Amin × 102 nm2"] / 100
df["Temp_Celsius"] = 25.0
df["C20"] = 10 ** -df["pC20"]

df = df.rename(
    columns={
        "Surfactants": "identifier",
        "T °C": "Temp_Celsius",
        "structure_code": "identifier",
        "πCMC mN·m-1": "Pi_CMC",
        "γCMC mN·m-1": "AW_ST_CMC"
    }
)


df = df.drop(
    columns=[
    "β",
    "CMC × 104 mol·dm-3",
    "Γmax × 1010 mol·cm-2",
    "Amin × 102 nm2",
    "ΔGmic kJ·mol-1",
    "ΔGad kJ·mol-1",
    ]
)
df = df[~(df.SMILES == "")]

df.to_csv("processed_data/asadov2019a.csv", index=False)
