import sqlite3

#funkcja wybierajaca z tabeli predictions ostatni bieżący rekord
def select_last(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id_pred FROM predictions ORDER BY id_pred DESC LIMIT 1")
    row = cursor.fetchall()
    print(row[0][0])
    return row[0][0]