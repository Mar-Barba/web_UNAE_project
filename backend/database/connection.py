import os
import psycopg2
from psycopg2.extras import RealDictCursor


def get_db_connection():
    """
    Creates and returns a connection to the PostgreSQL database.
    """
    DB_URL = os.getenv("DATABASE_URL")
    try:
        conn = psycopg2.connect(DB_URL, cursor_factory=RealDictCursor)
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None



