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

    df["pCMC"] = np.where(
        df["CMC"] > 0,
        -np.log10(df["CMC"]),
        np.nan,
    )

    df["pC20"] = np.where(
        df["C20"] > 0,
        -np.log10(df["C20"]),
        np.nan,
    )

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


def build_ml_subset(db_file):
    if not Path(db_file).is_file():
        raise RuntimeError("Database was not generated.")

    df = extract_ml_subset(
        db_file,
        "queries/extract_ml_subset.sql",
    )

    df = prepare_ml_subset(df)

    return df


def ml_subset_release(db_file, output_file):
    if output_file.exists():
        print(f"Deleting {output_file} for fresh build.")
        output_file.unlink(missing_ok=True)

    df = build_ml_subset(db_file)
    df.to_csv(output_file, index=False)


def main():
    config = toml.loads(Path("config.toml").read_text())
    output_file = Path(config["ML_SUBSET_PATH"])
    db_file = Path(config["DB_PATH"])

    df = build_ml_subset(db_file)

    report_dataset(df)

    df.to_csv(output_file, index=False)

    print(f"Saved to {output_file}")


if __name__ == "__main__":
    main()
