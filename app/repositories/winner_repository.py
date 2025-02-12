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
