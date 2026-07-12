import toml
import sqlite3
import pandas as pd
from pathlib import Path

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

print(f"Extracted database with {df.shape[0]} rows.")
print("Number of CMC entries:", df.loc[~df.CMC.isna()].shape[0])
print("Number of AW_ST_CMC entries:", df.loc[~df.AW_ST_CMC.isna()].shape[0])
print("Number of C20 entries:", df.loc[~df.C20.isna()].shape[0])
print("Number of Gamma_max entries:", df.loc[~df.Gamma_max.isna()].shape[0])

df.to_csv("target/surfpro2_ml_subset.csv", index=False)
print("The data have been saved to target/surfpro2_ml_subset.csv.")
