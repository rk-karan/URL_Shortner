from fastapi import HTTPException
from sqlalchemy.orm import Session
from database_handler.schemas import NEW_URL_REQUEST
from database_handler.models import URLS_Mapping
from sqlalchemy import func
from base62conversions.base62conversions import decimal_to_base62 , base62_to_decimal
from database_handler.db_connector import db_connector
from sqlalchemy import MetaData

def create_short_url(db: Session , create_url: NEW_URL_REQUEST, email: str):
    try:
        url_obj = URLS_Mapping(long_url=create_url.long_url, email=email)
        db.add(url_obj)
        db.commit()
        db.refresh(url_obj)
    
        short_url = "http://localhost:8000/" + decimal_to_base62(url_obj.id)
        return {"short_url": short_url}
    except Exception as e:
        Exception(f"Error creating short url:{e}")

def get_original_url(db: Session, short_url: str):
    _id = base62_to_decimal(short_url)
    item = db.query(URLS_Mapping).filter(URLS_Mapping.id == _id).first()
    
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item.long_url
