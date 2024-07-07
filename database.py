import sqlite3

def create_database():
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        date TEXT NOT NULL,
        time TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    ''')

    conn.commit()
    conn.close()

def add_user(name):
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

def get_user_id(name):
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE name = ?", (name,))
    user_id = cursor.fetchone()
    conn.close()
    if user_id:
        return user_id[0]
    else:
        return None

def is_attendance_marked(user_id, date):
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM attendance WHERE user_id = ? AND date = ?", (user_id, date))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def add_attendance(user_id, date, time):
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO attendance (user_id, date, time) VALUES (?, ?, ?)", (user_id, date, time))
    conn.commit()
    conn.close()

def get_attendance_records():
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    cursor.execute("SELECT users.name, attendance.date, attendance.time FROM attendance INNER JOIN users ON attendance.user_id = users.id")
    records = cursor.fetchall()
    conn.close()
    return records

def clear_database():
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM attendance")
    cursor.execute("DELETE FROM users")
    conn.commit()
    conn.close()
