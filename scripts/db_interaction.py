"""
Functions for interaction with the SurfPro2 SQLite database.
"""

import toml
import csv
import sqlite3
from pathlib import Path

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

    title = lit_entry.get("title")
    shorttitle = lit_entry.get("shorttitle")
    author = lit_entry.get("author")
    date = lit_entry.get("date")
    journaltitle = lit_entry.get("journaltitle")
    shortjournal = lit_entry.get("shortjournal")
    volume = lit_entry.get("volume")
    number = lit_entry.get("number")
    pages = lit_entry.get("pages")
    url = lit_entry.get("url")
    urldate = lit_entry.get("urldate")
    abstract = lit_entry.get("abstract")
    langid = lit_entry.get("langid")

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
        keyid=COALESCE(excluded.keyid, literature.keyid)
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


def upsert_literature_note(contents, literature_id, cursor):
    query = """
    INSERT INTO literature_notes (
        literature_id,
        content
    )
    VALUES (?, ?)
    ON CONFLICT(literature_id) DO UPDATE SET
        content = excluded.content
    RETURNING note_id;
    """
    # Execute and return the ID (New or Existing)
    cursor.execute(query, (literature_id, contents))

    return cursor.fetchone()[0]


def upsert_compound(row, cursor):
    smiles = row.get("SMILES")
    surfactant_type = row.get("Surfactant_Type")
    iupac_name = row.get("IUPAC_name")
    inchi = row.get("InChI")
    mol_wt = row.get("Molecular_Weight")

    if inchi is None:
        return

    try:
        mol_wt = round(float(mol_wt), 3) if mol_wt else None
    except ValueError:
        mol_wt = None

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
        Molecular_Weight=COALESCE(excluded.Molecular_Weight, compounds.Molecular_Weight)
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
        source_file=COALESCE(excluded.source_file, identifiers.source_file)
    RETURNING identifier_id;
    """

    citation_id = upsert_citation(source_id, cited_id, cursor)

    cursor.execute(
        query,
        (identifier, citation_id, compound_id, source_file),
    )

    return cursor.fetchone()[0]


def upsert_unit(unit, dimension, latex_unit, cursor):
    query = """
    INSERT INTO units (name, dimension, latex_math_text)
    VALUES (?, ?, ?)
    ON CONFLICT(name) DO UPDATE SET
        name = excluded.name,
        dimension = excluded.dimension,
        latex_math_text = excluded.latex_math_text
    RETURNING unit_id;
    """

    cursor.execute(
        query,
        (unit, dimension, latex_unit),
    )

    return cursor.fetchone()[0]


def upsert_method(method, cursor):
    query = """
    INSERT INTO methods (name)
    VALUES (?)
    ON CONFLICT(name) DO UPDATE SET
        name = excluded.name
    RETURNING method_id;
    """

    if method is not None and method.strip():
        cursor.execute(
            query,
            (method,),
        )

        return cursor.fetchone()[0]


def upsert_citation(source_id, cited_id, cursor):
    query = """
    INSERT INTO citations (source_id, cited_id)
    VALUES (?, ?)
    ON CONFLICT(source_id, cited_id_norm)
    DO UPDATE SET
        source_id = citations.source_id
    RETURNING citation_id;
    """

    cursor.execute(query, (source_id, cited_id))

    return cursor.fetchone()[0]


def upsert_property_type(name, latex_name, cursor):
    query = """
    INSERT INTO property_types (name, latex_math_text)
    VALUES (?, ?)
    ON CONFLICT(name) DO UPDATE SET
        name = excluded.name,
        latex_math_text = excluded.latex_math_text
    RETURNING property_type_id;
    """
    cursor.execute(query, (name, latex_name))

    return cursor.fetchone()[0]


def upsert_measurement(row, compound_id, source_id, cited_id, source_file, cursor):
    query = """
    INSERT INTO measurements (
        compound_id,
        property_type_id,
        value,
        temperature,
        unit_id,
        method_id,
        citation_id,
        source_file
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT (
        compound_id, property_type_id, value, temperature_norm, method_id_norm, citation_id
    )
    DO UPDATE SET
        unit_id = COALESCE(excluded.unit_id, measurements.unit_id),
        source_file = COALESCE(excluded.source_file, measurements.source_file)
    RETURNING measurement_id;
    """
    # (compound_id, property_type, value, temperature, source_id, cited_id)

    for property_type in PROPERTY_INFO:
        unit, dimension, property_name, latex_name, latex_unit = PROPERTY_INFO.get(
            property_type
        )

        method = row.get("method")

        value = row.get(property_type)

        try:
            value = float(value)
        except (TypeError, ValueError):
            continue

        temperature = row.get("Temp_Celsius")

        try:
            temperature = float(temperature) if temperature else None
        except (TypeError, ValueError):
            temperature = None

        if value is None or value == "":
            continue

        method_id = upsert_method(method, cursor)
        unit_id = upsert_unit(unit, dimension, latex_unit, cursor)
        citation_id = upsert_citation(source_id, cited_id, cursor)
        property_type_id = upsert_property_type(property_name, latex_name, cursor)

        cursor.execute(
            query,
            (
                compound_id,
                property_type_id,
                value,
                temperature,
                unit_id,
                method_id,
                citation_id,
                source_file,
            ),
        )

        _ = cursor.fetchone()[0]


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

    if compound_id is None or source_id is None:
        raise ValueError(f"Insertion failed for {source_file}")
    else:
        upsert_identifier(row, compound_id, source_id, cited_id, source_file, cursor)
        upsert_measurement(row, compound_id, source_id, cited_id, source_file, cursor)


def ingest_file(data_file, DB_PATH, bib_by_doi):
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        try:
            cursor.execute("PRAGMA foreign_keys = ON")
            with open(data_file, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    insert_or_update_row(row, data_file.name, cursor, bib_by_doi)
            connection.commit()
        except Exception:
            connection.rollback()
            raise


def add_surfactant_types(DB_PATH):
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
        connection.commit()


def ingest_notes(key, DB_PATH, source_dir, bib_by_key):
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        notes_file = source_dir / "note.txt"

        source_bibtex_entry = bib_by_key.get(key)

        lit_id = upsert_literature(source_bibtex_entry, cursor)

        if notes_file.is_file():
            with open(notes_file, "r", encoding="utf-8") as file:
                upsert_literature_note(file.read(), lit_id, cursor)
        connection.commit()


def upsert_flag(flag_name, description, cursor):
    query = """
    INSERT INTO data_flags (name, description)
    VALUES (?, ?)
    ON CONFLICT(name) DO UPDATE SET
        name = excluded.name,
        description = excluded.description
    RETURNING data_flag_id;
    """

    cursor.execute(
        query,
        (flag_name, description),
    )

    return cursor.fetchone()[0]


def upsert_measurement_flag(measurement_id, flag_id, cursor):
    query = """
    INSERT INTO measurement_flags (measurement_id, data_flag_id)
    VALUES (?, ?)
    ON CONFLICT(measurement_id, data_flag_id) DO UPDATE SET
        measurement_id = excluded.measurement_id,
        data_flag_id = excluded.data_flag_id
    RETURNING measurement_flag_id;
    """

    cursor.execute(
        query,
        (measurement_id, flag_id),
    )

    return cursor.fetchone()[0]


def find_measurement_id(cursor, annot, tol_value=0.01, tol_temp=0.01):
    """
    Find a unique measurement_id matching the annotation.

    Parameters
    ----------
    annot : dict with keys:
        property, value, method, temperature, identifier
    tol_value : float
        tolerance for value comparison
    tol_temp : float
        tolerance for temperature comparison

    Returns
    -------
    measurement_id : int

    Raises
    ------
    ValueError if no match or ambiguous match
    """

    required = ["property", "value", "method", "temperature", "identifier"]
    for key in required:
        if key not in annot:
            raise ValueError(f"Missing required annotation field: {key}")

    try:
        value = float(annot["value"])
    except (TypeError, ValueError):
        raise ValueError(f"Invalid value: {annot['value']}")

    try:
        temperature = (
            float(annot["temperature"])
            if annot["temperature"] not in (None, "")
            else None
        )
    except (TypeError, ValueError):
        temperature = None

    query = """
        SELECT DISTINCT m.measurement_id
        FROM measurements m
        JOIN property_types p USING(property_type_id)
        LEFT JOIN methods meth USING(method_id)
        JOIN identifiers i
            ON m.compound_id = i.compound_id
            AND i.citation_id = m.citation_id
        WHERE
            p.name = ?
            AND ABS(m.value - ?) < ?
            AND (meth.name = ? OR (? IS NULL AND meth.name IS NULL))
            AND (
                (? IS NULL AND m.temperature IS NULL)
                OR ABS(m.temperature - ?) < ?
            )
            AND i.identifier = ?
    """

    params = (
        annot["property"],
        value,
        tol_value,
        annot["method"],
        annot["method"],
        temperature,
        temperature,
        tol_temp,
        annot["identifier"],
    )

    cursor.execute(query, params)
    results = cursor.fetchall()

    if len(results) == 0:
        raise ValueError(f"No measurement found for annotation: {annot}")

    if len(results) > 1:
        raise ValueError(f"Ambiguous measurement match ({len(results)} rows): {annot}")

    return results[0][0]


def ingest_flag_annotations(DB_PATH, DATA_ROOT):
    source_dir = DATA_ROOT / "annotations"
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        for file in source_dir.iterdir():
            if file.suffix != ".toml":
                continue

            annotations = toml.loads(file.read_text())

            for ref in annotations:
                ref_annotations = annotations[ref]
                for annot in ref_annotations:
                    measurement_id = find_measurement_id(
                        cursor, annot, tol_value=2e-12, tol_temp=0.1
                    )

                    # get flag_id
                    flag_id = upsert_flag(annot["flag"], "", cursor)

                    # insert flagged entry
                    _ = upsert_measurement_flag(measurement_id, flag_id, cursor)

        connection.commit()


def update_metadata(DB_PATH, version, release_date, git_commit):
    query = """
    INSERT INTO metadata (
        metadata_id,
        version,
        release_date,
        git_commit
    )
    VALUES (1, ?, ?, ?)
    ON CONFLICT(metadata_id)
    DO UPDATE SET
        version = excluded.version,
        release_date = excluded.release_date,
        git_commit = excluded.git_commit;
    """

    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute(
            query,
            (version, release_date, git_commit),
        )
        connection.commit()


def validate_database(db_path):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        cursor.execute("PRAGMA foreign_key_check")

        errors = cursor.fetchall()

        if errors:
            raise RuntimeError(f"Foreign key violations found: {errors}")
