from fastapi import APIRouter, Depends, Body, Response, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from database_handler.db_connector import db_connector

from database_handler.schemas import NEW_USER_REQUEST, LOGIN_RESPONSE, USER_LOGIN, MESSAGE_RESPONSE
from utils.send_response import send_response
from logger import logger
from decorators import log_info
from database_handler.crud.users_crud.crud import add_user, login_user, get_urls
from base62conversions import decimal_to_base62

from auth import auth_handler
from constants import SIGNUP_SUCCESS_MESSAGE, LOGOUT_SUCCESS_MESSAGE, ACCESS_TOKEN_KEY, AUTHORIZATION_SCHEME

router = APIRouter(
    prefix="/user",
    tags=["user"],
)

@router.post("/create_user")
async def create_user(response: Response, create_user_request: NEW_USER_REQUEST = Body(default=None), db: Session = Depends(db_connector.get_db) , endpoint = 'create_user'):
    print(create_user_request)
    try:
        add_user(db , create_user_request)
        return MESSAGE_RESPONSE(message=SIGNUP_SUCCESS_MESSAGE).dict()
    except Exception as e:
        return send_response(content=e, status_code=status.HTTP_400_BAD_REQUEST, error_tag=True)

@router.post("/login", status_code=status.HTTP_200_OK)
async def user_login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(db_connector.get_db) , endpoint = 'login_user'):
    try:
        user_login = USER_LOGIN(email = form_data.username, password = form_data.password)
        access_token = login_user(db , user_login)
        response.set_cookie(key = ACCESS_TOKEN_KEY , value =f"{AUTHORIZATION_SCHEME} {access_token}", httponly = True)

        return LOGIN_RESPONSE(access_token=access_token).dict() 
    except Exception as e:
        return send_response(content=e, status_code=status.HTTP_400_BAD_REQUEST, error_tag=True)

@router.post("/logout", status_code=status.HTTP_202_ACCEPTED)
async def logout(response: Response, token: str = Depends(auth_handler.O2AUTH2_SCHEME)):
    try:
        auth_handler.get_current_user(token)
        response.set_cookie(key=ACCESS_TOKEN_KEY, value=None)
        return MESSAGE_RESPONSE(message=LOGOUT_SUCCESS_MESSAGE).dict()
    except Exception as e:
        return send_response(content=e, status_code=status.HTTP_401_UNAUTHORIZED, error_tag=True)

@router.get("/me", status_code=status.HTTP_200_OK)
async def get_user_me(db: Session = Depends(db_connector.get_db), token: str = Depends(auth_handler.O2AUTH2_SCHEME), endpoint = 'all_users'):
    try:
        user = auth_handler.get_current_user(token)
        urls = get_urls(db, user.get('email'))
        return send_response(content=get_user_profile_content(user, urls), status_code=status.HTTP_200_OK)

    except Exception as e:
        return send_response(content=e, status_code=status.HTTP_404_NOT_FOUND, error_tag=True)
