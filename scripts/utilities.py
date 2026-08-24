import subprocess


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


def get_current_git_commit(short: bool = False):
    if short:
        command = ["git", "rev-parse", "--short", "HEAD"]
    else:
        command = ["git", "rev-parse", "HEAD"]

    try:
        return subprocess.check_output(command, text=True).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"
