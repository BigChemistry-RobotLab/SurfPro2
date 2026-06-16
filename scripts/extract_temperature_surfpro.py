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
assert Path(DB_PATH).is_file()

query = Path("queries/extract_surfpro_temperature.sql").read_text()

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
    'area_min_value': 'Area_min',
    'pi_cmc_value': 'Pi_CMC',
    'surfactant_type': 'type',
    'temperature_bracket': 'temperature',
})
df['pCMC'] = -np.log10(df['CMC'])

# drop mixtures
assert not any(df.type.isna())
df = df[~df['type'].isin(['anionic-cationic mixture'])]

properties = ['pCMC', 'AW_ST_CMC', 'Gamma_max', 'pC20', 'Area_min', 'Pi_CMC']
col_order = ['SMILES', 'type', 'temperature'] + properties
col_order = col_order + [col for col in df.columns if col not in col_order]
df[col_order].to_csv("target/surfprov2_multi.csv", index=False)

i = 0
for smi, group in df.groupby('SMILES'):
    if len(group) > 2:
        i += 1
        print('\n\n', smi)
        for prop in properties:
            if not all(group[prop].isna()):
                clean_series = group[[prop] + ['temperature']].to_string(header=False)
                print(f"{prop}:\n{clean_series}\n")
print('n smil dupl', i)

print(df[properties].describe(), '\n')
print('temp counts', df['temperature'].value_counts(), '\n')
print('unique SMILES', len(pd.unique(df['SMILES'])))
for prop in properties:
    print(prop, df[prop].notna().sum())

assert sum(df.temperature == 0) == 0, f'{sum(df.temperature == 0)}\n{df[df.temperature == 0.]}'
