import sqlite3

def add_created_at_column():
    conn = sqlite3.connect("finance_tracker.db")
    cursor = conn.cursor()

    # Check if 'created_at' column already exists
    cursor.execute("PRAGMA table_info(transactions)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if "created_at" not in columns:
        cursor.execute("ALTER TABLE transactions ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        print("✅ 'created_at' column added successfully.")
    else:
        print("ℹ️ 'created_at' column already exists.")

    conn.commit()
    conn.close()

add_created_at_column()
