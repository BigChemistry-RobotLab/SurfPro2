"""
Procedures to build the SurfPro2 SQLite database.
"""

import csv
import toml
import bibtexparser
from pathlib import Path
from utilities import biblio_by_doi
from utilities import biblio_by_key
from utilities import get_current_git_commit
from db_interaction import (
    create_database,
    ingest_file,
    ingest_notes,
    ingest_flag_annotations,
    add_surfactant_types,
    update_metadata,
    validate_database,
)


def database_release():
    config = toml.loads(Path("config.toml").read_text())

    db_file = Path(config["DB_PATH"])

    if db_file.exists():
        print(f"Deleting {db_file} for fresh build.")
        db_file.unlink(missing_ok=True)

    initialise_database()
    validate_database(db_file)


def initialise_database():
    config = toml.loads(Path("config.toml").read_text())
    version_info = toml.loads(Path("version.toml").read_text())

    db_file = Path(config["DB_PATH"])
    data_root = config["DATA_ROOT"]
    lit_database = config["LIT_DATABASE"]

    version = version_info["version"]
    date = version_info["release_date"]
    schema_file = config["SCHEMA_FILE"]
    commit = get_current_git_commit(short=True)

    bibtex_string = Path(lit_database).read_text(encoding="utf-8")
    bib_database = bibtexparser.loads(bibtex_string)
    bib_by_doi = biblio_by_doi(bib_database)
    bib_by_key = biblio_by_key(bib_database)

    literature_to_omit = []
    with open("./data/omitted_literature.csv", "r") as file:
        reader = csv.DictReader(file)
        for r in reader:
            entry = bib_by_doi.get(r["DOI"])
            if entry:
                key = entry["ID"]
                literature_to_omit.append(key)

    db_file.parent.mkdir(exist_ok=True)
    create_database(db_file, schema_file)

    source = Path(f"{data_root}/sources")
    for dir in sorted(source.iterdir()):
        processed_source = dir / "processed_data"

        if dir.name in literature_to_omit:
            continue

        if not processed_source.is_dir():
            continue

        for file in sorted(processed_source.iterdir()):
            if file.name.startswith("._"):
                continue
            elif file.suffix == ".csv":
                print("Ingesting", file.name)
                ingest_file(file, db_file, bib_by_doi)

        ingest_notes(dir.name, db_file, dir, bib_by_key)

    add_surfactant_types(db_file)

    ingest_flag_annotations(db_file, Path(data_root))

    update_metadata(db_file, version, date, commit)

    print("Database build complete.")
    print(f"Version: {version}")
    print(f"Git commit: {commit}")
    print(f"Output: {db_file}")


def main():
    initialise_database()


if __name__ == "__main__":
    main()
