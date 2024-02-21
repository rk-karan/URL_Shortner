import os
from database_handler.db_connector.db_connector import DB_Connector
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path=env_path)

DB_URL= os.getenv("DB_URL")
DB_NAME= os.getenv("DB_NAME")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")

test_db_connector = DB_Connector(DB_URL=DB_URL, DB_NAME=DB_NAME, DB_USERNAME=DB_USERNAME, DB_PASSWORD=DB_PASSWORD)