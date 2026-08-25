import toml
import shutil
import subprocess
from pathlib import Path
from initialise_database import database_release
from extract_ml_subset import ml_subset_release


def create_git_archive(ref, output_name):
    subprocess.run(
        [
            "git",
            "archive",
            "--format=zip",
            f"--output={output_name}",
            ref,
        ],
        check=True,
    )


def create_build_archive(version, output_name):
    target_dir = Path("target")

    archive = shutil.make_archive(
        output_name,
        "zip",
        root_dir=target_dir,
    )

    return archive


def check_clean_git_tree():
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True,
    )

    if result.stdout.strip():
        raise RuntimeError("Working tree is not clean. Commit changes first.")


def main():
    version_info = toml.loads(Path("version.toml").read_text())
    config = toml.loads(Path("config.toml").read_text())

    db_file = Path(config["DB_PATH"])
    ml_subset_file = Path(config["ML_SUBSET_PATH"])

    version = version_info["version"]
    release_dir = Path("release")
    release_dir.mkdir(exist_ok=True)

    # Clean up previous releases
    if release_dir.exists():
        shutil.rmtree(release_dir)

    release_dir.mkdir()

    print("Checking repository state...")
    check_clean_git_tree()

    print("Building database...")
    database_release()

    print("Generating statistics...")
    ml_subset_release(db_file, ml_subset_file)

    if not Path("target/surfpro2.db").is_file():
        raise RuntimeError("Database was not generated.")

    if not Path("target/surfpro2_ml_subset.csv").is_file():
        raise RuntimeError("ML subset was not generated.")

    print("Creating repository archive...")
    create_git_archive(
        "HEAD",
        release_dir / f"SurfPro2-{version}-source.zip",
    )
    print("Creating target archive...")
    create_build_archive(
        version,
        release_dir / f"SurfPro2-{version}-build",
    )
    print("Release artefacts generated successfully.")


if __name__ == "__main__":
    main()
