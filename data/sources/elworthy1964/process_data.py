import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE = "source_data/elworthy1964_table_2.csv"
PROCESSED_FILE = "processed_data/elworthy1964.csv"

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

df = df.rename(
    columns={
        "Compound": "identifier",
        "limiting at 20oC/ dynes/cm": "AW_ST_CMC",
        "Amin (nm2)": "Area_min",
        "CMC/ mol/L": "CMC",
        "Temperature/ oC": "Temp_Celsius",
    }
)

df["pCMC"] = -np.log10(df.CMC)


df = df.drop(
    columns=[
        "deltaHm",
        "deltaSm",
        "Ao*/ A2",
    ]
)

df = df[df.SMILES != ""]

df.to_csv(PROCESSED_FILE, index=False)
