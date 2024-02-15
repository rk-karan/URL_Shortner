from sqlalchemy.orm import Session
from database_handler.schemas import NEW_URL_REQUEST
from database_handler.models import URLS_Mapping
from base62conversions.base62conversions import decimal_to_base62 , base62_to_decimal

from exceptions import NOT_FOUND_EXCEPTION
from constants import DOMAIN_NAME, NULL_TEXT

def create_short_url(db: Session , create_url: NEW_URL_REQUEST, email: str):
    try:
        existing_url = db.query(URLS_Mapping).filter_by(email=NULL_TEXT, long_url=NULL_TEXT).first()
        short_url = None
        _id =  None
        
        if existing_url:
            
            existing_url.email = email
            existing_url.long_url = create_url.long_url
            db.commit()
            _id = decimal_to_base62(existing_url.id)
        else:
            url_obj = URLS_Mapping(long_url=create_url.long_url, email=email)
            db.add(url_obj)
            db.commit()
            db.refresh(url_obj)
            _id = decimal_to_base62(url_obj.id)
        
        if not _id:
            raise Exception
    
        short_url = f"{DOMAIN_NAME}/{_id}"
        return short_url
    except Exception as e:
        raise e

def get_original_url(db: Session, short_url: str):
    try:
        _id = base62_to_decimal(short_url)
        item = db.query(URLS_Mapping).filter(URLS_Mapping.id == _id).first()
        if item is None:
            raise NOT_FOUND_EXCEPTION
        return item.long_url
    except Exception as e:
        raise e

def delete_url(db: Session, long_url: str, email: str):
    try:
        email_to_update = NULL_TEXT
        long_url_to_update = NULL_TEXT
        
        existing_url = db.query(URLS_Mapping).filter_by(email=email, long_url=long_url).first()
        
        if existing_url:
            existing_url.long_url = long_url_to_update
            existing_url.email = email_to_update
            
            db.commit()
            return
            
        raise NOT_FOUND_EXCEPTION
    
    except Exception as e:
        raise e
