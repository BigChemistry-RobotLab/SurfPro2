"""
Extracts a machine learning, multiproperty dataset file from the database.
"""
import toml
import sqlite3
import numpy as np
import pandas as pd
from pathlib import Path

config = toml.loads(Path("config.toml").read_text())

DB_PATH = config["DB_PATH"]

QUERY = Path("queries/extract_ml_subset.sql").read_text()
OUTPUT_FILE_NAME = "surfpro2_ml_subset.csv"

if not Path(DB_PATH).is_file():
    print(DB_PATH, "does not yet exist. Try building it first.")
    quit()

conn = sqlite3.connect(DB_PATH)

df = pd.read_sql(QUERY, conn)

# fill -9999 placeholder temperature with NaN
df = df.replace(-9999, np.nan)

# convert CMC and C20 to pCMC / pC20
df["pCMC"] = -np.log10(df["CMC"])
df["pC20"] = -np.log10(df["C20"])

df = df.drop(columns = ["CMC", "C20"])

df = df.rename(
    columns={
        "CMC_Temp_Celsius": "pCMC_Temp_Celsius",
        "CMC_doi": "pCMC_doi",
        "C20_Temp_Celsius": "pC20_Temp_Celsius",
        "C20_doi": "pC20_doi",
    }
)

# check surfactant types annotations
counts = np.unique(df.surfactant_type, return_counts=True)
type_counts = {typ: int(n) for typ, n in zip(counts[0], counts[1])}
print("Surfactant type counts:", list(type_counts.items()))

print(f"Extracted database with {df.shape[0]} rows (unique SMILES).")
print("Number of pCMC entries:", df.loc[~df.pCMC.isna()].shape[0])
print("Number of AW_ST_CMC entries:", df.loc[~df.AW_ST_CMC.isna()].shape[0])
print("Number of Gamma_max entries:", df.loc[~df.Gamma_max.isna()].shape[0])
print("Number of pC20 entries:", df.loc[~df.pC20.isna()].shape[0])

print(df.describe())

df.to_csv(f"target/{OUTPUT_FILE_NAME}", index=False)
print(f"The data have been saved to target/{OUTPUT_FILE_NAME}.")
