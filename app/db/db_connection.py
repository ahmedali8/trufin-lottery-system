import psycopg2
from psycopg2.extras import RealDictCursor
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
            _connection = psycopg2.connect(
                f"dbname={DB_CONFIG['dbname']} user={DB_CONFIG['user']} password={DB_CONFIG['password']} host={DB_CONFIG['host']} port={DB_CONFIG['port']}",
                cursor_factory=RealDictCursor
            )
            log_info(f"[INFO] Database connection established.")
        except Exception as e:
            log_error(f"[ERROR] Failed to connect to database: {e}")
            _connection = None
    return _connection


def close_connection():
    """
    Closes the database connection if it is open.
    """
    global _connection
    if _connection:
        _connection.close()
        log_info(f"[INFO] Database connection closed.")
        _connection = None


def get_cursor():
    """
    Returns a new cursor object for executing queries.
    """
    conn = get_db_connection()
    if conn:
        return conn.cursor()
    return None

