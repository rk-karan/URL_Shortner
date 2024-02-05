from fastapi import HTTPException
from sqlalchemy.orm import Session
from database_handler.schemas import NEW_URL_REQUEST
from database_handler.models import URLS_Mapping
from sqlalchemy import func
from base62conversions.base62conversions import decimal_to_base62 , base62_to_decimal
from database_handler.db_connector import db_connector
from sqlalchemy import MetaData

def create_short_url( db: Session , create_url: NEW_URL_REQUEST, hostname):
    if 'urls_mapping' in db_connector.Metadata:
        short_url_count = db.query(func.count(URLS_Mapping.id)).scalar()
        short_url_id = short_url_count + 1
        short_url = "http://localhost:8000/" + decimal_to_base62(short_url_id)
    else:
        short_url = "http://localhost:8000/" + decimal_to_base62(1)
    url_obj = URLS_Mapping(long_url=create_url.long_url, short_url=short_url)
    db.add(url_obj)
    db.commit()
    db.refresh(url_obj)
    return {"short_url": short_url}

def get_original_url(db: Session, short_url):
    id_ = base62_to_decimal(short_url)
    print("id: ",id_)
    item = db.query(URLS_Mapping).filter(URLS_Mapping.id == id_).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item.long_url
