import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def execute_query(conn, query, params=()):
    """ Execute a single query
    :param conn: Connection object
    :param query: a SQL query
    :param params: parameters for the query
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(query, params)
        conn.commit()
    except Error as e:
        print(e)
