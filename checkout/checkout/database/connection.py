import sqlite3

def connect_database():
    try:
        connection=sqlite3.connect("checkout.db")
    except Exception as e:
        print(e)
    return connection;
