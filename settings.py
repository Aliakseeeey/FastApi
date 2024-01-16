from envparse import Env
from dotenv import load_dotenv
import os

load_dotenv()

env = Env()
db_url = os.getenv("DATABASE_URL")
test_db_url = os.getenv("TEST_DATABASE_URL")

REAL_DATABASE_URL = env.str(
    "REAL_DATABASE_URL",
    default=db_url
)

TEST_DATABASE_URL = env.str(
    "TEST_DATABASE_URL",
    default=test_db_url
)

SECRET_KEY: str = env.str("SECRET_KEY", default="secret_key")
ALGORITHM: str = env.str("ALGORITHM", default="HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = env.int("ACCESS_TOKEN_EXPIRE_MINUTES", default=30)
###############################
#        EXAMPLE LINK         #
###############################
# 'postgresql+asyncpg://postgres:password@localhost:5432/postgres'
# postgresql+asyncpg - This is the protocol and driver used to connect to a PostgreSQL database using Asyncpg. postgresql
# postgres:password - This is the username and password to access the database
# localhost:5432 - This is the address and port of the database server
# postgres - This is the name of the database you are connecting to

)

