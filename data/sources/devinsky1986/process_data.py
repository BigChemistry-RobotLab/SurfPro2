import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

SOURCE_FILE = "source_data/devinsky1986_table_1.csv"
PROCESSED_FILE = "processed_data/devinsky1986.csv"

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

df["Gamma_max"] = df["Γmax x 10^6/ mol/m2"] / 1000000

df["Area_min"] = (df["F x 10^20/ m2"] / 10**20) * 10**18

df = df.rename(
    columns={
        "Compound": "identifier",
        "CMC surface tension/ mol/dm3": "CMC",
        "γcmc/ mN/m": "AW_ST_CMC",
    }
)

df["pCMC"] = -np.log10(df.CMC)


df = df.drop(
    columns=[
        "R",
        "X",
        "CMC conductivity/ mol/dm3",
        "-(dγ/dlogc)T",
        "Γmax x 10^6/ mol/m2",
        "-ΔGm surface tension/ kJ/mol",
        "-ΔGm conductivity / kJ/mol",
        "(nCH2)eq",
        "I",
    ]
)

df = df[df.SMILES != ""]

df.to_csv(PROCESSED_FILE, index=False)
