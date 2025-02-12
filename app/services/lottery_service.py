import time
from app.repositories.winner_repository import (
    create_versioned_table, insert_winner, get_winner_count, get_winners, get_new_version
)
from app.api.fetch_random_users import fetch_default_users
from app.utils.logger import log_info, log_winner, log_final_winners
from app.utils.constants import MAX_WINNER_COUNT, DEFAULT_SLEEP_TIME


def process_winners():
    """
    Manages the lottery process, ensuring 25 unique winners from different states.
    """
    version = get_new_version()
    table_name = create_versioned_table(version)

    while get_winner_count(table_name) < MAX_WINNER_COUNT:
        users = fetch_default_users()
        for user in users:
            state = user.get("address", {}).get("state")
            email = user.get("email")
            if state and email:
                existing_count = get_winner_count(table_name)

                # Insert winner
                insert_winner(email, state, table_name)

                # Determine if it's an update or insert
                if existing_count < get_winner_count(table_name):
                    log_winner(email, state, table_name, is_update=False)
                else:
                    log_winner(email, state, table_name, is_update=True)

                if get_winner_count(table_name) >= 25:
                    break
        time.sleep(DEFAULT_SLEEP_TIME)

    winners = get_winners(table_name)
    log_final_winners(table_name, winners)
    log_info(f"Lottery process completed for table: {table_name}")

