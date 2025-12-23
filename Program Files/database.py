import sqlite3

db_name = "bookings.db"

def get_connection():
    return sqlite3.connect(db_name)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   start TEXT NOT NULL,
                   end TEXT NOT NULL
                   )
    """)

    conn.commit()
    conn.close()
