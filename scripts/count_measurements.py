import toml
import sqlite3
import pandas as pd
from pathlib import Path

config = toml.loads(Path("config.toml").read_text())

DB_PATH = config["DB_PATH"]

query = """
-- Count number of entries for each property in the database
SELECT p.name, COUNT(*) as "num entries" from measurements m
JOIN compounds c on c.compound_id = m.compound_id
JOIN property_types p ON p.property_type_id = m.property_type_id
GROUP BY p.property_type_id;
"""

if not Path(DB_PATH).is_file():
    print(DB_PATH, "does not yet exist. Try building it first.")
    quit()

connection = sqlite3.connect(DB_PATH)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()
cursor.execute(query)

df = pd.DataFrame([dict(s) for s in cursor.fetchall()])

print(df)

