from fastapi import HTTPException
from sqlalchemy.orm import Session
from database_handler.schemas import NEW_URL_REQUEST
from database_handler.models import URLS_Mapping
from sqlalchemy import func
from base62conversions.base62conversions import decimal_to_base62 , base62_to_decimal
from database_handler.db_connector import db_connector
from sqlalchemy import MetaData
from sqlalchemy import update

def create_short_url(db: Session , create_url: NEW_URL_REQUEST, email: str):
    try:
        print(f"create_url: {create_url} email: {email} db: {db}")
        existing_url = db.query(URLS_Mapping).filter_by(email='NULL', long_url='NULL').first()
        print(f"existing_url: {existing_url}")
        short_url = None
        
        if existing_url:
            
            existing_url.email = email
            existing_url.long_url = create_url.long_url
            db.commit()
            short_url = "http://localhost:8000/" + decimal_to_base62(existing_url.id)
        else:
            url_obj = URLS_Mapping(long_url=create_url.long_url, email=email)
            db.add(url_obj)
            db.commit()
            db.refresh(url_obj)
    
            short_url = "http://localhost:8000/" + decimal_to_base62(url_obj.id)
            
        return {"short_url": short_url}
    except Exception as e:
        Exception(f"Error creating short url:{e}")

def get_original_url(db: Session, short_url: str):
    try:
        _id = base62_to_decimal(short_url)
        # print(f"_id: {_id}")
        item = db.query(URLS_Mapping).filter(URLS_Mapping.id == _id).first()
        # print(item)
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return item.long_url
    except Exception as e:
        raise Exception(f"Error getting original url: {e}")

def delete_url(db: Session, long_url: str, email: str):
    try:
        email_to_update = 'NULL'
        long_url_to_update = 'NULL'
        
        existing_url = db.query(URLS_Mapping).filter_by(email=email, long_url=long_url).first()
        
        if existing_url:
            existing_url.long_url = long_url_to_update
            existing_url.email = email_to_update
            
            db.commit()
            return {"message": "URL deleted successfully"}
        else:
            return {"message": "URL not found"}
    except Exception as e:
        raise Exception(f"Error deleting url: {e}")
