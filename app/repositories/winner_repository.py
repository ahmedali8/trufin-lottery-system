from app.db.db_connection import get_connection
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
