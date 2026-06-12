import csv
import toml
import bibtexparser
from pathlib import Path
from utilities import biblio_by_doi
from utilities import biblio_by_key
from db_interaction import (
    create_database,
    ingest_file,
    ingest_notes,
    add_surfactant_types
)

config = toml.loads(Path("config.toml").read_text())

DATA_ROOT = config["DATA_ROOT"]
DB_PATH = config["DB_PATH"]
LIT_DATABASE = config["LIT_DATABASE"]
CITATION_GRAPH = config["CITATION_GRAPH"]
SCHEMA_FILE = config["SCHEMA_FILE"]

def initialise_database():
    bibtex_string = Path(LIT_DATABASE).read_text(encoding="utf-8")
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

    Path(DB_PATH).parent.mkdir(exist_ok=True)
    create_database(DB_PATH, SCHEMA_FILE)

    source = Path(f"{DATA_ROOT}/sources")
    for dir in source.iterdir():
        processed_source = dir / "processed_data"

        if dir.name in literature_to_omit:
            continue

        if not processed_source.is_dir():
            continue

        for file in processed_source.iterdir():
            if file.name.startswith("._"):
                continue
            elif file.suffix == ".csv":
                print("Ingesting", file.name)
                ingest_file(file, DB_PATH, bib_by_doi)

        ingest_notes(key, DB_PATH, dir, bib_by_key)

    add_surfactant_types(DB_PATH)

def main():
    initialise_database()


if __name__ == "__main__":
    main()
