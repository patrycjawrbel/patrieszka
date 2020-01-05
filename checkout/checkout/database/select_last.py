import sqlite3

def select_last(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id_pred FROM predictions ORDER BY id_pred DESC LIMIT 1")
    row = cursor.fetchall()
    print(row)
    return row