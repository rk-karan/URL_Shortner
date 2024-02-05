"""
    This file contains the DB_Connector class which is used to connect to the database and get the db object.
    The db session object is used to perform CRUD operations on the database.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base

from logger.logger import logger

load_dotenv()

DB_URL= os.getenv("DB_URL")
DB_NAME= os.getenv("DB_NAME")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")

class DB_Connector:
    def __init__(self):
        """
        Initializes the DB_Connector class.

        Raises:
            Exception: DB_URL, DB_NAME, DB_USERNAME, DB_PASSWORD are required
        """
        try:
            self.logger = logger
            
            if(not DB_URL or not DB_NAME or not DB_USERNAME or not DB_PASSWORD):
                raise Exception("DB_URL, DB_NAME, DB_USERNAME, DB_PASSWORD are required")
            
            self.DB_URL = DB_URL
            self.DB_NAME = DB_NAME
            self.DB_USERNAME = DB_USERNAME
            self.DB_PASSWORD = DB_PASSWORD

            self.initialize_database()
            
        except Exception as e:
            self.logger.log(f"Error in DBConnector: {e}", error_tag=True)
            raise e
    
    def initialize_database(self):
        """Initializes the database connection, creates the session object and base.
        """
        
        try:
            self.engine = create_engine(f"postgresql://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_URL}/{self.DB_NAME}")
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            self.Metadata = MetaData()
            self.Metadata.bind = self.engine
            self.Base = declarative_base()
        except Exception as e:
            self.logger.log(f"Error in initialize_database: {e}", error_tag=True)
            raise e

    def get_db(self):
        """
        Generates the db session object.

        Yields:
            session: db session object.
        """
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