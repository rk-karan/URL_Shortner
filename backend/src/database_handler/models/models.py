""" This module contains the models for the database.
"""
from ..db_connector import db_connector
from sqlalchemy import Column, Integer, String, DateTime, func, UniqueConstraint

Base = db_connector._Base

class URLS_Mapping(Base):
    __tablename__ = 'urls_mapping'

    id = Column(Integer, primary_key=True, index=True)
    long_url = Column(String, index=True)
    email = Column(String, index=True)
    created_on = Column(DateTime, default= func.now())
    edited_on = Column(DateTime, default= func.now())
    hit_count = Column(Integer, default=0)

class USERS(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True, unique = True)
    hashed_password = Column(String)