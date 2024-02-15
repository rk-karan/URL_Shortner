from sqlalchemy import Column, Integer, String
from ..db_connector import db_connector

Base = db_connector.Base

class URLS_Mapping(Base):
    __tablename__ = 'urls_mapping'

    id = Column(Integer, primary_key=True, index=True)
    long_url = Column(String, index=True)
    email = Column(String, index=True)

class USERS(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True, unique = True)
    hashed_password = Column(String, index=True)