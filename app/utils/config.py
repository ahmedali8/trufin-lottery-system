import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL")

TABLE_PREFIX = os.getenv("TABLE_PREFIX")

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}
