import sqlite3


def insert_pred(conn, pred_list, path):
    cursor = conn.cursor()
    insert_query = "INSERT INTO predictions VALUES(?,?,?,?,?,?,?,?,?,?,?)"
    scores = (path, pred_list[0],pred_list[1],pred_list[2],pred_list[3],pred_list[4],pred_list[5],pred_list[6],pred_list[7],pred_list[8],pred_list[9])
    cursor.execute(insert_query, scores)

