import sqlite3

def select_class(conn, label):
    cursor = conn.cursor()
    cursor.execute("SELECT id_class FROM classes WHERE class_name=?", (label,))
    row = cursor.fetchall()
    print(row)
    return row
