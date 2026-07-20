import toml
import sqlite3
import pandas as pd
from pathlib import Path

config = toml.loads(Path("config.toml").read_text())

DB_PATH = config["DB_PATH"]

if not Path(DB_PATH).is_file():
    print(DB_PATH, "does not yet exist. Try building it first.")
    quit()

query = Path("queries/value_distributions.sql").read_text()

conn = sqlite3.connect(DB_PATH)

df = pd.read_sql(query, conn)
