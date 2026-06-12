PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS literature (
    literature_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    shorttitle TEXT,
    author TEXT,
    date INTEGER,
    journaltitle TEXT,
    shortjournal TEXT,
    volume INTEGER,
    number INTEGER,
    pages TEXT,
    issn TEXT,
    doi TEXT UNIQUE NOT NULL, -- DOI is unique ID
    url TEXT,
    urldate TEXT,
    abstract TEXT,
    langid TEXT,
    keyid TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS literature_notes (
    note_id INTEGER PRIMARY KEY AUTOINCREMENT,
    literature_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (literature_id) REFERENCES literature(literature_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS citations (
    citation_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    source_id INTEGER NOT NULL, -- source of the value
    cited_id INTEGER, -- cited work in the source
    cited_id_norm INTEGER GENERATED ALWAYS AS (COALESCE(cited_id, -1)) STORED,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (source_id) REFERENCES literature(literature_id) ON DELETE CASCADE,
    FOREIGN KEY (cited_id) REFERENCES literature(literature_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS compounds (
    compound_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    SMILES TEXT NOT NULL,
    Surfactant_Type TEXT,
    IUPAC_name TEXT,
    InChI TEXT UNIQUE NOT NULL, -- InChI is a unique ID
    Molecular_Weight REAL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS identifiers (
    identifier_id INTEGER PRIMARY KEY AUTOINCREMENT,
    identifier TEXT NOT NULL,
    compound_id INTEGER,
    citation_id INTEGER NOT NULL,
    source_file TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (compound_id) REFERENCES compounds(compound_id) ON DELETE CASCADE,
    FOREIGN KEY (citation_id) REFERENCES citations(citation_id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS measurements (
    measurement_id INTEGER PRIMARY KEY AUTOINCREMENT,
    compound_id INTEGER,
    property_type_id INTEGER,
    value REAL,
    temperature REAL,
    temperature_norm INTEGER REAL ALWAYS AS (COALESCE(temperature, -9999)) STORED, -- for unique index
    unit_id INTEGER NOT NULL,
    citation_id INTEGER NOT NULL,
    source_file TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (compound_id) REFERENCES compounds(compound_id) ON DELETE CASCADE,
    FOREIGN KEY (citation_id) REFERENCES citations(citation_id) ON DELETE CASCADE,
    FOREIGN KEY (property_type_id) REFERENCES property_types(property_type_id),
    FOREIGN KEY (unit_id) REFERENCES units(unit_id)
);


CREATE TABLE IF NOT EXISTS property_types (
    property_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS units (
    unit_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    dimension TEXT, -- e.g. concentration, surface_tension
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_notes_literature
ON literature_notes(literature_id);

CREATE UNIQUE INDEX IF NOT EXISTS idx_compounds_inchi ON compounds(InChI);

CREATE UNIQUE INDEX IF NOT EXISTS idx_units_name ON units(name);

CREATE INDEX IF NOT EXISTS idx_measurements_compound ON measurements(compound_id);
CREATE INDEX IF NOT EXISTS idx_measurements_citation ON measurements(citation_id);
CREATE UNIQUE INDEX IF NOT EXISTS idx_measurement_uniqueness ON measurements (compound_id, property_type_id, value, temperature_norm, citation_id);

CREATE INDEX IF NOT EXISTS idx_identifiers_citation ON identifiers(citation_id);
CREATE UNIQUE INDEX IF NOT EXISTS idx_identifier_uniqueness ON identifiers (citation_id, compound_id, identifier);
CREATE INDEX IF NOT EXISTS idx_identifiers_compound ON identifiers(compound_id);

CREATE INDEX IF NOT EXISTS idx_citations_source ON citations(source_id);
CREATE INDEX IF NOT EXISTS idx_citations_cited ON citations(cited_id);
CREATE UNIQUE INDEX IF NOT EXISTS idx_citation_uniqueness ON citations (source_id, cited_id_norm);

CREATE TRIGGER IF NOT EXISTS update_measurements_updated_at
BEFORE UPDATE ON measurements
FOR EACH ROW
BEGIN
    UPDATE measurements
    SET updated_at = CURRENT_TIMESTAMP
    WHERE measurement_id = OLD.measurement_id;
END;

CREATE TRIGGER IF NOT EXISTS update_literature_notes_updated_at
BEFORE UPDATE ON literature_notes
FOR EACH ROW
BEGIN
    UPDATE literature_notes
    SET updated_at = CURRENT_TIMESTAMP
    WHERE note_id = OLD.note_id;
END;
