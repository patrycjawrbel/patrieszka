import sqlite3


def insert_pred(conn, pred_list, path):
    cursor = conn.cursor()
    insert_query = "INSERT INTO predictions (photo_name, apple, banana, lemon, orange, pear, carrot, cucumber, pepper, tomato, tomato) VALUES(?,?,?,?,?,?,?,?,?,?,?)"
    scores = (path, pred_list[0][0],pred_list[0][1],pred_list[0][2],pred_list[0][3],pred_list[0][4],pred_list[0][5],pred_list[0][6],pred_list[0][7],pred_list[0][8],pred_list[0][9])
    cursor.execute(insert_query, scores)
    conn.commit()

    for row in cursor.execute('SELECT * FROM classes'):
        print (row)

