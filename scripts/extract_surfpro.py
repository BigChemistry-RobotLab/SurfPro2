import toml
import sqlite3
import pandas as pd
import numpy as np
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

df = df.rename(columns={
    'cmc_value': 'CMC',
    'aw_st_cmc_value': 'AW_ST_CMC',
    'gamma_max_value': 'Gamma_max',
    'pC20_value': 'pC20',
    'Surfactant_Type': 'type',
    'temperature_bracket': 'temperature',
})
df['pCMC'] = -np.log10(df['CMC'])

# drop mixtures
assert not any(df.type.isna())
df = df[~df['type'].isin(['anionic-cationic mixture'])]

col_order = ['SMILES', 'pCMC', 'AW_ST_CMC', 'Gamma_max', 'pC20', 'temperature']
col_order = col_order + [col for col in df.columns if col not in col_order]
df[col_order].to_csv("target/surfprov2_multi.csv", index=False)
