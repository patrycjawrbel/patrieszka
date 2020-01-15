import sqlite3

#funkcja zapisująca etykietę do tabeli Labels
def insert_label(conn, id_label, id_current_pred ):
    cursor = conn.cursor()
    insert_query = "INSERT INTO labels (id_pred, id_class) VALUES(?,?)"
    data = (id_current_pred, id_label)
    cursor.execute(insert_query, data)
    conn.commit()