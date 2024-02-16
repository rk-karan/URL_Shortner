from sqlalchemy.orm import Session

from exceptions.exceptions import NOT_FOUND_EXCEPTION
from constants import DOMAIN_NAME, NULL_TEXT
from database_handler.models import URLS_Mapping
from database_handler.schemas import NEW_URL_REQUEST
from base62conversions.base62conversions import decimal_to_base62 , base62_to_decimal


def create_short_url(db: Session , create_url: NEW_URL_REQUEST, email: str):
    """This function is used to create a new short URL and store the information in the db.

    Args:
        db (Session): DB Session
        create_url (NEW_URL_REQUEST): New URL request
        email (str): Email of the user

    Returns:
        str: Shortened URL
    """
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
    """This function is used to get the original URL from the short URL.

    Args:
        db (Session): DB Session
        short_url (str): Short URL Parameter. (Base62 Encoded ID)

    Returns:
        str: Original URL
    """
    try:
        _id = base62_to_decimal(short_url)
        item = db.query(URLS_Mapping).filter(URLS_Mapping.id == _id).first()
        if item is None:
            raise NOT_FOUND_EXCEPTION
        return item.long_url
    except Exception as e:
        raise e

def delete_url(db: Session, long_url: str, email: str):
    """This function is used to delete the URL from the database.

    Args:
        db (Session): DB Session
        long_url (str): Long URL to be deleted
        email (str): Email of the user

    Raises:
        NOT_FOUND_EXCEPTION: _description_
    """
    try:
        existing_url = db.query(URLS_Mapping).filter_by(email=email, long_url=long_url).first()
        
        if existing_url:
            existing_url.long_url = NULL_TEXT
            existing_url.email = NULL_TEXT
            
            db.commit()
            return
            
        raise NOT_FOUND_EXCEPTION
    
    except Exception as e:
        raise e
    
def edit_long_url(db: Session, old_long_url: str, new_long_url: str, email: str):
    try:
        existing_url = db.query(URLS_Mapping).filter_by(email=email, long_url=old_long_url).first()
        
        if existing_url:
            existing_url.long_url = new_long_url
            db.commit()
            return
        
        raise NOT_FOUND_EXCEPTION
    except Exception as e:
        raise e
