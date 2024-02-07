from fastapi import APIRouter, Depends, Body, Response, Request
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from database_handler.db_connector import db_connector

from database_handler.schemas import NEW_USER_REQUEST, TOKEN_RESPONSE, USER_LOGIN
from utils.send_response import send_response
from logger import logger
from decorators import log_info
from database_handler.crud.users_crud.crud import add_user, login_user, get_all_users

from auth import auth_handler

router = APIRouter(
    prefix="/user",
    tags=["user"],
)

@router.post("/create_user")
async def create_user(response: Response, create_user_request: NEW_USER_REQUEST = Body(default=None), db: Session = Depends(db_connector.get_db) , endpoint = 'create_user'):
    try:
        add_user(db , create_user_request)
        return send_response(content={"message": "User created successfully"}, status_code=200)
    except Exception as e:
        raise send_response(content={"error": e}, status_code=500, error_tag=True)

@router.post("/login")
async def user_login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(db_connector.get_db) , endpoint = 'login_user'):
    try:
        user_login = USER_LOGIN(email = form_data.username, password = form_data.password)
        access_token = login_user(db , user_login)
        response.set_cookie(key = "access_token" , value =f"Bearer {access_token}", httponly = True)
        return TOKEN_RESPONSE(access_token=access_token).dict()    
    except Exception as e:
        return send_response(content=e, status_code=500, error_tag=True)

@router.post("/logout")
async def logout(response: Response):
    response.set_cookie(key="access_token", value="")  # Expire the cookie
    return send_response(content={"message": "Logged out successfully"}, status_code=200)

@router.get("/all")
async def user_login(db: Session = Depends(db_connector.get_db) , endpoint = 'all_users', payload : dict = Depends(auth_handler.verify_token)):
    return [get_all_users(db), payload]
