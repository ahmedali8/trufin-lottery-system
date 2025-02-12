import logging
import sys
from colorama import Fore, init


# Initialize colorama for colored log output
init(autoreset=True)


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


def log_winner(email, state, table_name, is_update=False):
    """
    Logs information about adding or updating a winner.

    Args:
        email (str): Winner's email.
        state (str): Winner's state.
        table_name (str): Name of the table where winner is stored.
        is_update (bool): Indicates if it's an update (True) or a new addition (False).
    """
    if is_update:
        logging.info(Fore.YELLOW + f"[UPDATE] Winner updated: {email} for {state} in {table_name}")
    else:
        logging.info(Fore.GREEN + f"[NEW] Winner added: {email} for {state} in {table_name}")


def log_final_winners(table_name, winners):
    """
    Logs the final list of winners.

    Args:
        table_name (str): Name of the table where winners are stored.
        winners (list): List of winners.
    """
    logging.info(Fore.CYAN + f"[RESULT] Final Winners Table: {table_name}")
    for winner in winners:
        logging.info(Fore.MAGENTA + f"[WINNER] {winner}")


def log_info(message):
    """
    Logs a general informational message.

    Args:
        message (str): The info message to log.
    """
    logging.info(Fore.BLUE + f"[INFO] {message}")


def log_warning(message):
    """
    Logs a warning message.

    Args:
        message (str): The warning message to log.
    """
    logging.warning(Fore.YELLOW + f"[WARNING] {message}")


def log_error(message):
    """
    Logs an error message.

    Args:
        message (str): The error message to log.
    """
    logging.error(Fore.RED + f"[ERROR] {message}")

