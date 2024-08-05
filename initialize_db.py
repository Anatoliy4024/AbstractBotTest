import sqlite3

def initialize_db():
    conn = sqlite3.connect('user_sessions.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_sessions (
        session_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        language TEXT,
        user_name TEXT,
        event_date TEXT,
        start_time TEXT,
        end_time TEXT,
        number_of_people INTEGER,
        party_style TEXT,
        preferences TEXT,
        city TEXT
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    initialize_db()
