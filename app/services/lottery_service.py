import time
from app.repositories.winner_repository import (
    create_versioned_table, insert_winner, get_winner_count, get_winners, get_new_version
)
from app.api.fetch_random_users import fetch_random_users
from app.utils.logger import get_logger
from app.utils.constants import MAX_WINNER_COUNT

# Initialize logger
logger = get_logger(__name__)

def process_winners():
    """
    Manages the lottery process, ensuring 25 unique winners from different states.
    """
    version = get_new_version()
    table_name = create_versioned_table(version)

    while get_winner_count(table_name) < MAX_WINNER_COUNT:
        users = fetch_random_users()
        for user in users:
            state = user.get("address", {}).get("state")
            email = user.get("email")
            if state and email:
                existing_count = get_winner_count(table_name)

                # Insert winner
                insert_winner(email, state, table_name)

                # Determine if it's an update or insert
                if existing_count < get_winner_count(table_name):
                    logger.info(f"New winner added: {email} from {state} in table {table_name}")
                else:
                    logger.info(f"Updated existing winner: {email} from {state} in table {table_name}")

                if get_winner_count(table_name) >= 25:
                    break
        time.sleep(10)

    winners = get_winners(table_name)
    logger.info(f"Lottery completed. Total winners stored in {table_name}: {len(winners)}")
