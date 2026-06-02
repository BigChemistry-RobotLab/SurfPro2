import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

df = pd.read_csv("source_data/infante2004_table_1.csv")

smiles_list = []
inchi_list = []
mol_wts = []
for i, row in df.iterrows():
    sm = row.SMILES

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

df["CMC"] = df["cmc/ mmol.dm^{-3}"] / 1000
df["pCMC"] = -np.log10(df.CMC)

df = df.rename(
    columns={
        "Surfactant": "identifier",
    }
)
df = df.drop(
    columns=[
        "cmc/ mmol.dm^{-3}",
        "\delta G_{mic}^{0} / kJ/mol",
    ]
)

df = df[~(df.SMILES == "")]
df.to_csv("processed_data/infante2004.csv", index=False)
