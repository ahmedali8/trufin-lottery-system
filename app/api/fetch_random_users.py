import requests
from app.utils.config import API_URL
from app.utils.logger import get_logger

# Initialize logger
logger = get_logger(__name__)

def fetch_random_users(size=5):
    """
    Fetches a list of random users from the external API.

    Args:
        size (int): Number of users to fetch per request.

    Returns:
        list: A list of user dictionaries if successful, else an empty list.
    """
    url = f"{API_URL}?size={size}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        users = response.json()
        logger.info(f"Successfully fetched {len(users)} users.")
        return users
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching random users: {e}")
        return []

def fetch_default_users():
    """
    Fetches a default number of 5 random users from the external API.

    Returns:
        list: A list of user dictionaries if successful, else an empty list.
    """
    return fetch_random_users(size=5)
