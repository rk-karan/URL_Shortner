from auth import auth_handler

from sqlalchemy.orm import Session

from constants import USER_EXISTS_MESSAGE
from database_handler.models import USERS
from exceptions import INVALID_USER_EXCEPTION
from database_handler.models import URLS_Mapping
from database_handler.schemas import NEW_USER_REQUEST, USER_LOGIN, USER

def create_pay_load(user: str, email: str):
    """Creates the payload for a given name and email.

    Args:
        user (str): Name of the user
        email (str): Email of the user

    Returns:
        dict: Payload for a given user.
    """
    payload = {"user" : USER(name = user, email = email).dict()}
    return payload

def login_user(db: Session , user : USER_LOGIN):
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
        if not user:
            raise INVALID_USER_EXCEPTION
        
        stored_user = db.query(USERS).filter(USERS.email == user.email).first()
        
        if not stored_user:
            raise INVALID_USER_EXCEPTION
        
        if auth_handler.verify_password(user.password, stored_user.hashed_password):
            return f"{auth_handler.create_access_token(payload = create_pay_load(stored_user.name, stored_user.email))}"
        
        raise INVALID_USER_EXCEPTION
       
    except Exception as e:
        raise e
    
def check_user(db: Session, email: str):
    """Checks the presence of a user in the db using user email.

    Args:
        db (Session): DB Session
        email (str): Email of the user

    Returns:
        bool: True if the user with given email exists.
    """
    try:
        return db.query(USERS).filter(USERS.email == email).first()
    except Exception as e:
        raise e

def add_user(db: Session, create_user_request: NEW_USER_REQUEST):
    """Adds a new user to the db.

    Args:
        db (Session): DB Session
        create_user_request (NEW_USER_REQUEST): NEW_USER_REQUEST class
    """
    try:
        if check_user(db, create_user_request.email):
            raise Exception(USER_EXISTS_MESSAGE)
        
        hashed_password = auth_handler.get_hashed_password(create_user_request.password)
        new_entry = USERS(name=create_user_request.name, email=create_user_request.email, hashed_password=hashed_password)
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)
        
    except Exception as e:
        raise e

def get_all_users(db: Session):
    """Returns all the users in the database.

    Args:
        db (Session): DB Session
    """
    try:
        users = db.query(USERS).all()
        return users
    except Exception as e:
        raise e
    
def get_urls(db: Session, email: str):
    """Retrieves all the shortened urls made by the user with given email.

    Args:
        db (Session): DB Session
        email (str): Email of the user

    Returns:
        list: All urls made by the user with given email.
    """
    try:
        urls_data = db.query(URLS_Mapping.id, URLS_Mapping.long_url).filter(URLS_Mapping.email == email).all()
        return [{"id": id, "long_url": long_url} for id, long_url in urls_data]
    except Exception as e:
        raise e
