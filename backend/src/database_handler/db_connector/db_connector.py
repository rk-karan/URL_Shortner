import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from decorators import log_info
from logger import logger


dotEnv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotEnv_path)

DB_URL= os.environ.get("DB_URL")
DB_NAME= os.environ.get("DB_NAME")
DB_USERNAME = os.environ.get("DB_USERNAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

class DB_Connector:
    def __init__(self):
        try:
            
            if(not DB_URL or not DB_NAME or not DB_USERNAME or not DB_PASSWORD):
                raise Exception("DB_URL, DB_NAME, DB_USERNAME, DB_PASSWORD are required")
            
            self.DB_URL = DB_URL
            self.DB_NAME = DB_NAME
            self.DB_USERNAME = DB_USERNAME
            self.DB_PASSWORD = DB_PASSWORD
            
            self.logger = logger

            self.initialize_database()
            
        except Exception as e:
            self.logger.log(f"Error in DBConnector: {e}", error_tag=True)
    
    @log_info
    def initialize_database(self):
        
        try:
            self.engine = create_engine(f"postgresql://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_URL}/{self.DB_NAME}")
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            self.Base = declarative_base()
        except Exception as e:
            self.logger.log(f"Error in initialize_database: {e}", error_tag=True)
    
    @log_info  
    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
            self.logger.log("Database connection successful")
        except Exception as e:
            self.logger.log(f"Error connecting to the database: {e}", error_tag=True)
        finally:
            db.close()
            self.logger.log("Database connection closed")

db_connector = DB_Connector()