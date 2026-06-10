# SurfPro2.0

This is the second major version of the [SurfPro](https://github.com/BigChemistry-RobotLab/SurfPro) database, SurfPro2.0.
This database is provided in the form of:

- a set of source files (found in `data/sources/*/source_data/`),
- a set of accompanying curation scripts (`data/sources/*/process_data.py` in each source directory) which output processed data (`data/sources/*/processed_data/*.csv`),
- a script which builds processed data files into a SQLite database (`scripts/initialise_database.py`).

Each measurement has provenance as far back as we could trace the values in the literature.
The database also incorporates a citation file (`data/CMC_database.bib`), and a manually assembled data citation graph (`data/citation_graph.json`).

The schema for the database are given in `schema`.
Relative paths for the various components in the SurfPro2.0 database are stored in `config.toml`.

## UV environment
We use [UV](https://docs.astral.sh/uv/getting-started/installation) to create a reproducible python environment.
```
git clone https://github.com/BigChemistry-RobotLab/SurfPro2.0.git
cd SurfPro2.0

uv sync
```

## Building the Database

After installing the uv environment, run the following command to build the database:

```
uv run python scripts/initialise_database.py
```

The database can then be browsed using standard SQLite browser software (e.g. [DB Browser for SQLite](https://sqlitebrowser.org/)), python-based SQLite explorers (`datasette` or `harlequin`) or interacted with via Python's `sqlite3`.
Example scripts and queries to extract subsets of the data are give in the `scripts` and `queries` directories, respectively.

```
uv add datasette harlequin
uv run datasette target/surfpro.db
uv run harlequin target/surfpro.db
```

## Updating the Database

The database is updated by modifying or creating files in `data/sources/<ref_key>/source_data`, and creating or updating the file `data/sources/<ref_key>/process_data.py`.
Running the `process_data.py` script in its parent directory should process the source data into a standardised file in the `processed_data` directory.
TODO! provide more precise instructions.

## Contributors to SurfPro2.0

This database has been assembled and curated by:

- Stefan L. Hödl
- Pim F.J. Dankloff
- Alexander A. Korotkevich
- William E. Robinson
