import toml
import sqlite3
import pandas as pd
from pathlib import Path
import numpy as np

config = toml.loads(Path("config.toml").read_text())

DB_PATH = config["DB_PATH"]

query = Path("queries/extract_ml_subset.sql").read_text()

if not Path(DB_PATH).is_file():
    print(DB_PATH, "does not yet exist. Try building it first.")
    quit()

connection = sqlite3.connect(DB_PATH)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()
cursor.execute(query)

df = pd.DataFrame([dict(s) for s in cursor.fetchall()])

# fill -9999 placeholder temperature with NaN
df = df.replace(-9999, np.nan)

# cast CMC and C20 to pCMC / pC20 (-log10) while preserving ordering
df['CMC'] = -np.log10(df['CMC'])
df['C20'] = -np.log10(df['C20'])
df = df.rename(columns = {
    'CMC': 'pCMC', 'C20': 'pC20',
    'CMC_Temp_Celsius': 'pCMC_Temp_Celsius', 'CMC_doi': 'pCMC_doi',
    'C20_Temp_Celsius': 'pC20_Temp_Celsius', 'C20_doi': 'pC20_doi',
})

# check surfactant types annotations
counts = np.unique(df.surfactant_type, return_counts=True)
type_counts = {typ: int(n) for typ, n in zip(counts[0], counts[1])}
print('surfactant types:', list(type_counts.items()))

# drop 5 anionic-cationic mixtures
df = df[~df['surfactant_type'].isin(['anionic-cationic mixture'])]

print(df.describe())

print(f"Extracted database with {df.shape[0]} rows (unique SMILES).")
print("Number of pCMC entries:", df.loc[~df.pCMC.isna()].shape[0])
print("Number of AW_ST_CMC entries:", df.loc[~df.AW_ST_CMC.isna()].shape[0])
print("Number of Gamma_max entries:", df.loc[~df.Gamma_max.isna()].shape[0])
print("Number of pC20 entries:", df.loc[~df.pC20.isna()].shape[0])

# sort for clarity
df = df.sort_values(by=['surfactant_type', 'pCMC_doi', 'SMILES'])

df.to_csv("target/surfpro2_ml_subset.csv", index=False)
print("The data have been saved to target/surfpro2_ml_subset.csv.")
