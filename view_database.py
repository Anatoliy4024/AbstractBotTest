import sqlite3

def view_user_sessions():
    conn = sqlite3.connect('user_sessions.db')
    cursor = conn.cursor()

    cursor.execute("SELECT user_id, username, user_name FROM user_sessions")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    conn.close()

if __name__ == '__main__':
    view_user_sessions()
