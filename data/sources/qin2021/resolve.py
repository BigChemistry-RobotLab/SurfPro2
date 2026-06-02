import json
import numpy as np
import pandas as pd
from pathlib import Path

data122 = pd.read_csv("dataset_122.csv", names=["SMILES", "pCMC"])
data202 = pd.read_csv("dataset_202.csv", names=["SMILES", "pCMC"])
df = pd.concat([data122, data202])
table_s1 = pd.read_csv("qin2021_table_S1.csv")
pcmc_vals = table_s1["Experimental log CMC (uM)"]

mappings = {}
for i,row in df.iterrows():
    closest = np.abs(pcmc_vals - row.pCMC)
    idx = np.where(closest <= 0.01)[0]
    smiles= row.SMILES
    names = table_s1.iloc[idx].Surfactant.to_list()
    for n in names:
        if mappings.get(n):
            mappings[n].add(smiles)
        else:
            mappings[n] = set([smiles])


output = {}
for m in mappings:
    output[m] = list(mappings[m])
json_text = json.dumps(output, indent=4)

Path("name_smiles_mapping_based_on_cmc.json").write_text(json_text)
