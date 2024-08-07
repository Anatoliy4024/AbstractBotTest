import sqlite3

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

def initialize_database():
    conn = create_connection('user_sessions.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_sessions (
        session_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        language TEXT,
        user_name TEXT,
        event_date TEXT,
        start_time TEXT,
        end_time TEXT,
        number_of_people INTEGER,
        party_style TEXT,
        preferences TEXT,
        city TEXT,
        username TEXT -- добавляем новое поле для username
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_database()
