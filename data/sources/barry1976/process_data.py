import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE = "source_data/barry1976_table_II.csv"
PROCESSED_FILE = "processed_data/barry1976.csv"

df = pd.read_csv(SOURCE_FILE)

smiles_list = []
inchi_list = []
mol_wts = []
for i, row in df.iterrows():
    smiles = row.SMILES
    mol = Chem.MolFromSmiles(smiles)
    smiles = Chem.MolToSmiles(mol)
    inchi = Chem.MolToInchi(mol)
    mw = Descriptors.MolWt(mol)

    smiles_list.append(smiles)
    inchi_list.append(inchi)
    mol_wts.append(mw)


df["SMILES"] = smiles_list
df["Molecular_Weight"] = mol_wts
df["InChI"] = inchi_list

df["Area_min"] = df["A/ Α2"] / 100
df["Gamma_max"] = df["Γ * 10^10/ mol/cm2"] / 1000000

df = df.rename(
    columns={
        "Surfactant": "identifier",
        "γcmc/ dyne/cm": "AW_ST_CMC",
        "Temperature/ oC": "Temp_Celsius",
    }
)


df = df.drop(
    columns=[
        "-dγ/dlnc/ dyne/cm",
        "Γ * 10^10/ mol/cm2",
        "A/ Α2",
    ]
)

df = df[df.SMILES != ""]

df.to_csv(PROCESSED_FILE, index=False)
