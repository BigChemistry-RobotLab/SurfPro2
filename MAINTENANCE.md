# Maintenance

SurfPro2 releases are reproducible from the tagged Git repository state corresponding to the release.
The source data, processing scripts, schema definition and release metadata should therefore be regarded as the canonical source of truth for the project.

## Versioning

SurfPro2 follows a semantic versioning scheme (`vMAJOR.MINOR.PATCH`).

**Major versions** entail breaking changes which are not backward-compatible with previous versions of SurfPro2.
Such changes include, but are not limited to:

- updates to the database schema (e.g. overall design, column name changes),
- updates to the database creation scripts.

**Minor versions** are for the addition of data without the introduction of any breaking changes.
The following updates are examples of minor versions:

- addition of a new literature source,
- extraction of additional data from a literature source.

**Patches** are assigned for corrections and minor updates to data or processing scripts.
Examples of patches include:

- fixing errors in source data,
- correcting chemical structures,
- adding annotations/flags to data.

## Release Schedule

SurfPro2 follows a rolling release schedule.
New versions will be released when sufficient additions or corrections have accumulated to warrant a new release.
One to two releases per year are expected, although no release will be issued if substantial changes have not been made since the previous version.

## Contribution Checklists

Please review [`CURATION.md`](./CURATION.md) before making any changes to the database.
Any updates made to SurfPro2 should be under version control.
When writing a git commit for the changes, please adopt the format below.
The first line should be written as a title, as if you are completing the line `A git commit to...`.
Though more details about the commit can be written two lines below the message, doing so is in general not necessary.
Please avoid adding more details beyond the first line of the commit.
The changes made should be plain by diffing the commit, and any decisions made or considerations should be documented in the repository.
Please keep to one update per commit.
For example, if multiple sources of data are updated, place the updates in separate commits, noting which sources were updated in the commit message.

```
short statement indicating changes.

More details about the changes can be written two lines below the message.
```

Please do not alter `config.toml` or `version.toml` as part of routine data updates.
These files are maintained by the Lead Maintainer during releases.

### Addition of New Data (Minor updates)

To add new data to SurfPro2, please follow the steps below:

- [ ] Create a new git branch from the current main branch for your updates,
- [ ] Add the new source publication to `data/bibliography.bib`, including a unique BibTeX key,
- [ ] Create a source directory in `data/sources` named after the publication's BibTeX key,
- [ ] Add new data in `data/sources/<key>/source_data`,
- [ ] Validate chemical structures in the data.
- [ ] Write a processing script for the data (a template is available in `archetypes/process_data.py`),
- [ ] If necessary, add notes or flags in `data/sources/<key>/note.txt` or in `data/annotations`,
- [ ] Run the script to generate the processed data in `data/sources/<key>/processed_data`,
- [ ] Validate that the processed data are correct,
- [ ] Run `scripts/initialise_database.py`,
- [ ] Review the changes in the built database,
- [ ] Create a git commit detailing that the new source was added,
- [ ] Make a pull request in the [project repository](https://github.com/BigChemistry-RobotLab/SurfPro2). Alternatively, contact the lead maintainer about your changes.

Please do not alter `config.toml` or `version.toml` as part of routine data updates.
These files are maintained by the Lead Maintainer during releases.

### Corrections (Patches)

To make a correction to SurfPro2, please follow the steps below:

- [ ] Create a new git branch from the current main branch for your updates,
- [ ] Implement the updates,
- [ ] Re-run any relevant processing scripts,
- [ ] Verify that the updates have been made as intended,
- [ ] Run `scripts/initialise_database.py`,
- [ ] Review the changes in the built database,
- [ ] Create a git commit briefly indicating the changes made (see example below).
- [ ] Make a pull request in the [project repository](https://github.com/BigChemistry-RobotLab/SurfPro2). Alternatively, contact the lead maintainer about your changes.

### Major Updates

Major updates (to schema, scripts, etc.) can be made.
Please create a new git branch first.
Ideally, they are made in isolation, for example without changing any data, so that actions like building the database can be reviewed more easily.
These changes require more care, as changes to one file may affect others.
Major changes should be accompanied with a git commit and pull request.

Please do not alter `config.toml` or `version.toml` when making major updates.

#### Updating Schema

Updates to schema should made in a new file in the `schema/` directory.
The file names should be incremented by one for each update.
Remember to keep the schema file name updated in `config.toml`.

## Release Checklist

This checklist is provided here for the Lead Maintainer to follow.

- [ ] Review changes since the last version,
- [ ] Update version.toml,
- [ ] Update CHANGELOG.md,
- [ ] Commit the changes,
- [ ] Prepare the built files (`python scripts/release.py`)
- [ ] Review the built database
- [ ] Merge/rebase changes into the main branch
- [ ] Create a git tag (`git tag v2.0.0; git push; git push --tags`),
- [ ] Rebuild the release files from the tagged repository state (`python scripts/release.py`)
- [ ] Create a GitHub release (attach built files),
- [ ] Publish the Zenodo release with the database stored in the `target` directory.

The release files generated from the tagged repository state should be always be attached to their corresponding GitHub and Zenodo releases.

### Check Dependencies

Dependencies for the project are given in three files, make sure that they are all consistent:

- `requirements.txt`
- `pyproject.toml`
- `uv.lock`

This situation arose from the need to cater to users with varying package managers.

## Maintenance Team

The database is currently maintained by the authors of SurfPro2.
The lead curator is William E. Robinson (Radboud University Nijmegen), who is responsible for approving releases, changes to schema or data and managing versioning.
