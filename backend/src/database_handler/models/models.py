from sqlalchemy import Column, Integer, String, ForeignKey
from ..db_connector import db_connector

Base = db_connector.Base
class URLS_Mapping(Base):
    __tablename__ = 'urls_mapping'

    id = Column(Integer, primary_key=True, index=True)
    long_url = Column(String, index=True)
    short_url = Column(String, index=True)