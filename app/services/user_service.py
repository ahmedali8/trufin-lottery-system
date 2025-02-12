from app.repositories.winner_repository import insert_winner, get_winners, get_winner_count
from app.utils.logger import log_info, log_error


def add_winner(email: str, state: str, table_name: str):
    """
    Adds a new winner to the database or updates an existing winner from the same state.
    """
    try:
        insert_winner(email, state, table_name)
        log_info(f"Successfully added or updated winner: {email} for state {state} in table {table_name}")
    except Exception as e:
        log_error(f"Error adding winner: {e}")


def get_all_winners(table_name: str):
    """
    Retrieves all winners from the specified table.
    """
    try:
        winners = get_winners(table_name)
        log_info(f"Retrieved {len(winners)} winners from {table_name}")
        return winners
    except Exception as e:
        log_error(f"Error fetching winners: {e}")
        return []


def count_winners(table_name: str) -> int:
    """
    Returns the total number of winners in the specified table.
    """
    try:
        count = get_winner_count(table_name)
        log_info(f"Winner count for {table_name}: {count}")
        return count
    except Exception as e:
        log_error(f"Error counting winners: {e}")
        return 0

