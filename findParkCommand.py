import sqlite3

db = sqlite3.connect("MosTourist.db")
cur = db.cursor()

def find_park(coordinates):
    sqlvar = coordinates
    cur.execute(f"""SELECT TOP 3 FROM park ORDER BY ABS(longitude - {sqlvar[0]} + latitude - {sqlvar[1]})""")
    result = cur.fetchall()
    return result
