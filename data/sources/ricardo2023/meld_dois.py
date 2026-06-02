import pandas as pd
from pathlib import Path

df = pd.read_csv("ChemEngSci_2023_265_118208.csv")

file = "ChemEngSci_2023_265_118208_refs.csv"


text = Path(file, encoding="utf-8").read_text(encoding="utf-8").split("\n")

doi_dict = {}
for l in text:
    line = l.split(",")
    if line == "":
        continue
    doi = line[-1].strip(".").replace("https://doi.org/https://doi.org/", "")
    doi = doi.replace("https://doi.org/", "")
    doi_dict[line[0]] = doi


new_doi_col = []
for i, row in df.iterrows():
    ref = row.ref
    new_doi_col.append(doi_dict[ref])

df.DOI_2 = new_doi_col

df.to_csv("ChemEngSci_2023_265_118208_with_DOI.csv", index=False)
