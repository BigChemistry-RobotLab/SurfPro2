# Curation Details

This document details how curation has been performed for the SurfPro2 database.
Data curation is inherently non-trivial and involves judgement and interpretation.
The details below provide users and curators with transparency and guidance on how the data in SurfPro2 were aggregated.
These rules serve as guidelines rather than strict guarantees.
The presence of a curation rule does not imply that every data point in SurfPro2 strictly adheres to it, particularly for older entries.
Rather, these guidelines are recorded here to aid curation and addition of new data to the database going forward.

Please see the explanation in `README.md` for an overview of the organisation of the repository and installation requirements.
For the organisation of relational database, please see the schema in the repository `schema` directory.

## Units

All units should be standardised during the processing of source data in each source's `process_data.py` file.
The standardised units currently used for properties in the database are:

- $\text{CMC}$/ $M$
- pC20: no units
- $\Gamma_{max}$/ $\frac{mol}{m^2}$
- $\gamma_{CMC}$/ $\frac{mN}{m}$
- $\Pi_{CMC}$/ $\frac{mN}{m}$
- $\text{Area}_{min}$/ nm2

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

There are many synthesis reported in the database which synthesis compounds which contain a single chiral centre in the absence of chiral catalysts or enantiomerically pure starting materials.
In these cases, an enantiomeric mixture is implicit.
These structures have been transcribed without stereochemical annotations.

### Compounds containing more than one undefined chiral centre

Structures which are reported as enantiomeric mixtures, but which have more than one chiral centre (thus implying the potential for stereoisomers) have been transcribed as structural pairs enantiomers.
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
\Gamma_{max} = \frac{1}{2.303 n R T} (\frac{\partial \gamma}{\partial log(C)})_{T,P}
$$

where $n$ is an integer constant, $\gamma$ is surface tension, $C$ is the surfactant concentration, $T$ is temperature, $P$ is pressure and $R$ is the ideal gas constant.

The equation for $\text{Area}_{min}$ is:

$$
\text{Area}_{min} = \frac{10^20}{N_A \Gamma_{max}}
$$

where $N_A$ is Avogadro's number.

Where possible, we have reported the values for the equation fitted with $n = 2$ for gemini surfactants.

## Two CMC values

In some cases, two CMC values are reported.
In these cases, the CMC from the first breakpoint is reported.

Critical aggregation concentrations (CACs) are also taken to be CMC values in this database.
In future versions, CMC may be changed to CAC in the database, as CMC can be regarded as a type of CAC (micellisation is a form of aggregation).

## Air-water surface tension at CMC ($\gamma_{CMC}$)

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
However, the repository aslo makes use of BibTeX-style literature keys for directory and file naming.
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
