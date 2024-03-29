from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
JWT_SECRET = os.environ.get("JWT_SECRET")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TTL = int(os.environ.get("ACCESS_TTL"))
REFRESH_TTL = int(os.environ.get("REFRESH_TTL"))