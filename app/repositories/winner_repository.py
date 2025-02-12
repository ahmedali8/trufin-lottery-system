from app.db.db_connection import get_connection
from datetime import datetime
from app.utils.config import TABLE_PREFIX
from app.utils.logger import get_logger

# Initialize logger
logger = get_logger(__name__)

def get_new_version():
    """
    Retrieves the next version number for a new table.
    """
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name LIKE %s", (TABLE_PREFIX + '%',))
        version = cursor.fetchone()[0] + 1
    logger.info(f"Generated new version: {version}")
    return version

def create_versioned_table(version: int):
    """
    Creates a new versioned winners table.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    table_name = f"{TABLE_PREFIX}{timestamp}_v{version}"
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id SERIAL PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                state TEXT UNIQUE NOT NULL
            )
        """)
        conn.commit()
    logger.info(f"Created new table: {table_name}")
    return table_name

def insert_winner(email: str, state: str, table_name: str):
    """
    Inserts a new winner or updates an existing entry for a given state.
    """
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute(f"SELECT email FROM {table_name} WHERE state = %s", (state,))
        existing_winner = cursor.fetchone()

        if existing_winner:
            cursor.execute(f"UPDATE {table_name} SET email = %s WHERE state = %s", (email, state))
            logger.info(f"Updated winner in {table_name}: {email} for state {state}")
        else:
            cursor.execute(f"INSERT INTO {table_name} (email, state) VALUES (%s, %s)", (email, state))
            logger.info(f"Inserted new winner in {table_name}: {email} for state {state}")
        conn.commit()

def get_winners(table_name: str):
    """
    Retrieves all winners from a given table.
    """
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute(f"SELECT * FROM {table_name}")
        winners = cursor.fetchall()
    logger.info(f"Fetched {len(winners)} winners from {table_name}")
    return winners

def get_winner_count(table_name: str) -> int:
    """
    Returns the count of winners in a given table.
    """
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
    logger.info(f"Total winners in {table_name}: {count}")
    return count
