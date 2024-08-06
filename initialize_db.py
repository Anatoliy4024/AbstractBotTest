import sqlite3
from database_logger import log_message, execute_query_with_logging

def initialize_db():
    conn = sqlite3.connect('user_sessions.db')
    cursor = conn.cursor()

    create_table_query = '''
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
    '''

    try:
        execute_query_with_logging(conn, create_table_query)
        log_message('Tables created successfully.')
    except sqlite3.Error as e:
        log_message(f'Error creating tables: {e}')
    finally:
        conn.close()

if __name__ == '__main__':
    initialize_db()
