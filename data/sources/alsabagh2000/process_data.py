import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

# Compare to manual transcription
df = pd.read_csv("source_data/alsabagh2000_table_2.csv")

translations = {
    "P,[i-OPE10] (HC1)": f"CC(C)CCCCCc1ccc({'OCC' * 10}O)cc1",
    "P,[i-OPE10] PO4H2 (HC4)": f"CC(C)CCCCCc1ccc({'OCC' * 10}OP(=O)(O)O)cc1",
    "P,[i-OPE15] (HC2)": f"CC(C)CCCCCc1ccc({'OCC' * 15}O)cc1",
    "P,[i-OPE15] PO4H2 (HC5)": f"CC(C)CCCCCc1ccc({'OCC' * 15}OP(=O)(O)O)cc1",
    "P,[i-OPE20] (HC3)": f"CC(C)CCCCCc1ccc({'OCC' * 20}O)cc1",
    "P,[i-OPE20] PO4H2 (HC6)": f"CC(C)CCCCCc1ccc({'OCC' * 20}OP(=O)(O)O)cc1",
    "PFOAE2 (FC)": "FC(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)C(=O)NCCOCCO",
}

# update the database with generated smiles
new_smiles_list = []
inchi_list = []
reference_keys = []
reference_doi = []
mol_wts = []

for i, row in df.iterrows():
    code = row.Surfactants
    new_smiles = translations.get(code)

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

df = df.rename(
    columns={
        "Surfactants": "identifier",
        "Temp. (°C)": "Temp_Celsius",
        "CMC (mol dm-3)": "CMC",
        "γCMC (mNm−1)": "AW_ST_CMC",
    }
)

df["pCMC"] = -np.log10(df.CMC)

df = df.drop(
    columns=[
        "Ethylene oxide units (n)",
        "HLB",
        "−dg/d log C Pre-CMC units (slope)",
    ]
)
df = df[~(df.SMILES == "")]

df.to_csv("processed_data/alsabagh2000.csv", index=False)
