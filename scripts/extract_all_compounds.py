
import toml
import sqlite3
import pandas as pd
from pathlib import Path

config = toml.loads(Path("config.toml").read_text())

DB_PATH = config["DB_PATH"]

query = Path("queries/extract_all_compounds.sql").read_text()

if not Path(DB_PATH).is_file():
    print(DB_PATH, "does not yet exist. Try building it first.")
    quit()

connection = sqlite3.connect(DB_PATH)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()
cursor.execute(query)

df = pd.DataFrame([dict(s) for s in cursor.fetchall()])

print(f"Extracted database with {df.shape[0]} rows.")
df.to_csv("target/SurfPro2_compounds.csv", index=False)
print("The data have been saved to target/SurfPro2_compounds.csv")
