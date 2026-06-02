import pandas as pd
from rdkit import Chem
import matplotlib.pyplot as plt
from rdkit.Chem import Draw

df = pd.read_csv("source_data/ChemEngSci_2023_265_118208_with_DOI.csv")

for i,row in df.iterrows():
    smiles = row.SMILES
    doi = row.DOI_2
    mol = Chem.MolFromSmiles(smiles)

    if mol is None:
        print(doi)
        print(f"Skipping invalid SMILES {smiles}")
        continue

    img = Draw.MolToImage(mol)


