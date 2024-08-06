# # Ver1
# import sqlite3
# import time
#
# def create_connection(db_file):
#     """Создает соединение с базой данных SQLite."""
#     conn = None
#     try:
#         conn = sqlite3.connect(db_file)
#     except sqlite3.Error as e:
#         print(e)
#     return conn
#
# def execute_query(conn, query, params=()):
#     """Выполняет SQL-запрос."""
#     try:
#         c = conn.cursor()
#         c.execute(query, params)
#         conn.commit()
#     except sqlite3.Error as e:
#         print(e)
#
# def execute_query_with_retry(query, params=(), max_retries=5):
#     """Выполняет SQL-запрос с повторными попытками при блокировке базы данных."""
#     retries = 0
#     while retries < max_retries:
#         try:
#             conn = sqlite3.connect('user_sessions.db')
#             cursor = conn.cursor()
#             cursor.execute(query, params)
#             conn.commit()
#             conn.close()
#             break
#         except sqlite3.OperationalError as e:
#             if "database is locked" in str(e):
#                 retries += 1
#                 time.sleep(1)  # Задержка перед повторной попыткой
#             else:
#                 raise e


## Ver2___________________________________________________________________________________________________
import sqlite3
import time
from database_logger import log_message, log_query  # Добавить импорт логирования

def create_connection(db_file):
    """Создает соединение с базой данных SQLite."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        log_message(f"Connected to database {db_file}")
    except sqlite3.Error as e:
        log_message(f"Error connecting to database: {e}")
    return conn

def execute_query(conn, query, params=()):
    """Выполняет SQL-запрос."""
    try:
        c = conn.cursor()
        log_query(query, params)  # Логирование запроса
        c.execute(query, params)
        conn.commit()
    except sqlite3.Error as e:
        log_message(f"Error executing query: {e}")

def execute_query_with_retry(query, params=(), max_retries=5):
    """Выполняет SQL-запрос с повторными попытками при блокировке базы данных."""
    retries = 0
    while retries < max_retries:
        try:
            conn = sqlite3.connect('user_sessions.db')
            cursor = conn.cursor()
            log_query(query, params)  # Логирование запроса
            cursor.execute(query, params)
            conn.commit()
            conn.close()
            break
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e):
                retries += 1
                log_message(f"Database is locked, retrying {retries}/{max_retries}")
                time.sleep(1)  # Задержка перед повторной попыткой
            else:
                log_message(f"Error executing query with retry: {e}")
                raise e
