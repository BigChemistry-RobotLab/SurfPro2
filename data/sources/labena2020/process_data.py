import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

translations = {
    "FHPAD": f"O=C(OC1=CC=C(CCC(NCC[N+](C)({'C' * 8})C)=O)C=C1)/C=C/C(OC2=CC=C(CCC(NCC[N+](C)({'C' * 8})C)=O)C=C2)=O.[Br-].[Br-]",
    "FHPAH": f"O=C(OC1=CC=C(CCC(NCC[N+](C)({'C' * 12})C)=O)C=C1)/C=C/C(OC2=CC=C(CCC(NCC[N+](C)({'C' * 12})C)=O)C=C2)=O.[Br-].[Br-]",
    "FHPAO": f"O=C(OC1=CC=C(CCC(NCC[N+](C)({'C' * 16})C)=O)C=C1)/C=C/C(OC2=CC=C(CCC(NCC[N+](C)({'C' * 16})C)=O)C=C2)=O.[Br-].[Br-]",
}

df = pd.read_csv("source_data/labena2020_table_1.csv")

smiles_list = []
inchi_list = []
mol_wts = []
for i, row in df.iterrows():
    code = row.Compounds
    smiles = translations.get(code)
    mol = Chem.MolFromSmiles(smiles)
    if mol:
        inchi = Chem.MolToInchi(mol)
        canon_smiles = Chem.MolToSmiles(mol)
        mw = Descriptors.MolWt(mol)
        smiles_list.append(canon_smiles)
        inchi_list.append(inchi)
        mol_wts.append(mw)
    else:
        print("!!!!!!")
        smiles_list.append("")
        inchi_list.append("")
        mol_wts.append("")

df["SMILES"] = smiles_list
df["Molecular_Weight"] = mol_wts
df["InChI"] = inchi_list

df["CMC"] = df["CMC (mM)"] / 1000
df["pCMC"] = -np.log10(df["CMC"])

df["Gamma_max"] = df["ΓmaxX10−10 (mol cm−2)"] / 10**6
df["Area_min"] = df["Amin/A2"] / 100

df = df.rename(
    columns={
        "Compounds": "identifier",
        "Temp. C": "Temp_Celsius",
        "πCMC/(mN m−1)": "Pi_CMC",
    }
)
df = df.drop(
    columns=[
        "CMC (mM)",
        "Co X10−6 (mol L−1)",
        "Amin/A2",
    ]
)
df.to_csv("processed_data/labena2020.csv", index=False)
