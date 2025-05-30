import sqlite3
from datetime import datetime

def connect():
    return sqlite3.connect("finance.db")

def create_table():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            amount REAL,
            category TEXT,
            note TEXT,
            date TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_transaction(type, amount, category, note=""):
    conn = connect()
    cursor = conn.cursor()
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO transactions (type, amount, category, note, date) VALUES (?, ?, ?, ?, ?)",
                   (type, amount, category, note, date))
    conn.commit()
    conn.close()