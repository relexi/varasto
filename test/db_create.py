from create_varasto_sql import create_string
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
    except Error as e:
        print(e)
    return conn


conn = create_connection("test\\test14.db")
crsr = conn.cursor()
for query in create_string():
    crsr.execute(query)
