import toml
import sqlite3
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

query = """
SELECT
    c.compound_id,
    c.SMILES,
    c.Surfactant_Type,
    m.temperature,
    m.value,
    p.name,
    cit.citation_id
FROM measurements m
JOIN compounds c USING(compound_id)
JOIN property_types p USING(property_type_id)
LEFT JOIN measurement_flags fl ON m.measurement_id = fl.measurement_id
JOIN citations cit USINg(citation_id)
WHERE fl.data_flag_id IS NULL AND p.name == "CMC";
"""

config = toml.loads(Path("config.toml").read_text())

DB_PATH = config["DB_PATH"]

if not Path(DB_PATH).is_file():
    print(DB_PATH, "does not yet exist. Try building it first.")
    quit()

connection = sqlite3.connect(DB_PATH)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()
cursor.execute(query)

df = pd.DataFrame([dict(s) for s in cursor.fetchall()])

fig, ax = plt.subplots(ncols=df.Surfactant_Type.unique().shape[0])
i = 0
ax[i].set_ylabel("CMC/ mM")
for c,group in df.groupby("Surfactant_Type"):
    ax[i].set_title(c)
    for c, group in group.groupby("SMILES"):
        if group.temperature.unique().shape[0] > 1:
            group = group.sort_values("temperature")
            ax[i].plot(group.temperature, group.value*1000, "-o")
    ax[i].set_xlabel("Temperature/ °C")
    i += 1
plt.show()
