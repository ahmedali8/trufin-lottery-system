import psycopg2
import requests
import time
import logging
import os
from typing import List, Dict
from psycopg2 import sql
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# TODO: do a versioned db for storing the previous history of winners

# Database setup
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")

def initialize_db():
    """Creates the winner table if it doesn't exist."""
    with psycopg2.connect(dbname=db_name, user=db_user, password=db_password, host=db_host, port=db_port) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS winners (
                    id SERIAL PRIMARY KEY,
                    email TEXT NOT NULL,
                    state TEXT UNIQUE NOT NULL
                )
            """)
            conn.commit()

def fetch_users() -> List[Dict]:
    """Fetches 5 random users from the API with retry logic."""
    url = "https://random-data-api.com/api/users/random_user?size=5"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"API request failed: {e}")
        return []

def add_winner(user: Dict):
    """Inserts or updates a winner in the database."""
    with psycopg2.connect(dbname=db_name, user=db_user, password=db_password, host=db_host, port=db_port) as conn:
        with conn.cursor() as cursor:
            user_id = user["id"]
            email = user["email"]
            state = user["address"]["state"]

            cursor.execute("""
                INSERT INTO winners (id, email, state)
                VALUES (%s, %s, %s)
                ON CONFLICT (state)
                DO UPDATE SET id = EXCLUDED.id, email = EXCLUDED.email
            """, (user_id, email, state))
            logging.info(f"Added/Updated winner for state {state}: {email}")
            conn.commit()

def get_winner_states() -> List[str]:
    """Returns a list of states that already have winners."""
    with psycopg2.connect(dbname=db_name, user=db_user, password=db_password, host=db_host, port=db_port) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT state FROM winners")
            return [row[0] for row in cursor.fetchall()]

def print_winners():
    """Prints the final winner table."""
    with psycopg2.connect(dbname=db_name, user=db_user, password=db_password, host=db_host, port=db_port) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM winners")
            winners = cursor.fetchall()
            logging.info("Final Winners Table:")
            for winner in winners:
                print(winner)

def main():
    initialize_db()
    while True:
        if len(get_winner_states()) >= 25:
            logging.info("Lottery complete!")
            break

        users = fetch_users()
        for user in users:
            if "address" in user and "state" in user["address"]:
                add_winner(user)

        time.sleep(10)  # Wait 10 seconds before fetching again

    print_winners()

if __name__ == "__main__":
    main()
