"""
Extracts a machine learning, multiproperty dataset file from the database.
"""

import toml
import sqlite3
import numpy as np
import pandas as pd
from pathlib import Path


def extract_ml_subset(db_path, query_file):
    query = Path(query_file).read_text()

    with sqlite3.connect(db_path) as conn:
        df = pd.read_sql(query, conn)

    return df


def prepare_ml_subset(df):
    df = df.replace(-9999, np.nan)

    df["pCMC"] = -np.log10(df["CMC"])
    df["pC20"] = -np.log10(df["C20"])

    df = df.drop(columns=["CMC", "C20"])

    df = df.rename(
        columns={
            "CMC_Temp_Celsius": "pCMC_Temp_Celsius",
            "CMC_doi": "pCMC_doi",
            "C20_Temp_Celsius": "pC20_Temp_Celsius",
            "C20_doi": "pC20_doi",
        }
    )

    return df


def report_dataset(df):
    counts = np.unique(df.surfactant_type, return_counts=True)
    type_counts = {typ: int(n) for typ, n in zip(counts[0], counts[1])}

    print("Surfactant type counts:")
    print(type_counts)

    print(f"Extracted database with {df.shape[0]} rows.")

    for column in [
        "pCMC",
        "AW_ST_CMC",
        "Gamma_max",
        "pC20",
    ]:
        print(column, df.loc[~df[column].isna()].shape[0])

    print(df.describe())


def ml_subset_release():
    config = toml.loads(Path("config.toml").read_text())

    df = extract_ml_subset(
        config["DB_PATH"],
        "queries/extract_ml_subset.sql",
    )

    df = prepare_ml_subset(df)

    output = Path("target/surfpro2_ml_subset.csv")

    output.parent.mkdir(exist_ok=True)

    df.to_csv(output, index=False)

def main():
    config = toml.loads(Path("config.toml").read_text())

    df = extract_ml_subset(
        config["DB_PATH"],
        "queries/extract_ml_subset.sql",
    )

    df = prepare_ml_subset(df)

    report_dataset(df)

    output = Path("target/surfpro2_ml_subset.csv")

    output.parent.mkdir(exist_ok=True)

    df.to_csv(output, index=False)

    print(f"Saved to {output}")


if __name__ == "__main__":
    main()
