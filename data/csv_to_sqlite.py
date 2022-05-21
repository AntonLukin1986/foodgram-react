import csv
import sqlite3

connect = sqlite3.connect('db.sqlite3')
cursor = connect.cursor()
cursor.execute(
    """CREATE TABLE recipes_ingredient (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    measurement_unit TEXT
)""")

with open('ingredients.csv', 'r', encoding="utf8") as f:
    dr = csv.DictReader(f, delimiter=",")
    to_db = [(i['name'], i['measurement_unit']) for i in dr]

cursor.executemany("INSERT INTO recipes_ingredient (name, measurement_unit) VALUES (?, ?);", to_db)
connect.commit()
connect.close()
