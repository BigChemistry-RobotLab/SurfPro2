import toml
import sqlite3
from pathlib import Path

config = toml.loads(Path("config.toml").read_text())
query = Path("./queries/find_measurements_close_to_25_degC.sql").read_text()

DB_PATH = config["DB_PATH"]

if not Path(DB_PATH).is_file():
    print(DB_PATH, "does not yet exist. Try building it first.")
    quit()

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()
cursor.execute(query)

num_measurements = cursor.fetchall()[0][0]

print("Number of measurements at 25 +/- 1.0 °C:", num_measurements)
