import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv


class Session:
    def __init__(self):
        load_dotenv()
        dbhost = os.getenv("DATABASE_HOST", "unknown_host")
        dbuser = os.getenv("DATABASE_USER", "unknown_user")
        dbport = os.getenv("DATABASE_PORT", "unknown_port")
        dbname = os.getenv("DATABASE_NAME", "unknown_name")
        dbpassword = os.getenv("DATABASE_PASSWORD", "unknown_password")
        dbadapter = os.getenv("DATABASE_ADAPTER", "postgresql+psycopg")

        sqlalchemy_url = f"{
            dbadapter}://{dbuser}:{dbpassword}@{dbhost}:{dbport}/{dbname}"

        engine = create_engine(sqlalchemy_url)
        self.session = sessionmaker(bind=engine)

    def get_session(self):
        return self.session
