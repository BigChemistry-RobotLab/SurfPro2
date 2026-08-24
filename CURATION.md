# Curation Details

This document details how curation has been performed for the SurfPro2 database.
Contributors to SurfPro2 should read this document carefully, and follow the checklists in [`MAINTENANCE.md`](./MAINTENANCE.md) to make updates.
Data curation is inherently non-trivial and involves judgement and interpretation.
The details below provide users and curators with transparency and guidance on how the data in SurfPro2 were aggregated.
These rules serve as guidelines rather than strict guarantees.
The presence of a curation rule does not imply that every data point in SurfPro2 strictly adheres to it, particularly for older entries.
Rather, these guidelines are recorded here to aid curation and addition of new data to the database going forward.

Please see the explanation in `README.md` for an overview of the organisation of the repository and installation requirements.
For the organisation of relational database, please see the schema in the repository `schema` directory.

## Adding New Sources

This section provides a general overview of how to add a new source of data to SurfPro2.
Please read the sections following it for more specific guidance on how data should be curated.

### Adding New Data

To add a new source to SurfPro2, first make sure that it is in the BibTeX file (`data/CMC_database.bib`).
Create a new folder for it in `data/sources` named after its BibTex key (e.g. `wilk2001`).
Inside this directory, create sub-directories named `source_data` and `processed_data`.
Also create a file `process_data.py` based on the template given in `archetypes/process_data.py`.
Add any source data required into `source_data`.
The naming conventions adopted are to name the file after its BibTeX key, with a suffix indicating its origin in the source, for example, `source_data/wilk2001_table_1.csv`.
The processed data file is simply named after the BibTeX key (e.g. `processed_data/wilk2001.csv`).
Multiple files can be placed in this directory and can follow an sensible format (usually, comma-separated values).
In addition to copied or transcribed data from the source, the following columns should be added (if possible):

| Column name      | Description                                             |
|------------------|---------------------------------------------------------|
| SMILES           | SMILES string for the surfactant                        |
| source_doi       | DOI string for the source publication                   |
| reference_doi    | DOI string for cited literature                         |
| method           | Experimental method used to determine values            |
| Temp_Celsius     | Temperature of the measurement in degrees Celsius       |

This information may also be included in separate files (in the `source_data` directory) and merged with the rest of the data during processing.

### Processing Data

The file `process_data.py` should contain all of the operations required to standardise column names and units, add in SMILES strings, or any other operations required.
All processed data files should contain data with the following headers and units (headings with a \* are mandatory, although at least one property should be provided!):

| Column name       | Description                                             |
|-------------------|---------------------------------------------------------|
| *SMILES           | SMILES string for the surfactant                        |
| *InChI            | InChI string for the surfactant                         |
| *Molecular_Weight | Molecular weight of the surfactant/ $g/mol$             |
| *source_doi       | DOI string for the source publication                   |
| identifier        | Name given to the surfactant in the source text         |
| method            | Experimental method used to determine values            |
| reference_doi     | DOI string for cited literature                         |
| Temp_Celsius      | Temperature of the measurement in degrees Celsius       |
| AW_ST_CMC         | Air-water surface tension at CMC/ $\text{mN}/m$         |
| Area_min          | Minimum surfactant area/ $\text{nm}^2$                  |
| C20               | Surfactant efficiency/ $M$                              |
| CMC               | Critical micelle concentration (CMC)/ $M$               |
| Gamma_max         | Maximum surface excess concentration/ $\text{mol}/m^2$  |
| Pi_CMC            | Surface pressure at CMC/ $\text{mN}/m$                  |

Addition of extra columns should not break anything, but please bear in mind that the purpose of this step is to prepare standardised data for integration into the database.
Any extraneous columns will simply not be read in this process.
Running `process_data.py` should be all that is required to prepare the data for incorporation into the relational database.
Once the processed data file has been created, it will be read into the database along with the other files when running `scripts/initialise_database.py`.

## Units

All units should be standardised during the processing of source data in each source's `process_data.py` file.
The standardised units currently used for properties in the database are:

- $\text{CMC}$/ $M$
- $C_{20}$/ $M$
- $\Gamma_{\text{max}}$/ $\frac{\text{mol}}{m^2}$
- $\gamma_{\text{CMC}}$/ $\frac{\text{mN}}{m}$
- $\Pi_{\text{CMC}}$/ $\frac{\text{mN}}{m}$
- $\text{Area}_{\text{min}}$/ nm2

## Method Annotations

Methods should be annotated onto entries wherever possible using a separate column named 'method'.
If method information is not indicated in the source, the method annotation should be left empty.
The current terms for methods are:

- tensiometry
- conductometry
- fluorimetry
- calorimetry
- ultrasonic
- interferometry
- dye solubilisation
- 1H NMR

There are sub-classes of each of these types which have not yet been incorporated in to the database.
For instance, pendant drop and the Wilhelmy Plate methods of tensiometry fall under the 'tensiometry' method.
In general, the method annotation should reflect the physical quantity measured to derive the parameter of interest (e.g. force for tensiometry, electrical conductivity for conductometry).

## Undefined stereochemical centres

Many sources provide chemical structures which contain chiral centres, yet which lack any kind of annotation describing their stereochemistry.
There are several different cases where this may occur, for instance, the synthesis of enantiomeric mixtures (whether noted in the text or not) and simply the absence of stereochemical annotations.
We have applied the following rules to transcribing structures:

- if the trivial name of a molecule indicating its stereochemical configuration is given, then stereochemical annotations are added to the structure (e.g. β-D-decyl-glucoside).
- if stereochemical annotations are absent and no other indication is present in the compound name, chiral centres are left unspecified.

### Compounds containing a single, undefined chiral centre

There are many syntheses reported in the database which synthesise compounds containing a single chiral centre in the absence of chiral catalysts or enantiomerically pure starting materials.
In these cases, an enantiomeric mixture is implicit.
These structures have been transcribed without stereochemical annotations.

### Compounds containing more than one undefined chiral centre

Structures which are reported as enantiomeric mixtures, but which have more than one chiral centre (thus implying the potential for stereoisomers) have been transcribed as structural pairs of enantiomers.

This reporting method prevents ambiguity between physically different stereoisomers.

### Enumerating Stereoisomers

```python
from rdkit import Chem
from rdkit.Chem.EnumerateStereoisomers import EnumerateStereoisomers
from rdkit.Chem.EnumerateStereoisomers import StereoEnumerationOptions

def enumerate_stereoisomers(smiles):

    options = StereoEnumerationOptions(
        onlyUnassigned=True,
        unique=True,
        tryEmbedding=False
    )

    mol = Chem.MolFromSmiles(smiles)

    isomers = tuple(EnumerateStereoisomers(mol, options=options))
    smiles_list = sorted(Chem.MolToSmiles(x, isomericSmiles=True) for x in isomers)

    return ".".join(smiles_list)
```

## Γmax and A_min values

For some surfactant classes such as gemini surfactants, it is common to report more than one $\Gamma_max$ and/or $\text{Area}_{min}$ value for different values of $n$ in the equation below:

$$
\Gamma_{\text{max}} = \frac{1}{2.303 n R T} (\frac{\partial \gamma}{\partial log(C)})_{T,P}
$$

where $n$ is an integer constant, $\gamma$ is surface tension, $C$ is the surfactant concentration, $T$ is temperature, $P$ is pressure and $R$ is the ideal gas constant.

The equation for $\text{Area}_{min}$ (in $\text{nm}^2$) is:

$$
\text{Area}_{\text{min}}/ \text{nm}^2 = \frac{10^{18} \text{nm}^2/m^2}{N_A/ \text{mol } \Gamma_{\text{max}}/ \text{mol}/m^2}
$$

where $N_A$ is Avogadro's number.

Where possible, we have reported the values for the equation fitted with $n = 2$ for gemini surfactants.

## Two CMC values

In some cases, two CMC values are reported.
In these cases, the CMC from the first breakpoint is reported.

Critical aggregation concentrations (CACs) are also taken to be CMC values in this database.
In future versions, CMC may be changed to CAC in the database, as CMC can be regarded as a type of CAC (micellisation is a form of aggregation).

## Air-water surface tension at CMC ($\gamma_{\text{CMC}}$)

For pure, conventional surfactants, the air-water surface tension at CMC is the limiting surface tension obtained at 'infinite' surfactant concentration.
However, under non-ideal conditions, such as in the presence of impurities, the surface tension at CMC does not necessarily reflect the surface tension at surfactant concentrations higher than CMC.
In this database, the surface tension *at* the CMC is predominantly reported.
However, in some cases quantities such as $\gamma_{lim}$ (limiting surface tension) are reported, which are also regarded as valid.
Ideally, the quantity $\gamma_{CMC}$ should reflect the lowest surface tension achievable with the surfactant.
However, this may only be verified by inspection of the experimental data.

In cases where two CMC values are obtained, the $\gamma_{CMC}$ values for the first CMC are reported.

## Notes

Each literature source may include a `note.txt` file (`<ref_key>/note.txt`) which is ingested into the database.
Notes should document:

- decisions made during data extraction
- ambiguities or inconsistencies in the source
- assumptions or interpretations applied
- relevant contextual information not captured in structured fields

While free-form, notes should be used whenever curation involves judgement or loss of information from the original source.

## Literature

Although DOIs are used as unique identifiers for literature sources, BibTeX-style keys are used for directory and file naming.
However, the repository also makes use of BibTeX-style literature keys for directory and file naming.
Therefore, when adding a new literature source, care should be taken that the keys for any new sources added do not clash with those already in `CMC_database.bib`, and that the existing keys are not changed by updates.
This situation is not convenient, but the benefit of using BibTeX keys during curation is too great to pass over in favour of DOIs, for example.

The literature sources in SurfPro2 originate from a BibTeX file exported from a collection managed by [Zotero 9](https://www.zotero.org/) using the [Better BibTeX plugin](https://github.com/retorquere/zotero-better-bibtex).

## Data Provenance and Interpretation

Each measurement should reflect a value reported or derived from a specific literature source.

Where applicable, notes should record:

- whether a value was directly reported (e.g. in a table in the source text), digitised from a plot, or calculated
- any assumptions made during extraction
- ambiguities in interpretation (e.g. unclear units, multiple values)

The database does not currently enforce structured provenance fields for these distinctions; therefore, such details should be recorded in the associated notes.

## Experimental Conditions

Where available, experimental conditions such as temperature should be recorded.

- Temperatures can be entered in Kelvin or °C, but must be standardised in processing scripts
- If not reported, the temperature field should be left null rather than inferred.
- If a range is reported, a representative value (e.g. midpoint) may be used, with justification recorded in `note.txt` for each source.

Other conditions such as pH, ionic strength, and solvent composition are not yet systematically captured in the schema, but should be noted where relevant.
Future would could integrate these paramters into the database.

## Chemical Structure Normalisation

Chemical structures are represented using SMILES and InChI identifiers.

- InChI strings are treated as the unique identifiers for compounds.
- SMILES should be canonicalised during processing of the source files.
- Molecular weights should be calculated during processing of the source files if possible.
- salts and mixtures should be reported as closely as possible to those provided in the source (i.e do not remove salts). Only stoichiometric mixtures should be reported (i.e. if the ratio of structures in the SMILES strings reflects the molar ratios)

## Handling Conflicting or Duplicate Data

Multiple values for the same property or measurement may exist across or within sources in the database.

- The database is designed to retain multiple measurements rather than report a single value per substance.
- Differences between values should not be reconciled during ingestion unless there is clear justification.
- Any selection or preference (e.g. choosing one of two reported CMCs) should be documented explicitly in the source's notes file.

## Flagged entries

Entries which are highly likely to be erroneous in the source literature, which cannot otherwise be corrected, can be flagged.
The files in `data/annotations` are the primary source of these annotations.
Each file should contain a set of entries in the following format:

```toml
[[quagliotto2009]]
property = "Gamma_max"
value = 2.43e-10
method = "tensiometry"
temperature = 25.0
identifier = "2b"
flag = "possible unit conversion error"
```

Please try to keep flags standardised as much as possible.
