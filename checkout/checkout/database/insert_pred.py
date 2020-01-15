import sqlite3

#funkcja zapisująca sciezke do zdjecia oraz wartosci predykcji w tabeli predictions
def insert_pred(conn, pred_list, path):
    fruits = [0,0,0,0,0,0,0,0,0,0]
    for i in range(10):
        fruits[i] = round(pred_list[0][i]*100,2)
    cursor = conn.cursor()
    insert_query = "INSERT INTO predictions (photo_name, apple, banana, lemon, orange, pear, carrot, cucumber, pepper, potato, tomato) VALUES(?,?,?,?,?,?,?,?,?,?,?)"
    scores = (path, fruits[0],fruits[1],fruits[2],fruits[3],fruits[4],fruits[5],fruits[6],fruits[7],fruits[8],fruits[9])
    cursor.execute(insert_query, scores)
    conn.commit()


