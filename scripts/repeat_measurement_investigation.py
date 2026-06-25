import toml
import sqlite3
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt


def plot_boxplot(df, ax):
    if df.shape[0] < 3:
        return

    data = [-np.log10(x.value) for _, x in df.groupby("SMILES") if x.shape[0] > 2]
    labels = [x for x, z in df.groupby("identifier") if z.shape[0] > 2]

    ax.boxplot(
        data,
        patch_artist=True,
        tick_labels=labels,
    )

    for c, d in enumerate(data):
        ax.annotate(len(d), xy=(c + 1, d.max() * 1.01), fontweight="bold")


config = toml.loads(Path("config.toml").read_text())
DB_PATH = config["DB_PATH"]

query = """
WITH unique_identifiers AS(
    SELECT
        compound_id,
        identifier
    FROM identifiers
    GROUP BY compound_id
)
SELECT
    c.compound_id,
    i.identifier,
    c.SMILES,
    p.name,
    m.value,
    meth.name as method,
    m.temperature
FROM measurements m
LEFT JOIN compounds c ON c.compound_id = m.compound_id
LEFT JOIN citations cit ON m.citation_id = cit.citation_id
LEFT JOIN literature l ON cit.source_id = l.literature_id
LEFT JOIN unique_identifiers i ON i.compound_id = m.compound_id
LEFT JOIN property_types p ON m.property_type_id = p.property_type_id
LEFT JOIN methods meth ON meth.method_id = m.method_id
WHERE
p.name = "CMC"
AND ABS(m.temperature - 25.0) < 1.0
AND cit.cited_id IS NULL
AND m.compound_id IN (
    SELECT compound_id
    FROM measurements
    LEFT JOIN citations cit ON m.citation_id = cit.citation_id
    WHERE cit.cited_id IS NULL
    AND p.name = "CMC"
    AND ABS(m.temperature - 25.0) < 1.0
    GROUP BY compound_id
    HAVING COUNT(*) > :compound_count
);
"""

conn = sqlite3.connect(DB_PATH)
df = pd.read_sql(query, conn, params={"compound_count": 20})
df.sort_values("SMILES").to_csv("temp.csv")

fig, ax = plt.subplots(ncols=3)

plot_boxplot(df, ax[0])

i = 1
for c, group in df.groupby("method"):
    if c == "":
        continue
    plot_boxplot(group, ax[i])
    i += 1
plt.show()
