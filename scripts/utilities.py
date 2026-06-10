def biblio_by_doi(bib_database):
    bibliography = {}
    for e in bib_database.entries:
        entry_doi = e.get("doi", "")
        entry_isbn = e.get("isbn")
        if entry_doi:
            bibliography[entry_doi] = e
        elif entry_isbn:
            bibliography[entry_isbn] = e

    return bibliography


def biblio_by_key(bib_database):
    bibliography = {}
    for e in bib_database.entries:
        entry_key = e.get("ID", "")
        if entry_key:
            bibliography[entry_key] = e
    return bibliography
