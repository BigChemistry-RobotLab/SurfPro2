import toml
import sqlite3
import numpy as np
import pandas as pd
from pathlib import Path


def sd_report(series):
    sd = series.std()

    sd_r = float(f"{sd:.1g}")
    return sd_r


def mean_sd_report(series):
    mean = series.mean()
    sd = series.std()

    sd_r = float(f"{sd:.1g}")
    decimals = max(0, -int(np.floor(np.log10(abs(sd_r)))))
    mean_r = round(mean, decimals)

    return mean_r


config = toml.loads(Path("config.toml").read_text())
DB_PATH = config["DB_PATH"]

if not Path(DB_PATH).is_file():
    print(DB_PATH, "does not yet exist. Try building it first.")
    quit()

query = Path("queries/extract_repeat_independent_measurements.sql").read_text()

conn = sqlite3.connect(DB_PATH)

df = pd.read_sql(query, conn, params={"compound_count": 20})

# ---------------------------------------------------------------------
# Literature Source Reproducibility Analysis
# ---------------------------------------------------------------------

# Sort measurements by method name and then remove duplicate
# (identifier, keyid) combinations.
df_first = df.sort_values("method").drop_duplicates(
    subset=["identifier", "keyid"], keep="first"
)

# Group rows by compound identifier and retain only compounds
# with more than two independent literature sources.
df_filtered = (
    df_first.groupby("identifier")
    .filter(lambda g: g.shape[0] > 2)
    .sort_values("identifier")
)

# Group measurements by compound structure (SMILES) and calculate
# the mean and standard deviation of the groups.
df_repeat_literature_sources = (
    df_filtered.groupby("SMILES")
    .agg(
        value_mean=("value", mean_sd_report),
        value_std=("value", sd_report),
        n=("keyid", "nunique"),
        citations=("keyid", lambda x: "[@" + ";@".join(map(str, x)) + "]"),
        identifier=("identifier", "first"),
    )
    .reset_index()
)

# ---------------------------------------------------------------------
# Method Reproducibility Analysis
# ---------------------------------------------------------------------

# Group by identifier and literature source and retain only groups containing at least three measurements.
repeated = df.groupby(["identifier", "keyid"]).filter(lambda g: len(g) >= 3)

# Group these repeated measurements by compound structure and calculate
# the mean and standard deviation of the groups.
df_repeat_measurements = (
    repeated.groupby("SMILES")
    .agg(
        value_mean=("value", mean_sd_report),
        value_std=("value", sd_report),
        n=("method", "nunique"),
        citation=("keyid", "first"),
    )
    .reset_index()
)
