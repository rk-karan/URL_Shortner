from sqlalchemy.orm import Session

from database_handler.schemas import NEW_USER_REQUEST, USER_LOGIN
from database_handler.models import USERS
from logger import logger

from passlib.context import CryptContext
from auth import JWT_Handler

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
auth_handler = JWT_Handler()

def add_user(db: Session, create_url_request: NEW_USER_REQUEST):
    
    try:
        if check_user(db, create_url_request.email):
            raise Exception("User already exists")
        
        hashed_password = bcrypt_context.hash(create_url_request.password)
        new_entry = USERS(name=create_url_request.name, email=create_url_request.email, hashed_password=hashed_password)
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)
        
        user_login = USER_LOGIN(email=new_entry.email, password=hashed_password)
        return auth_handler.signJWT(user=user_login)
        
    except Exception as e:
        logger.log(f"Error adding user: {e}", error_tag=True)
        raise e
    
def check_user(db: Session, email: str):
    try:
        return db.query(USERS).filter(USERS.email == email).first()
    except Exception as e:
        logger.log(f"Error checking user: {e}", error_tag=True)
        raise e
