# SurfPro2.0

This is the second major version of the [SurfPro](https://github.com/BigChemistry-RobotLab/SurfPro) database, SurfPro2.0.
This database is provided in the form of:

- a set of source files (found in `data/sources/<ref_key>/source_data/`),
- a set of accompanying curation scripts (`data/sources/<ref_key>/process_data.py` in each source directory) which output processed data (`data/sources/<ref_key>/processed_data/<ref_key>.csv`),
- a script which builds processed data files into a SQLite database (`scripts/initialise_database.py`).

Each measurement has provenance as far back as we could trace the values in the literature.
The database also incorporates a citation file (`data/CMC_database.bib`), and a manually assembled data citation graph (`data/citation_graph.json`).

The schema for the database are given in `schema`.
Relative paths for the various components in the SurfPro2.0 database are stored in `config.toml`.

## Installing Dependencies

The scripts in this repository run using Python 3.12.11.

```
pip install -r requirements.txt
```

## Building the Database

After installing the dependencies, run the following command to build the database:

```
python scripts/initialise_database.py
```

The database will then be created in the `target` directory (`target/surfpro.db`).
The database can then be browsed using standard SQLite browser software (e.g. [DB Browser for SQLite](https://sqlitebrowser.org/)), or interacted with via Python's `sqlite3`.
Example scripts and queries to extract subsets of the data are give in the `scripts` and `queries` directories, respectively.

## Extracting Database Subsets

The `scripts` directory and the `queries` directory contain examples of how to extract useful subsets of SurfPro2.
For example, an ML-ready subset of SurfPro2 containing each compound entry as a row with property ($\text{CMC}$, $\gamma_{\text{CMC}}$, $C_{20}$ and $\Gamma_{\text{max}}$), citation and temperature data annotated is given in `scripts/extract`

## Updating the Database

The database is updated by modifying or creating files in `data/sources/<ref_key>/source_data`, and creating or updating the file `data/sources/<ref_key>/process_data.py`.
Running the `process_data.py` script in its parent directory should process the source data into a standardised file in the `processed_data` directory.
Please see `curation.md` for guidance on how to curate the database.

## Contributors to SurfPro2.0

This database has been assembled and curated by:

- William E. Robinson
- Stefan L. Hödl
- Pim Dankloff
- Alexander Korotkevich
