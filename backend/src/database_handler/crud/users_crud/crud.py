"""This module contains the CRUD operations for the users.
"""
from sqlalchemy.orm import Session

from auth import auth_handler
from database_handler.schemas import USER, PAYLOAD
from base62conversions import decimal_to_base62
from database_handler.models import USERS, URLS_Mapping
from constants import NULL_ENTRY_IN_URLS_MAPPING, USER_EMAIL_KEY
from exceptions.exceptions import User_Already_Exists, Invalid_User, Missing_Params

def create_pay_load(name: str, email: str):
    """Creates the payload for a given name and email.

    Args:
        user (str): Name of the user
        email (str): Email of the user

    Returns:
        dict: Payload for a given user.
    """
    if not name or not email:
        raise Missing_Params
    
    return PAYLOAD(user= USER(name = name, email = email).dict()).dict()

def get_urls(user: dict= None, urls= []):
    """Returns the user and urls in a dictionary.

    Args:
        user (dict): user token dict. Defaults to None.
        urls (list): Defaults to [].

    Raises:
        MISSING_PARAMS_EXCEPTION
    """
    
    if not user:
        raise Missing_Params
        
    for url in urls:
        url.update({'short_url': decimal_to_base62(int(url.get('id')))})

    return { 'user': user, 'urls': urls }
    
def check_user(db: Session, email: str):
    """Checks the presence of a user in the db using user email.

    Args:
        db (Session): DB Session
        email (str): Email of the user

    Returns:
        bool: True if the user with given email exists.
    """
    try:
        if not email:
            raise Missing_Params
        
        return db.query(USERS).filter(USERS.email == email).first()
    except Exception as e:
        raise e

def add_user(db: Session, email: str, password: str, name: str):
    """Adds a new user to the db.

    Args:
        db (Session): DB Session
        create_user_request (NEW_USER_REQUEST): NEW_USER_REQUEST class
    """
    try:
        if not email or not password or not name:
            raise Missing_Params
        
        if check_user(db, email):
            raise User_Already_Exists
        
        hashed_password = auth_handler.get_hashed_password(password)
        new_entry = USERS(name=name, email=email, hashed_password=hashed_password)
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)
        
    except Exception as e:
        raise e

def login_user(db: Session, email: str, password: str):
    """

    Args:
        db (Session): DB Session
        user (USER_LOGIN): USER_LOGIN class

    Raises:
        INVALID_USER_EXCEPTION

    Returns:
        str: JWT Token after successful login
    """
    try:
        if not email or not password:
            raise Invalid_User
        
        stored_user = db.query(USERS).filter(USERS.email == email).first()
        
        if not stored_user:
            raise Invalid_User
        
        if auth_handler.verify_password(password, stored_user.hashed_password):
            return f"{auth_handler.create_access_token(payload = create_pay_load(stored_user.name, stored_user.email))}"
        
        raise Invalid_User
       
    except Exception as e:
        raise e

def get_user_profile_content(db: Session, user: dict):
    """Retrieves all the shortened urls made by the user with given email.

    Args:
        db (Session): DB Session
        email (str): Email of the user

    Returns:
        list: All urls made by the user with given email.
    """
    try:
        if not user or not user.get(USER_EMAIL_KEY):
            raise Missing_Params
        
        urls_data = db.query(URLS_Mapping.id, URLS_Mapping.long_url).filter(URLS_Mapping.email == user.get(USER_EMAIL_KEY)).all()
        processed_url_data = [{"id": id, "long_url": long_url} for id, long_url in urls_data]
        
        return get_urls(user = user, urls = processed_url_data)
    except Exception as e:
        raise e

def change_user_password(db: Session, email: str, new_password: str, old_password: str):
    """Changes the password of the user with given email.

    Args:
        db (Session): DB Session
        email (str): Email of the user
        new_password (str): New password
        old_password (str): Old password

    Raises:
        MISSING_PARAMS_EXCEPTION
        INVALID_USER_EXCEPTION
    """
    try:
        if not email or not new_password or not old_password:
            raise Missing_Params
        
        stored_user = db.query(USERS).filter(USERS.email == email).first()
        
        if not stored_user and not auth_handler.verify_password(old_password, stored_user.hashed_password):
            raise Invalid_User

        hashed_password = auth_handler.get_hashed_password(new_password)
        db.query(USERS).filter(USERS.email == email).update({"hashed_password": hashed_password})
        db.commit()
        return
    except Exception as e:
        raise e

def delete_user_by_email(db: Session, email: str):
    """Deletes the user with given email from the db.

    Args:
        db (Session): DB Session
        email (str): Email of the user

    Raises:
        INVALID_USER_EXCEPTION
    """
    try:
        if not email:
            Invalid_User

        db.query(URLS_Mapping).filter(URLS_Mapping.email == email).update(NULL_ENTRY_IN_URLS_MAPPING)
        db.commit()
        
        db.query(USERS).filter(USERS.email == email).delete()
        db.commit()
        return
    except Exception as e:
        raise e
