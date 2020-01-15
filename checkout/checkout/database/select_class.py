import sqlite3

#funkcja wybierajaca rekord z tabeli Classes o podanym w argumencie numerze klasy
def select_class(conn, label):
    cursor = conn.cursor()
    cursor.execute("SELECT id_class FROM classes WHERE class_name=?", (label,))
    row = cursor.fetchall()
    print(row[0][0])
    return row[0][0]
