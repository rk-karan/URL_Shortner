import time
from typing import Union
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, Body, Response, status

from logger import logger
from auth import auth_handler
from exceptions.exceptions import Invalid_User, User_Already_Exists
from utils import send_response, get_processing_time
from database_handler.db_connector import db_connector
from database_handler.crud.users_crud.crud import add_user, login_user, get_user_profile_content, delete_user_by_email, change_user_password
from database_handler.schemas import USER_CREATE_REQUEST, USER_LOGIN_REQUEST, USER_LOGIN_RESPONSE, USER_PASSWORD_UPDATE_REQUEST, MESSAGE_RESPONSE, USER_CREATE_RESPONSE, USER_PROFILE_RESPONSE
from constants import LOGOUT_SUCCESS_MESSAGE, ACCESS_TOKEN_KEY, AUTHORIZATION_SCHEME, DELETE_USER_SUCCESS_MESSAGE, USER_EMAIL_KEY, CHANGE_PASSWORD_SUCCESS_MESSAGE, PAYLOAD_USER_KEY, URLS_KEY, X_PROCESS_TIME_KEY

router = APIRouter(
    prefix="/user",
    tags=["user"],
)

@router.post("/create_user", status_code=status.HTTP_201_CREATED, summary="Create a new user", response_description="User details")
async def create_user(response: Response, user_create_request: USER_CREATE_REQUEST = Body(default=None), db: Session = Depends(db_connector.get_db)) -> Union[USER_CREATE_RESPONSE, dict]:
    """This api endpoint adds a new user to the db.

    Args:
        create_user_request (NEW_USER_REQUEST, optional): NEW_URL_REQUEST class. Defaults to Body(default=None).
        db (Session, optional): Defaults to Depends(db_connector.get_db).
    """
    try:
        add_user(db , name=user_create_request.name, email=user_create_request.email, password=user_create_request.password)
        logger.log(f"SUCCESSFUL: User: {user_create_request.email}, created", error_tag=False)
        
        return USER_CREATE_RESPONSE(name= user_create_request.name, email= user_create_request.email).dict()
    except User_Already_Exists as e:
        return send_response(content=e, status_code=status.HTTP_409_CONFLICT, error_tag=True)
    except Exception as e:
        return send_response(content=e, status_code=status.HTTP_400_BAD_REQUEST, error_tag=True)

@router.post("/login", status_code=status.HTTP_200_OK, summary="Login an existing user", response_description="JWT Token")
async def user_login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(db_connector.get_db)) -> Union[USER_LOGIN_RESPONSE, dict]:
    """This api endpoint logs in an existing user using JWT Tokens. The token is sent using cookies.

    Args:
        response (Response): Response class instance.
        form_data (OAuth2PasswordRequestForm, optional): OAuth2PasswordRequestForm class instance. Defaults to Depends().
        db (Session, optional): Defaults to Depends(db_connector.get_db).
    """
    try:
        user_login = USER_LOGIN_REQUEST(email = form_data.username, password = form_data.password)
        logger.log(f"User: {user_login.email}", error_tag=False)
        
        access_token = login_user(db , email=user_login.email, password=user_login.password)
        logger.log(f"SUCCESSFUL: User: {user_login.email}, logged in", error_tag=False)
        
        response.set_cookie(key = ACCESS_TOKEN_KEY, value =f"{AUTHORIZATION_SCHEME} {access_token}", httponly = True)
        logger.log(f"SUCCESSFUL: Token: {access_token}, sent", error_tag=False)
        
        return USER_LOGIN_RESPONSE(access_token=access_token).dict() 
    except Invalid_User as e:
        return send_response(content=e, status_code=status.HTTP_401_UNAUTHORIZED, error_tag=True)
    except Exception as e:
        return send_response(content=e, status_code=status.HTTP_400_BAD_REQUEST, error_tag=True)

@router.get("/me", status_code=status.HTTP_200_OK, summary="Get the current user profile. (Details and URLS)", response_description="User details and URLs")
async def get_user_me(response: Response, db: Session = Depends(db_connector.get_db), token: str = Depends(auth_handler._O2AUTH2_SCHEME)) -> Union[USER_PROFILE_RESPONSE, dict]:
    """This api endpoint retrieves all the information of the current active user. The user must be logged in.

    Args:
        db (Session, optional): Defaults to Depends(db_connector.get_db).
        token (str, optional): Defaults to Depends(auth_handler._O2AUTH2_SCHEME).
    """
    try:
        user = auth_handler.get_current_user(token)
        logger.log(f"User: {user.get(USER_EMAIL_KEY)}", error_tag=False)
        
        content = get_user_profile_content(db, user)
        logger.log(f"SUCCESSFUL: Content: {content}, urls retrieved", error_tag=False)

        return USER_PROFILE_RESPONSE(user=content.get(PAYLOAD_USER_KEY), urls=content.get(URLS_KEY), urls_count=len(content.get(URLS_KEY)), current_access_token=token).dict()
    except Invalid_User as e:
        return send_response(content=e, status_code=status.HTTP_401_UNAUTHORIZED, error_tag=True)
    except Exception as e:
        return send_response(content=e, status_code=status.HTTP_404_NOT_FOUND, error_tag=True)

@router.put("/change_password", status_code=status.HTTP_200_OK, summary="Change the password of the current user", response_description="Success message")
async def change_password(response: Response, user_password_change: USER_PASSWORD_UPDATE_REQUEST = Body(default=None), db: Session = Depends(db_connector.get_db), token: str = Depends(auth_handler._O2AUTH2_SCHEME)) -> Union[MESSAGE_RESPONSE, dict]:
    try:
        user = auth_handler.get_current_user(token)
        logger.log(f"User: {user.get(USER_EMAIL_KEY)}", error_tag=False)
        
        change_user_password(db, email=user.get(USER_EMAIL_KEY), new_password=user_password_change.new_password, old_password=user_password_change.old_password)
        logger.log(f"SUCCESSFUL: User: {user.get(USER_EMAIL_KEY)} Password Changed", error_tag=False)
        
        response.set_cookie(key=ACCESS_TOKEN_KEY, value=None)
        logger.log(f"SUCCESSFUL: Token: {token}, removed", error_tag=False)

        return MESSAGE_RESPONSE(message=CHANGE_PASSWORD_SUCCESS_MESSAGE).dict()
    except Invalid_User as e:
        return send_response(content=e, status_code=status.HTTP_401_UNAUTHORIZED, error_tag=True)
    except Exception as e:
        return send_response(content=e, status_code=status.HTTP_400_BAD_REQUEST, error_tag=True)

@router.delete("/delete_user", status_code=status.HTTP_200_OK, summary="Delete the current user", response_description="Success message")
async def delete_user(response: Response, db: Session = Depends(db_connector.get_db), token: str = Depends(auth_handler._O2AUTH2_SCHEME)) -> Union[MESSAGE_RESPONSE, dict]:
    """This api endpoint deletes an existing user. The user must be logged in.

    Args:
        response (Response): Response class instance.
        db (Session, optional): Defaults to Depends(db_connector.get_db).
        token (str, optional): Defaults to Depends(auth_handler._O2AUTH2_SCHEME).
    """
    try:
        user = auth_handler.get_current_user(token)
        logger.log(f"User: {user.get(USER_EMAIL_KEY)}", error_tag=False)
        
        delete_user_by_email(db, user.get(USER_EMAIL_KEY))
        logger.log(f"SUCCESSFUL: User: {user.get(USER_EMAIL_KEY)} Deleted", error_tag=False)
        
        response.set_cookie(key=ACCESS_TOKEN_KEY, value=None)
        logger.log(f"SUCCESSFUL: Token: {token}, removed", error_tag=False)

        return MESSAGE_RESPONSE(message=DELETE_USER_SUCCESS_MESSAGE).dict()
    except Invalid_User as e:
        return send_response(content=e, status_code=status.HTTP_401_UNAUTHORIZED, error_tag=True)
    except Exception as e:
        return send_response(content=e, status_code=status.HTTP_400_BAD_REQUEST, error_tag=True)

@router.post("/logout", status_code=status.HTTP_200_OK, summary="Logout the current user", response_description="Success message")
async def logout(response: Response, token: str = Depends(auth_handler._O2AUTH2_SCHEME)) -> Union[MESSAGE_RESPONSE, dict]:
    """This api endpoint logs out an existing user. The user must be logged in.

    Args:
        response (Response): Response class instance.
        token (str, optional): JWT Token. Defaults to Depends(auth_handler._O2AUTH2_SCHEME).
    """
    try:
        start_time = time.time()
        user = auth_handler.get_current_user(token)
        logger.log(f"SUCCESSFUL: User: {user.get(USER_EMAIL_KEY)}, logged out", error_tag=False)
        
        response.set_cookie(key=ACCESS_TOKEN_KEY, value=None)
        logger.log(f"SUCCESSFUL: Token: {token}, removed", error_tag=False)
        
        response.headers[X_PROCESS_TIME_KEY] = get_processing_time(start_time)
        return MESSAGE_RESPONSE(message=LOGOUT_SUCCESS_MESSAGE).dict()
    except Invalid_User as e:
        return send_response(content=e, status_code=status.HTTP_401_UNAUTHORIZED, error_tag=True)
    except Exception as e:
        return send_response(content=e, status_code=status.HTTP_401_UNAUTHORIZED, error_tag=True)
