import sqlite3

def initialize_db():
    conn = sqlite3.connect('sqlite.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        user_name TEXT,
        language TEXT,
        status INTEGER, 
        created_at TIMESTAMP,
        updated_at TIMESTAMP 
        )
 ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        selected_date TIMESTAMP,
        start_time TEXT,
        end_time   TEXT,
        duration   INTEGER,
        people_count INTEGER,
        selected_style TEXT,
        city TEXT,
        preferences TEXT,
        status INTEGER 
        )
    ''')
  # cursor.execute('''
  #   CREATE TABLE IF NOT EXISTS user_sessions (
  #       user_id INTEGER PRIMARY KEY,
  #       username TEXT,
  #       user_name TEXT,
  #       language TEXT,
  #       selected_date TIMESTAMP DEFAULT (now() AT TIME ZONE 'utc'),
  #       start_time TEXT,
  #       end_time TEXT,
  #       duration INTEGER,
  #       people_count INTEGER,
  #       selected_style TEXT,
  #       city TEXT,
  #       preferences TEXT
  #   )
  #   ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    initialize_db()
