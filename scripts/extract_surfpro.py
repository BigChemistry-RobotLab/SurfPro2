import toml
import sqlite3
import pandas as pd
from pathlib import Path

config = toml.loads(Path("config.toml").read_text())

DATA_ROOT = config["DATA_ROOT"]
DB_PATH = config["DB_PATH"]
LIT_DATABASE = config["LIT_DATABASE"]
CITATION_GRAPH = config["CITATION_GRAPH"]
SCHEMA_FILE = config["SCHEMA_FILE"]

query = Path("queries/extract_multiple_properties.sql").read_text()

if not Path(DB_PATH).is_file():
    print(DB_PATH, "does not yet exist. Try building it first.")
    quit()

connection = sqlite3.connect(DB_PATH)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()
cursor.execute(query)

df = pd.DataFrame([dict(s) for s in cursor.fetchall()])

df.to_csv("target/new_db.csv", index=False)
