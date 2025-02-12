import psycopg2
from app.utils.config import DB_CONFIG
from app.utils.logger import log_info, log_error


# Global database connection instance
_connection = None


def get_db_connection():
    """
    Establishes and returns a connection to the PostgreSQL database.
    """
    global _connection
    if _connection is None:
        try:
            _connection = psycopg2.connect(**DB_CONFIG)
            log_info(f"Database connection established.")
        except Exception as e:
            log_error(f"Failed to connect to database: {e}")
            _connection = None
    return _connection


def close_connection():
    """
    Closes the database connection if it is open.
    """
    global _connection
    if _connection:
        _connection.close()
        log_info(f"Database connection closed.")
        _connection = None

