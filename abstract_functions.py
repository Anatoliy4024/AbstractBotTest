import sqlite3
import time
from database_logger import log_message, log_query
from constants import DATABASE_PATH

def create_connection(db_file):
    """ create a database connection to the SQLite database specified by the db_file """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        log_message(f"Database connected: {db_file}")
        return conn
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
        log_message(f"Query executed successfully: {query} with params {params}")
    except sqlite3.Error as e:
        log_message(f"Error executing query: {e}")
    finally:
        conn.close()  # Закрытие соединения
        log_message("Database connection closed")

def execute_query_with_retry(query, params=(), max_retries=5):
    """Выполняет SQL-запрос с повторными попытками при блокировке базы данных."""
    retries = 0
    while retries < max_retries:
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()
            log_query(query, params)  # Логирование запроса
            cursor.execute(query, params)
            conn.commit()
            conn.close()
            log_message(f"Query executed successfully with retry: {query} with params {params}")
            break
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e):
                retries += 1
                log_message(f"Database is locked, retrying {retries}/{max_retries}")
                time.sleep(1)  # Задержка перед повторной попыткой
            else:
                log_message(f"Error executing query with retry: {e}")
                raise e
        finally:
            if conn:
                conn.close()
                log_message("Database connection closed after retry")
