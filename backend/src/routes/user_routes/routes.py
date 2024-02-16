from fastapi import APIRouter, Depends, Body, Response, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from database_handler.db_connector import db_connector

from logger import logger
from decorators import log_info
from utils.send_response import send_response
from base62conversions import decimal_to_base62
from database_handler.crud.users_crud.crud import add_user, login_user, get_urls, delete_user, change_user_password
from database_handler.schemas import NEW_USER_REQUEST, LOGIN_RESPONSE, USER_LOGIN, MESSAGE_RESPONSE, USER_PASSWORD_CHANGE

from auth import auth_handler
from constants import SIGNUP_SUCCESS_MESSAGE, LOGOUT_SUCCESS_MESSAGE, ACCESS_TOKEN_KEY, AUTHORIZATION_SCHEME, DELETE_USER_SUCCESS_MESSAGE, USER_EMAIL_KEY, CHANGE_PASSWORD_SUCCESS_MESSAGE

router = APIRouter(
    prefix="/user",
    tags=["user"],
)

def get_user_profile_content(user= None, urls= []):
    
    if not user:
        return
        
    for url in urls:
        url.update({'id': decimal_to_base62(int(url.get('id')))})

    return { 'user': user, 'urls': urls }


@router.post("/create_user", status_code=status.HTTP_201_CREATED)
async def create_user(create_user_request: NEW_USER_REQUEST = Body(default=None), db: Session = Depends(db_connector.get_db) , endpoint = 'create_user'):
    """This api endpoint adds a new user to the db.

    Args:
        create_user_request (NEW_USER_REQUEST, optional): NEW_URL_REQUEST class. Defaults to Body(default=None).
        db (Session, optional): DB Session. Defaults to Depends(db_connector.get_db).
    """
    try:
        add_user(db , create_user_request)
        return MESSAGE_RESPONSE(message=SIGNUP_SUCCESS_MESSAGE).dict()
    except Exception as e:
        return send_response(content=e, status_code=status.HTTP_400_BAD_REQUEST, error_tag=True)

@router.post("/login", status_code=status.HTTP_200_OK)
async def user_login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(db_connector.get_db) , endpoint = 'login_user'):
    """This api endpoint logs in an existing user using JWT Tokens. The token is sent using cookies.

    Args:
        response (Response): Response class instance.
        form_data (OAuth2PasswordRequestForm, optional): OAuth2PasswordRequestForm class instance. Defaults to Depends().
        db (Session, optional): DB Session. Defaults to Depends(db_connector.get_db).
    """
    try:
        user_login = USER_LOGIN(email = form_data.username, password = form_data.password)
        access_token = login_user(db , user_login)
        response.set_cookie(key = ACCESS_TOKEN_KEY, value =f"{AUTHORIZATION_SCHEME} {access_token}", httponly = True)
        
        return LOGIN_RESPONSE(access_token=access_token).dict() 
    except Exception as e:
        return send_response(content=e, status_code=status.HTTP_400_BAD_REQUEST, error_tag=True)

@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(response: Response, token: str = Depends(auth_handler._O2AUTH2_SCHEME)):
    """This api endpoint logs out an existing user. The user must be logged in.

    Args:
        response (Response): Response class instance.
        token (str, optional): JWT Token. Defaults to Depends(auth_handler._O2AUTH2_SCHEME).
    """
    try:
        auth_handler.get_current_user(token)
        response.set_cookie(key=ACCESS_TOKEN_KEY, value=None)
        return MESSAGE_RESPONSE(message=LOGOUT_SUCCESS_MESSAGE).dict()
    except Exception as e:
        return send_response(content=e, status_code=status.HTTP_401_UNAUTHORIZED, error_tag=True)

@router.get("/me", status_code=status.HTTP_200_OK)
async def get_user_me(db: Session = Depends(db_connector.get_db), token: str = Depends(auth_handler._O2AUTH2_SCHEME), endpoint = 'current_active_user'):
    """This api endpoint retrieves all the information of the current active user. The user must be logged in.

    Args:
        db (Session, optional): DB Session. Defaults to Depends(db_connector.get_db).
        token (str, optional): JWT Token. Defaults to Depends(auth_handler._O2AUTH2_SCHEME).
    """
    try:
        user = auth_handler.get_current_user(token)
        urls = get_urls(db, user.get(USER_EMAIL_KEY))
        return send_response(content=get_user_profile_content(user, urls), status_code=status.HTTP_200_OK)
    
    except Exception as e:
        return send_response(content=e, status_code=status.HTTP_404_NOT_FOUND, error_tag=True)

@router.put("/change_password", status_code=status.HTTP_200_OK)
async def change_password(response: Response, user_password_change: USER_PASSWORD_CHANGE = Body(default=None), db: Session = Depends(db_connector.get_db), token: str = Depends(auth_handler._O2AUTH2_SCHEME), endpoint = 'change_password'):
    try:
        user = auth_handler.get_current_user(token)
        change_user_password(db, user.get(USER_EMAIL_KEY), user_password_change.new_password)
        response.set_cookie(key=ACCESS_TOKEN_KEY, value=None)
        
        return MESSAGE_RESPONSE(message=CHANGE_PASSWORD_SUCCESS_MESSAGE).dict()
    except Exception as e:
        return send_response(content=e, status_code=status.HTTP_400_BAD_REQUEST, error_tag=True)

@router.delete("/delete_user_by_email", status_code=status.HTTP_200_OK)
async def delete_user_by_email(response: Response, db: Session = Depends(db_connector.get_db), token: str = Depends(auth_handler._O2AUTH2_SCHEME), endpoint = 'delete_user_by_email'):
    try:
        user = auth_handler.get_current_user(token)
        delete_user(db, user.get(USER_EMAIL_KEY))
        response.set_cookie(key=ACCESS_TOKEN_KEY, value=None)
        
        return MESSAGE_RESPONSE(message=DELETE_USER_SUCCESS_MESSAGE).dict()
    except Exception as e:
        return send_response(content=e, status_code=status.HTTP_400_BAD_REQUEST, error_tag=True)
