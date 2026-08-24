"""
Visualise distributions of measurements in SurfPro2.
"""

import toml
import sqlite3
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

config = toml.loads(Path("config.toml").read_text())
DB_PATH = config["DB_PATH"]
conn = sqlite3.connect(DB_PATH)

# first get a list of properties
prop_query = """
SELECT
    property_type_id,
    name AS property,
    latex_math_text
FROM property_types;
"""
df_prop = pd.read_sql(prop_query, conn)

# Iterate over property types and visualise distributions
measurement_query = """
SELECT
    c.compound_id,
    c.SMILES,
    m.value,
    u.latex_math_text as unit_latex
FROM measurements m
LEFT JOIN compounds c ON c.compound_id = m.compound_id
LEFT JOIN units u on u.unit_id = m.unit_id
WHERE m.property_type_id = :prop_id;
"""
log_convert_props = ["C20", "CMC", "Area_min", "Gamma_max"]

fig, ax = plt.subplots(ncols=df_prop.shape[0])
for i, row in df_prop.iterrows():
    df = pd.read_sql(measurement_query, conn, params={"prop_id": row.property_type_id})
    unit = df.unit_latex.iloc[0]
    if row.property in log_convert_props:
        ax_title = (
            "$-\\log_{10}(\\frac{" + row.latex_math_text + "}{" + unit + "})$"
        )
        ax[i].hist(-np.log10(df.value))
    else:
        ax_title = f"${row.latex_math_text}/ {unit}$"
        ax[i].hist(df.value)

    ax[i].set_title(ax_title)

plt.show()
