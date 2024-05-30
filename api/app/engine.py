import os
from sqlalchemy import create_engine

class Engine:
    def __init__(self):
        dbhost = os.getenv("DATABASE_HOST", "unknown_host")
        dbuser = os.getenv("DATABASE_USER", "unknown_user")
        dbport = os.getenv("DATABASE_PORT", "unknown_port")
        dbname = os.getenv("DATABASE_NAME", "unknown_name")
        dbpassword = os.getenv("DATABASE_PASSWORD", "unknown_password")

        sqlalchemy_url = f"postgresql+psycopg://{dbuser}:{dbpassword}@{dbhost}:{dbport}/{dbname}"

        self.engine = create_engine(sqlalchemy_url)

    def get_engine(self):
        return self.engine