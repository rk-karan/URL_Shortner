"""This module handles the CRUD operations for the URLS_Mapping table.
"""
import os
from logger import logger
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from database_handler.models import URLS_Mapping
from base62conversions.base62conversions import decimal_to_base62 , base62_to_decimal
from exceptions.exceptions import Not_Found, Missing_Params, URL_Create_Limit_Reached, URL_Create_URL_Already_Exists
from constants import DOMAIN_NAME, NULL_ENTRY_IN_URLS_MAPPING, USER_EMAIL_KEY, LONG_URL_KEY, NULL_INTEGER, URL_HIT_COUNT_KEY

# Load Environment Variables
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'config', '.env')
load_dotenv(dotenv_path=env_path)

URL_CREATE_MAX_LIMIT = os.getenv("URL_CREATE_MAX_LIMIT")

def get_short_url(domain_name: str = DOMAIN_NAME, entry_id: int = None):
    
    if not entry_id:
        raise Missing_Params
    
    return f"{domain_name}/{entry_id}"

async def increment_hit_count(db: Session, entry_id: int):
    """This function is used to increment the hit count of the URL.

    Args:
        db (Session): DB Session
        _id (int): ID of the URL
    """
    try:
        logger.log(f"Incrementing hit count for URL with ID: {entry_id}")
        if not entry_id:
            raise Missing_Params
        
        existing_url = db.query(URLS_Mapping).filter_by(id=entry_id).first()
        
        if existing_url:
            existing_url.hit_count = existing_url.hit_count+1
            db.commit()
            
            logger.log(f"SUCCESSFUL: Hit count incremented for URL with ID: {entry_id}")
            return
        
        raise Not_Found
    except Exception as e:
        raise e

def create_short_url(db: Session , long_url: str, email: str):
    """This function is used to create a new short URL and store the information in the db.

    Args:
        db (Session): DB Session
        long_url (str): New URL request
        email (str): Email of the user

    Returns:
        str: Shortened URL
    """
    try:
        if long_url is None or email is None:
            raise Missing_Params
        
        if db.query(URLS_Mapping).filter(URLS_Mapping.email == email).count() >= int(URL_CREATE_MAX_LIMIT):
            raise URL_Create_Limit_Reached
        
        if db.query(URLS_Mapping).filter(URLS_Mapping.long_url == long_url and URLS_Mapping.email==email).count() > 0:
            raise URL_Create_URL_Already_Exists

        existing_url = db.query(URLS_Mapping).filter_by(email=NULL_ENTRY_IN_URLS_MAPPING.get(USER_EMAIL_KEY), long_url=NULL_ENTRY_IN_URLS_MAPPING.get(LONG_URL_KEY)).first()
        short_url = None
        entry_id =  None
        
        if existing_url:
            existing_url.email = email
            existing_url.long_url = long_url
            existing_url.created_on = datetime.utcnow()
            existing_url.edited_on = datetime.utcnow()
            existing_url.hit_count = NULL_INTEGER
            
            db.commit()
            entry_id = decimal_to_base62(existing_url.id)
        else:
            url_obj = URLS_Mapping(long_url=long_url, email=email)
            db.add(url_obj)
            db.commit()
            db.refresh(url_obj)
            entry_id = decimal_to_base62(url_obj.id)
        
        short_url = get_short_url(entry_id=entry_id)
        return short_url

    except Exception as e:
        raise e

def get_original_url(db: Session, short_url: str):
    """This function is used to get the original URL from the short URL.

    Args:
        db (Session): DB Session
        short_url (str): Short URL Parameter. (Base62 Encoded ID)

    Returns:
        str: Original URL
    """
    try:
        if not short_url:
            raise Missing_Params
        
        entry_id = base62_to_decimal(short_url)
        item = db.query(URLS_Mapping).filter(URLS_Mapping.id == entry_id).first()
        
        if item is None:
            raise Not_Found

        return (item.long_url, entry_id)
    except Exception as e:
        raise e

def delete_url(db: Session, entry_id: int, email: str, long_url: str):
    """This function is used to delete the URL from the database.

    Args:
        db (Session): DB Session
        long_url (str): Long URL to be deleted
        email (str): Email of the user

    Raises:
        NOT_FOUND_EXCEPTION: _description_
    """
    try:
        if not entry_id or not email:
            raise Missing_Params
        
        existing_url = db.query(URLS_Mapping).filter_by(id=entry_id).first()
        
        if existing_url and existing_url.email == email and existing_url.long_url == long_url:
            existing_url.long_url = NULL_ENTRY_IN_URLS_MAPPING.get(LONG_URL_KEY)
            existing_url.email = NULL_ENTRY_IN_URLS_MAPPING.get(USER_EMAIL_KEY)
            existing_url.hit_count = NULL_ENTRY_IN_URLS_MAPPING.get(URL_HIT_COUNT_KEY)
            
            db.commit()
            return
            
        raise Not_Found
    except Exception as e:
        raise e
    
def edit_long_url(db: Session, entry_id: int, new_long_url: str, email: str, old_long_url: str):
    """This function is used to edit the long URL in the database.

    Args:
        db (Session): DB Session
        old_long_url (str): Previous Long URL
        new_long_url (str): New Long URL
        email (str): Email of the user

    Raises:
        NOT_FOUND_EXCEPTION
    """
    try:
        if not entry_id or not new_long_url or not email:
            raise Missing_Params
        
        existing_url = db.query(URLS_Mapping).filter_by(id=entry_id).first()
        
        if existing_url and existing_url.email == email and existing_url.long_url == old_long_url:
            existing_url.long_url = new_long_url
            existing_url.edited_on = datetime.utcnow()
            db.commit()
            return
        
        raise Not_Found
    except Exception as e:
        raise e
