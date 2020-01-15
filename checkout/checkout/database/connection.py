import sqlite3

#funkcja zapewniająca połączenie z bazą danych
def connect_database():
    try:
        connection=sqlite3.connect("checkout.db", check_same_thread=False)
    except Exception as e:
        print(e)
    return connection;
