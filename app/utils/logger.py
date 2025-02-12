import logging
import sys

# Configure logging settings
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)  # Log to console
    ]
)

def get_logger(name):
    """
    Returns a configured logger instance.

    Args:
        name (str): Name of the logger (usually __name__ of the calling module).

    Returns:
        logging.Logger: Configured logger instance.
    """
    return logging.getLogger(name)
