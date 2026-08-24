import toml
import sqlite3
from pathlib import Path

count_compounds_query = "SELECT COUNT(compound_id) FROM compounds;"
count_measurements_query = "SELECT COUNT(measurement_id) FROM measurements;"
count_methods_query = "SELECT COUNT(method_id) FROM methods;"
count_literature_query = "SELECT COUNT(literature_id) FROM literature;"
count_properties_query = """
SELECT p.name, COUNT(*) FROM measurements m
JOIN property_types p USING(property_type_id)
GROUP BY p.name;
"""
count_25_degrees_query = """
SELECT COUNT(measurement_id) FROM measurements
WHERE ABS(temperature - 25.0) <= 0.1;
"""

config = toml.loads(Path("config.toml").read_text())

DB_PATH = config["DB_PATH"]

if not Path(DB_PATH).is_file():
    print(DB_PATH, "does not yet exist. Try building it first.")
    quit()

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()
cursor.execute(count_compounds_query)
print("Number of compounds:", cursor.fetchall()[0])
cursor.execute(count_measurements_query)
print("Number of measurements:", cursor.fetchall()[0])
cursor.execute(count_methods_query)
print("Number of methods:", cursor.fetchall()[0])
cursor.execute(count_literature_query)
print("Number of literature sources:", cursor.fetchall()[0])
cursor.execute(count_properties_query)
print("Property numbers:", cursor.fetchall())
cursor.execute(count_25_degrees_query)
print("Number of measurements at 25 (+/- 0.1) °C", cursor.fetchall()[0][0])
