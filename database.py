import sqlite3
import hashlib
from datetime import datetime
import os

DATABASE_NAME = "finance_tracker.db"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_table():
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                type TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                note TEXT,
                date TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (username) REFERENCES users (username)
            )
        ''')
        
        conn.commit()
        conn.close()
        print("Database tables created successfully!")
        return True
        
    except Exception as e:
        print(f"Error creating database tables: {e}")
        return False

def register_user(username, password):
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        
        # Check if username already exists
        cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            conn.close()
            return False
        
        hashed_password = hash_password(password)
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed_password)
        )
        
        conn.commit()
        conn.close()
        print(f"User {username} registered successfully!")
        return True
        
    except Exception as e:
        print(f"Error registering user: {e}")
        return False

def validate_user(username, password):
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        
        hashed_password = hash_password(password)
        cursor.execute(
            "SELECT username FROM users WHERE username = ? AND password = ?",
            (username, hashed_password)
        )
        
        result = cursor.fetchone()
        conn.close()
        
        return result is not None
        
    except Exception as e:
        print(f"Error validating user: {e}")
        return False

def add_transactions(username, transaction_type, amount, category, note, date):
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO transactions (username, type, amount, category, note, date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (username, transaction_type, amount, category, note, date))
        
        conn.commit()
        conn.close()
        print(f"Transaction added: {transaction_type} of {amount} for {category}")
        return True
        
    except Exception as e:
        print(f"Error adding transaction: {e}")
        return False

def get_transactions(username):
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, type, amount, category, note, date
            FROM transactions 
            WHERE username = ?
            ORDER BY date DESC
        ''', (username,))
        
        transactions = cursor.fetchall()
        conn.close()
        
        return transactions
        
    except Exception as e:
        print(f"Error getting transactions: {e}")
        return []

def delete_transaction(transaction_id, username):
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        
        cursor.execute(
            "DELETE FROM transactions WHERE id = ? AND username = ?",
            (transaction_id, username)
        )
        
        conn.commit()
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error deleting transaction: {e}")
        return False

def get_user_stats(username):
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        
        # Get total income
        cursor.execute(
            "SELECT SUM(amount) FROM transactions WHERE username = ? AND type = 'Income'",
            (username,)
        )
        total_income = cursor.fetchone()[0] or 0
        
        # Get total expense
        cursor.execute(
            "SELECT SUM(amount) FROM transactions WHERE username = ? AND type = 'Expense'",
            (username,)
        )
        total_expense = cursor.fetchone()[0] or 0
        
        cursor.execute(
            "SELECT COUNT(*) FROM transactions WHERE username = ?",
            (username,)
        )
        transaction_count = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return {
            'total_income': total_income,
            'total_expense': total_expense,
            'balance': total_income - total_expense,
            'transaction_count': transaction_count
        }
        
    except Exception as e:
        print(f"Error getting user stats: {e}")
        return {
            'total_income': 0,
            'total_expense': 0,
            'balance': 0,
            'transaction_count': 0
        }

def backup_database(backup_path="backup_finance.db"):
    try:
        if os.path.exists(DATABASE_NAME):
            import shutil
            shutil.copy2(DATABASE_NAME, backup_path)
            print(f"Database backed up to {backup_path}")
            return True
        else:
            print("Database file not found!")
            return False
    except Exception as e:
        print(f"Error backing up database: {e}")
        return False

def get_transaction_by_id(transaction_id):
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, type, amount, category, note, date FROM transactions WHERE id = ?", (transaction_id,))
        result = cursor.fetchone()
        conn.close()
        return result
    except Exception as e:
        print(f"Error fetching transaction by ID: {e}")
        return None


# Update transaction
def update_transaction(transaction_id, t_type, amount, category, note, date):
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE transactions
            SET type = ?, amount = ?, category = ?, note = ?, date = ?
            WHERE id = ?
        ''', (t_type, amount, category, note, date, transaction_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating transaction: {e}")
        return False


# Delete transaction
def delete_transaction(transaction_id):
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error deleting transaction: {e}")
        return False

if __name__ == "__main__":
    print("Initializing database...")
    create_table()
