import sqlite3

def initialize_db():
    conn = sqlite3.connect('user_sessions.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_sessions (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        user_name TEXT,
        language TEXT,
        selected_date TEXT,
        start_time TEXT,
        end_time TEXT,
        duration INTEGER,
        people_count INTEGER,
        selected_style TEXT,
        city TEXT,
        preferences TEXT
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    initialize_db()
