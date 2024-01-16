from envparse import Env
from dotenv import load_dotenv
import os

load_dotenv()

env = Env()
db_url = os.getenv("DATABASE_URL")

REAL_DATABASE_URL = env.str(
    "REAL_DATABASE_URL",
    default=db_url
)