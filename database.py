import sqlite3
from datetime import datetime
import hashlib

def connect():
    return sqlite3.connect("finance.db")

def create_table():
    conn = connect()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT
    )
    """)
        
    # Transactions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transaction (
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

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return False
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                   (username, hash_password(password)))
    conn.commit()
    conn.close()
    return True

def validate_user(username, password):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    if row and row[0] == hash_password(password):
        return True
    return False

def add_transactions(type, amount, category, note=""):
    conn = connect()
    cursor = conn.cursor()
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO transactions (type, amount, category, note, date) VALUES (?, ?, ?, ?, ?)",
                   (type, amount, category, note, date))
    conn.commit()
    conn.close()

def get_transactions():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions ORDER BY date")
    rows = cursor.fetchall()
    conn.close()
    return rows
