# SurfPro2

SurfPro2 is a curated database of surfactant physicochemical properties and associated molecular structures, assembled from the scientific literature.
This repository contains the source data, curation workflows, and scripts required to reproduce the SurfPro2 SQLite database.
This database contains:

- a set of source files (found in `data/sources/<ref_key>/source_data/`),
- a set of accompanying curation scripts (`data/sources/<ref_key>/process_data.py` in each source directory) which output processed data (`data/sources/<ref_key>/processed_data/<ref_key>.csv`),
- a script which builds processed data files into a SQLite database (`scripts/initialise_database.py`).

Each measurement has provenance as far back as we could trace the values in the literature.
The database also incorporates a citation file (`data/CMC_database.bib`), and a manually assembled data citation graph (`data/citation_graph.json`).

The schema for the database is given in `schema`.
Relative paths for the various components in the SurfPro2 database are stored in `config.toml`.

## Getting started

To build SurfPro2 yourself, please follow the steps below.

### Obtain a copy of the repository

You can either clone the repository (`git clone https://github.com/BigChemistry-RobotLab/SurfPro2.git`) or download it from [GitHub](https://github.com/BigChemistry-RobotLab/SurfPro2.git) or [Zenodo](https://doi.org/10.5281/zenodo.21456552).
Once you have it on your computer, navigate to the SurfPro2 directory in your command line (the directory which contains this file).

### Install Dependencies

The scripts in this repository have been tested with Python 3.12.
The dependencies can be installed by running the command below.
Consider creating a virtual environment first (e.g. using anaconda/miniconda/mamba, UV, or venv, as you prefer).

```
pip install -r requirements.txt
```

### Build the Database

After installing the dependencies, run the following command to build the database:

```
python scripts/initialise_database.py
```

This command runs a script which reads all of the curated data files, and compiles the data in them into the SurfPro2 database.
It should only take a short time to run (<2 minutes).
The resulting database will saved in the `target` directory (`target/surfpro2.db`).
The database can then be browsed using standard SQLite browser software (e.g. [DB Browser for SQLite](https://sqlitebrowser.org/)), or interacted with via Python's `sqlite3`.
Another option for a graphical interface which may be used to browse SurfPro2 is [Datasette](https://datasette.io/) (run `datasette target/surfpro2.db` after Datasette installation).
Example scripts and queries to extract subsets of the data are given in the `scripts` and `queries` directories, respectively.

## Extracting Database Subsets

The `scripts` directory and the `queries` directory contain examples of how to extract useful subsets of SurfPro2 using SQL and Python.
For example, an machine learning ready subset of SurfPro2 containing each compound entry as a row with property ($\text{CMC}$, $\gamma_{\text{CMC}}$, $C_{20}$ and $\Gamma_{\text{max}}$), citation and temperature data annotated is given in `scripts/extract_ml_subset.py` (see also the SQL query given in `queries/extract_ml_subset.sql`).
Running this script will deposit the data subset in the file `target/surfpro2_ml_subset.csv`.

## Updating the Database

The database is updated by modifying or creating files in `data/sources/<ref_key>/source_data`, and creating or updating the file `data/sources/<ref_key>/process_data.py`.
Running the `process_data.py` script in its parent directory should process the source data into a standardised file in the `processed_data` directory.
Please see [`CURATION.md`](./CURATION.md) and [`MAINTENANCE.md`](./MAINTENANCE.md) for guidance on how to curate the database.

## License

SurfPro2 is distributed under the CC BY-NC-SA 4.0 license.
See LICENSE.txt for details.
This is a non-commercial license.
If you would like you use these data for commercial purposes, please contact Dr. William E. Robinson or Prof. Wilhelm T. S. Huck.

## Citation

If you use SurfPro2 in academic work, please cite our preprint on ChemRxiv: [10.26434/chemrxiv.15006392/v1](https://chemrxiv.org/doi/abs/10.26434/chemrxiv.15006392/v1).

## Contributors to SurfPro2

This database has been assembled and curated by:

- William E. Robinson
- Stefan L. Hödl
- Pim F. J. Dankloff
- Alexander A. Korotkevich
