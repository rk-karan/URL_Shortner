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
        existing_url = db.query(URLS_Mapping).filter(URLS_Mapping.email.is_('NULL')).first()
        short_url = None
        
        if existing_url:
            
            update_data = {
                "long_url": create_url.long_url,
                "email": email
            }
            db.execute(update(URLS_Mapping).where(URLS_Mapping.id == existing_url.id).values(update_data))
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
    _id = base62_to_decimal(short_url)
    item = db.query(URLS_Mapping).filter(URLS_Mapping.id == _id).first()
    
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item.long_url

def delete_url(db: Session, long_url: str, email: str):
    try:
        email_to_update = 'NULL'
        long_url_to_update = 'NULL'
        db.execute(
            update(URLS_Mapping).
            where((URLS_Mapping.email == email) & (URLS_Mapping.long_url ==long_url)).  # Filter based on the old email
            values(email=email_to_update, long_url=long_url_to_update)
        )
        db.commit()
    except Exception as e:
        raise Exception(f"Error deleting url: {e}")
