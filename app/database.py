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
                   end TEXT NOT NULL,
                   student_name NOT NULL,
                   student_timezone NOT NULL
                   )
    """)

    conn.commit()
    conn.close()

def get_all_bookings():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT start, end, student_name, student_timezone FROM bookings")
    rows = cursor.fetchall()

    conn.close()

    return [{"start": row[0], "end": row[1]} for row in rows]

def insert_booking(start, end, student_name, student_timezone):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO bookings (start, end, student_name, student_timezone) VALUES (?, ?, ?, ?)", 
        (start, end, student_name, student_timezone)
                   )

    conn.commit()
    conn.close()

def delete_booking(start, end):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM bookings WHERE start = ? AND end = ?", (start, end))

    deleted = cursor.rowcount
    conn.commit()
    conn.close()

    return deleted > 0
