from sqlalchemy.orm import Session
from database_handler.schemas import NEW_USER_REQUEST, USER_LOGIN, TOKEN_RESPONSE, USER
from database_handler.models import USERS
from database_handler.models import URLS_Mapping
from auth import auth_handler


def create_pay_load(user: str, email: str):
    payload = { "user" : USER(name = user, email = email).dict()}
    return payload

def login_user(db: Session , user : USER_LOGIN):
    try:
        stored_user = db.query(USERS).filter(USERS.email == user.email).first()
        
        if auth_handler.verify_password(user.password, stored_user.hashed_password):
            return f"{auth_handler.create_access_token(payload = create_pay_load(stored_user.name, stored_user.email))}"
       
    except Exception as e:
        raise Exception(f"Error logging user: {e}")
    
def check_user(db: Session, email: str):
    try:
        return db.query(USERS).filter(USERS.email == email).first()
    except Exception as e:
        raise Exception(f"Error checking user: {e}")

def add_user(db: Session, create_url_request: NEW_USER_REQUEST):
    try:
        if check_user(db, create_url_request.email):
            raise Exception("User already exists")
        hashed_password = auth_handler.get_hashed_password(create_url_request.password)
        new_entry = USERS(name=create_url_request.name, email=create_url_request.email, hashed_password=hashed_password)
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)
    except Exception as e:
        raise e

def get_all_users(db: Session):
    try:
        users = db.query(USERS).all()
        return users
    except Exception as e:
        raise Exception(f"Error getting all users: {e}")
    
def get_urls(db: Session, email: str):
    try:
        urls_data = db.query(URLS_Mapping.id, URLS_Mapping.long_url).filter(URLS_Mapping.email == email).all()
        print(f"Urls data: {urls_data}")
        return [{"id": id, "long_url": long_url} for id, long_url in urls_data]
    except Exception as e:
        raise Exception(f"Error getting urls: {e}")
