import toml
import csv
import sqlite3
import bibtexparser
from pathlib import Path
from utilities import biblio_by_doi

PROPERTY_INFO = toml.loads(Path("data/property_info.toml").read_text())

def create_database(DB_PATH, schema_file):
    create_commands = Path(schema_file).read_text()
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.executescript(create_commands)
        connection.commit()


def upsert_literature(lit_entry, cursor):
    doi = lit_entry.get("doi")
    isbn = lit_entry.get("isbn")
    issn = lit_entry.get("issn")
    id_key = lit_entry.get("ID")

    title = lit_entry.get("title", "")
    shorttitle = lit_entry.get("shorttitle", "")
    author = lit_entry.get("author", "")
    date = lit_entry.get("date", "")
    journaltitle = lit_entry.get("journaltitle", "")
    shortjournal = lit_entry.get("shortjournal", "")
    volume = lit_entry.get("volume", "")
    number = lit_entry.get("number", "")
    pages = lit_entry.get("pages", "")
    url = lit_entry.get("url", "")
    urldate = lit_entry.get("urldate", "")
    abstract = lit_entry.get("abstract", "")
    langid = lit_entry.get("langid", "")

    if all([x is None for x in [doi, isbn, issn]]):
        return

    if doi is None:
        doi = isbn

    query = """
    INSERT INTO literature (
        title,
        shorttitle,
        author,
        date,
        journaltitle,
        shortjournal,
        volume,
        number,
        pages,
        issn,
        doi,
        url,
        urldate,
        abstract,
        langid,
        keyid
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(doi) DO UPDATE SET
        title=COALESCE(excluded.title, literature.title),
        shorttitle=COALESCE(excluded.shorttitle, literature.shorttitle),
        author=COALESCE(excluded.author, literature.author),
        date=COALESCE(excluded.date, literature.date),
        journaltitle=COALESCE(excluded.journaltitle, literature.journaltitle),
        shortjournal=COALESCE(excluded.shortjournal, literature.shortjournal),
        volume=COALESCE(excluded.volume, literature.volume),
        number=COALESCE(excluded.number, literature.number),
        pages=COALESCE(excluded.pages, literature.pages),
        issn=COALESCE(excluded.issn, literature.issn),
        url=COALESCE(excluded.url, literature.url),
        urldate=COALESCE(excluded.urldate, literature.urldate),
        abstract=COALESCE(excluded.abstract, literature.abstract),
        langid=COALESCE(excluded.langid, literature.langid),
        keyid=COALESCE(excluded.keyid, literature.keyid),
        updated_at=CURRENT_TIMESTAMP
    RETURNING literature_id;
    """

    # Execute and return the ID (New or Existing)
    cursor.execute(
        query,
        (
            title,
            shorttitle,
            author,
            date,
            journaltitle,
            shortjournal,
            volume,
            number,
            pages,
            issn,
            doi,
            url,
            urldate,
            abstract,
            langid,
            id_key,
        ),
    )

    return cursor.fetchone()[0]


def upsert_compound(row, cursor):
    smiles = row.get("SMILES")
    surfactant_type = row.get("Surfactant_Type")
    iupac_name = row.get("IUPAC_name")
    inchi = row.get("InChI")
    mol_wt = row.get("Molecular_Weight")

    if inchi is None:
        return

    query = """
    INSERT INTO compounds (
        SMILES,
        Surfactant_Type,
        IUPAC_name,
        InChI,
        Molecular_Weight
    ) VALUES (?, ?, ?, ?, ?)
    ON CONFLICT(InChI) DO UPDATE SET
        SMILES=COALESCE(excluded.SMILES, compounds.SMILES),
        Surfactant_Type=COALESCE(excluded.Surfactant_Type, compounds.Surfactant_Type),
        IUPAC_name=COALESCE(excluded.IUPAC_name, compounds.IUPAC_name),
        Molecular_Weight=COALESCE(excluded.Molecular_Weight, compounds.Molecular_Weight),
        updated_at=CURRENT_TIMESTAMP
    RETURNING compound_id;
    """

    cursor.execute(
        query,
        (smiles, surfactant_type, iupac_name, inchi, mol_wt),
    )

    return cursor.fetchone()[0]


def upsert_identifier(row, compound_id, source_id, cited_id, source_file, cursor):
    identifier = row.get("identifier")
    if identifier is None:
        return

    query = """
    INSERT INTO identifiers (
        identifier,
        citation_id,
        compound_id,
        source_file
    ) VALUES (?, ?, ?, ?)
    ON CONFLICT(identifier, citation_id, compound_id)
    DO UPDATE SET
        identifier=COALESCE(excluded.identifier, identifiers.identifier),
        citation_id=COALESCE(excluded.citation_id, identifiers.citation_id),
        compound_id=COALESCE(excluded.compound_id, identifiers.compound_id),
        source_file=COALESCE(excluded.source_file, identifiers.source_file),
        updated_at=CURRENT_TIMESTAMP
    RETURNING identifier_id;
    """

    citation_id = upsert_citation(source_id, cited_id, cursor)

    cursor.execute(
        query,
        (identifier, citation_id, compound_id, source_file),
    )

    return cursor.fetchone()[0]


def upsert_unit(unit, dimension, cursor):
    query = """
    INSERT INTO units (name, dimension)
    VALUES (?, ?)
    ON CONFLICT(name) DO UPDATE SET
        updated_at = CURRENT_TIMESTAMP
    RETURNING unit_id;
    """

    cursor.execute(
        query,
        (unit, dimension),
    )

    return cursor.fetchone()[0]


def upsert_citation(source_id, cited_id, cursor):
    query = """
    INSERT INTO citations (source_id, cited_id)
    VALUES (?, ?)
    ON CONFLICT(source_id, cited_id_norm) DO UPDATE SET
        updated_at = CURRENT_TIMESTAMP
    RETURNING citation_id;
    """

    cursor.execute(query, (source_id, cited_id))

    return cursor.fetchone()[0]


def upsert_property_type(name, cursor):
    query = """
    INSERT INTO property_types (name)
    VALUES (?)
    ON CONFLICT(name) DO UPDATE SET
        updated_at = CURRENT_TIMESTAMP
    RETURNING property_type_id;
    """
    cursor.execute(query, (name,))

    return cursor.fetchone()[0]


def upsert_measurement(row, compound_id, source_id, cited_id, source_file, cursor):
    properties = ["CMC", "pC20", "Gamma_max", "AW_ST_CMC", "Pi_CMC", "Area_min"]

    query = """
    INSERT INTO measurements (
        compound_id,
        property_type_id,
        value,
        temperature,
        unit_id,
        citation_id,
        source_file
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT
    DO UPDATE SET
        unit_id = COALESCE(excluded.unit_id, measurements.unit_id),
        source_file = COALESCE(excluded.source_file, measurements.source_file),
        updated_at = CURRENT_TIMESTAMP;
    """
    # (compound_id, property_type, value, temperature, source_id, cited_id)

    for property_type in properties:
        value = row.get(property_type)
        unit, dimension, property_name = PROPERTY_INFO.get(property_type)
        temperature = row.get("Temp_Celsius")

        if value is None or value == "":
            continue

        unit_id = upsert_unit(unit, dimension, cursor)
        citation_id = upsert_citation(source_id, cited_id, cursor)
        property_type_id = upsert_property_type(property_name, cursor)

        cursor.execute(
            query,
            (
                compound_id,
                property_type_id,
                value,
                temperature,
                unit_id,
                citation_id,
                source_file,
            ),
        )


def insert_or_update_row(row, source_file, cursor, bib_database):
    compound_id = upsert_compound(row, cursor)

    ref_doi = row.get("reference_doi")
    source_doi = row.get("source_doi")

    source_bibtex_entry = bib_database.get(source_doi, {"doi": row["source_doi"]})

    source_id = upsert_literature(source_bibtex_entry, cursor)

    if ref_doi is None or ref_doi == "":
        cited_id = None
    else:
        cited_bibtex_entry = bib_database.get(
            ref_doi, {"doi": row.get("reference_doi", "")}
        )
        cited_id = upsert_literature(cited_bibtex_entry, cursor)

    if compound_id and source_id:
        upsert_identifier(row, compound_id, source_id, cited_id, source_file, cursor)
        upsert_measurement(row, compound_id, source_id, cited_id, source_file, cursor)
    else:
        print(f"Issue inserting {source_file}")


def ingest_file(data_file, DB_PATH, bib_by_doi):
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        with open(data_file, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                insert_or_update_row(row, data_file.name, cursor, bib_by_doi)
        connection.commit()


def add_surfactant_types(DB_PATH):
    comp_to_smiles = []
    query = """
    UPDATE compounds
    SET Surfactant_Type = ?
    WHERE SMILES = ?;
    """

    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        with open("data/surfactant_types.csv", "r") as file:
            reader = csv.DictReader(file)
            for r in reader:
                cursor.execute(query, (r["Surfactant_Type_1"], r["SMILES"]))
                comp_to_smiles.append(r)
        connection.commit()


def main():
    config = toml.loads(Path("config.toml").read_text())

    DATA_ROOT = Path(config["DATA_ROOT"])
    DB_PATH = Path(config["DB_PATH"])
    LIT_DATABASE = Path(config["LIT_DATABASE"])
    SCHEMA_FILE = Path(config["SCHEMA_FILE"])

    if not DB_PATH.parent.is_dir():
        DB_PATH.mkdir(exist_ok=True)

    bibtex_string = Path(LIT_DATABASE).read_text(encoding="utf-8")
    bib_database = bibtexparser.loads(bibtex_string)
    bib_by_doi = biblio_by_doi(bib_database)

    create_database(DB_PATH, SCHEMA_FILE)

    ingestion_keys = []
    for key in ingestion_keys:
        source_dir = DATA_ROOT / key / "processed_data"
        for file in source_dir.iterdir():
            ingest_file(file, DB_PATH, bib_by_doi)


if __name__ == "__main__":
    main()
