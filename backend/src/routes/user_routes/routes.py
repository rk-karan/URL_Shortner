from fastapi import APIRouter, Depends, Body, Response
from sqlalchemy.orm import Session

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

@router.post("/create_user", response_model = TOKEN_RESPONSE)
async def create_user(response: Response, create_user_request: NEW_USER_REQUEST = Body(default=None), db: Session = Depends(db_connector.get_db) , endpoint = 'create_user'):
    try:
        user_obj = add_user(db , create_user_request)
        response.set_cookie(key = "access_token" , value = user_obj.access_token)
        return user_obj
    except Exception as e:
        logger.log(f"Error creating user: {e}", error_tag=True)
        raise send_response(content={"error": e}, status_code=500, error_tag=True)

@router.post("/login", response_model = TOKEN_RESPONSE)
async def user_login(response: Response, user_login: USER_LOGIN = Body(default=None), db: Session = Depends(db_connector.get_db) , endpoint = 'login_user'):
    try:
        user_obj = login_user(db , user_login)
        response.set_cookie(key = "access_token" , value = user_obj.access_token)
        return user_obj
    except Exception as e:
        logger.log(f"Error logging user: {e}", error_tag=True)
        raise send_response(content={"error": e}, status_code=500, error_tag=True)

@router.post("/logout")
async def logout(response: Response):
    response.set_cookie(key="access_token", value="")  # Expire the cookie
    return {"message": "Logged out successfully"}

@router.get("/all")
async def user_login(db: Session = Depends(db_connector.get_db) , endpoint = 'all_users', payload : dict = Depends(auth_handler.verify_token)):
    return [get_all_users(db), payload]
