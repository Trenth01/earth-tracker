from contextlib import contextmanager
import psycopg2
from flask_app.constants.postgress_constants import DB_CONFIG

@contextmanager
def db_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    try:
        yield conn, cursor
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def table_exists(cursor, table_name: str) -> bool:
    """
    Checks if the specified table exists in the database.
    :param cursor: Active database cursor.
    :param table_name: Name of the table to check.
    :return: True if the table exists, otherwise False.
    """
    cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_name = %s
        );
    """, (table_name,))
    return cursor.fetchone()[0]
