from typing import Union
from src.logger import logger
from src.auth.auth_handler import auth_handler
from src.utils import send_response
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from src.database_handler.db_connector import db_connector
from src.exceptions import Invalid_User, User_Already_Exists
from fastapi import APIRouter, Depends, Body, Response, status, BackgroundTasks
from src.database_handler.schemas.response_schemas import User_Profile_Response, User_Validate_Token_Response
from src.constants import ACCESS_TOKEN_KEY, AUTHORIZATION_SCHEME, USER_EMAIL_KEY, USER_NAME_KEY
from src.routes.response_handler import get_user_create_response, get_login_response, get_user_profile_response
from src.database_handler.schemas.response_schemas import User_Delete_Response, User_Password_Update_Response, User_Create_Response, User_Logout_Response, User_Login_Response
from src.database_handler.crud.users_crud import add_user, login_user, get_user_profile_content, delete_user_by_email, change_user_password
from src.database_handler.schemas.user_schemas import User_Create_Request, User_Login_Request, User_Password_Update_Request
from src.routes.response_handler import get_user_password_update_response, get_user_validate_token_response, get_user_delete_response, get_user_logout_response

router = APIRouter(
    prefix="/user",
    tags=["user"],
)

@router.post("/create_user", status_code=status.HTTP_201_CREATED, summary="Create a new user", response_description="User details")
async def create_user(background_tasks: BackgroundTasks, user_create_request: User_Create_Request = Body(default=None), db: Session = Depends(db_connector.get_db)) -> Union[User_Create_Response, str]:
    """This api endpoint adds a new user to the db.

    Args:
        create_user_request (NEW_USER_REQUEST, optional): NEW_URL_REQUEST class. Defaults to Body(default=None).
        db (Session, optional): Defaults to Depends(db_connector.get_db).
    """
    try:
        add_user(db , name=user_create_request.name, email=user_create_request.email, password=user_create_request.password)
        background_tasks.add_task(logger.log, message=f"User: {user_create_request.email}, created")
        # logger.log(f"SUCCESSFUL: User: {user_create_request.email}, created", error_tag=False)
        
        return get_user_create_response()
    except User_Already_Exists as e:
        return send_response(content=e, status_code=status.HTTP_409_CONFLICT, error_tag=True)
    except Exception as e:
        return send_response(content=e, status_code=status.HTTP_400_BAD_REQUEST, error_tag=True)

@router.post("/login", status_code=status.HTTP_200_OK, summary="Login an existing user", response_description="JWT Token")
async def user_login(background_tasks: BackgroundTasks, response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(db_connector.get_db)) -> Union[User_Login_Response, str]:
    """This api endpoint logs in an existing user using JWT Tokens. The token is sent using cookies.

    Args:
        response (Response): Response class instance.
        form_data (OAuth2PasswordRequestForm, optional): OAuth2PasswordRequestForm class instance. Defaults to Depends().
        db (Session, optional): Defaults to Depends(db_connector.get_db).
    """
    try:
        user_login = User_Login_Request(email = form_data.username, password = form_data.password)
        background_tasks.add_task(logger.log, message=f"User: {user_login.email}, logged in")
        # logger.log(f"User: {user_login.email}", error_tag=False)
        
        access_token = login_user(db , email=user_login.email, password=user_login.password)
        background_tasks.add_task(logger.log, message=f"Token: {access_token}, sent")
        # logger.log(f"SUCCESSFUL: User: {user_login.email}, logged in", error_tag=False)
        
        response.set_cookie(key = ACCESS_TOKEN_KEY, value =f"{AUTHORIZATION_SCHEME} {access_token}", httponly = True)
        background_tasks.add_task(logger.log, message=f"Token: {access_token}, sent")
        # logger.log(f"SUCCESSFUL: Token: {access_token}, sent", error_tag=False)
        
        return get_login_response(access_token=access_token)
    except Invalid_User as e:
        return send_response(content=e, status_code=status.HTTP_401_UNAUTHORIZED, error_tag=True)
    except Exception as e:
        return send_response(content=e, status_code=status.HTTP_400_BAD_REQUEST, error_tag=True)

@router.get("/validate_token", status_code=status.HTTP_200_OK, summary="Validate the JWT Token", response_description="Success message")
async def validate_token(background_tasks: BackgroundTasks, token: str = Depends(auth_handler._O2AUTH2_SCHEME)) -> Union[User_Validate_Token_Response, str]:
    try:
        user = auth_handler.get_current_user(token)
        background_tasks.add_task(logger.log, message=f"User: {user.get(USER_EMAIL_KEY)}, token validated")
        # logger.log(f"SUCCESSFUL: User: {user.get(USER_EMAIL_KEY)}, token validated", error_tag=False)
        
        return get_user_validate_token_response()
    except Exception as e:
        return send_response(content=e, status_code=status.HTTP_401_UNAUTHORIZED, error_tag=True)

@router.get("/me", status_code=status.HTTP_200_OK, summary="Get the current user profile. (Details and URLS)", response_description="User details and URLs")
async def get_user_me(background_tasks: BackgroundTasks, db: Session = Depends(db_connector.get_db), token: str = Depends(auth_handler._O2AUTH2_SCHEME)) -> Union[User_Profile_Response, str]:
    """This api endpoint retrieves all the information of the current active user. The user must be logged in.

    Args:
        db (Session, optional): Defaults to Depends(db_connector.get_db).
        token (str, optional): Defaults to Depends(auth_handler._O2AUTH2_SCHEME).
    """
    try:
        user = auth_handler.get_current_user(token)
        background_tasks.add_task(logger.log, message=f"User: {user.get(USER_EMAIL_KEY)}")
        # logger.log(f"User: {user.get(USER_EMAIL_KEY)}", error_tag=False)
        
        content = get_user_profile_content(db, user)
        background_tasks.add_task(logger.log, message=f"User: {user.get(USER_EMAIL_KEY)}, urls retrieved")
        # logger.log(f"SUCCESSFUL: Content: {content}, urls retrieved", error_tag=False)

        return get_user_profile_response(name= user.get(USER_NAME_KEY), email=user.get(USER_EMAIL_KEY), urls=content)
    except Invalid_User as e:
        return send_response(content=e, status_code=status.HTTP_401_UNAUTHORIZED, error_tag=True)
    except Exception as e:
        return send_response(content=e, status_code=status.HTTP_404_NOT_FOUND, error_tag=True)

@router.put("/change_password", status_code=status.HTTP_200_OK, summary="Change the password of the current user", response_description="Success message")
async def change_password(background_tasks: BackgroundTasks, response: Response, user_password_change: User_Password_Update_Request = Body(default=None), db: Session = Depends(db_connector.get_db), token: str = Depends(auth_handler._O2AUTH2_SCHEME)) -> Union[User_Password_Update_Response, str]:
    try:
        user = auth_handler.get_current_user(token)
        background_tasks.add_task(logger.log, message=f"User: {user.get(USER_EMAIL_KEY)}")
        # logger.log(f"User: {user.get(USER_EMAIL_KEY)}", error_tag=False)
        
        change_user_password(db, email=user.get(USER_EMAIL_KEY), new_password=user_password_change.new_password, old_password=user_password_change.old_password)
        background_tasks.add_task(logger.log, message=f"User: {user.get(USER_EMAIL_KEY)}, password changed")
        # logger.log(f"SUCCESSFUL: User: {user.get(USER_EMAIL_KEY)} Password Changed", error_tag=False)
        
        response.set_cookie(key=ACCESS_TOKEN_KEY, value=None)
        background_tasks.add_task(logger.log, message=f"Token: {token}, removed")
        # logger.log(f"SUCCESSFUL: Token: {token}, removed", error_tag=False)

        return get_user_password_update_response()
    except Invalid_User as e:
        return send_response(content=e, status_code=status.HTTP_401_UNAUTHORIZED, error_tag=True)
    except Exception as e:
        return send_response(content=e, status_code=status.HTTP_400_BAD_REQUEST, error_tag=True)

@router.delete("/delete_user", status_code=status.HTTP_200_OK, summary="Delete the current user", response_description="Success message")
async def delete_user(background_tasks: BackgroundTasks, response: Response, db: Session = Depends(db_connector.get_db), token: str = Depends(auth_handler._O2AUTH2_SCHEME)) -> Union[User_Delete_Response, str]:
    """This api endpoint deletes an existing user. The user must be logged in.

    Args:
        response (Response): Response class instance.
        db (Session, optional): Defaults to Depends(db_connector.get_db).
        token (str, optional): Defaults to Depends(auth_handler._O2AUTH2_SCHEME).
    """
    try:
        user = auth_handler.get_current_user(token)
        background_tasks.add_task(logger.log, message=f"User: {user.get(USER_EMAIL_KEY)}")
        # logger.log(f"User: {user.get(USER_EMAIL_KEY)}", error_tag=False)
        
        delete_user_by_email(db, user.get(USER_EMAIL_KEY))
        background_tasks.add_task(logger.log, message=f"User: {user.get(USER_EMAIL_KEY)} Deleted")
        # logger.log(f"SUCCESSFUL: User: {user.get(USER_EMAIL_KEY)} Deleted", error_tag=False)
        
        response.set_cookie(key=ACCESS_TOKEN_KEY, value=None)
        background_tasks.add_task(logger.log, message=f"Token: {token}, removed")
        # logger.log(f"SUCCESSFUL: Token: {token}, removed", error_tag=False)

        return get_user_delete_response()
    except Invalid_User as e:
        return send_response(content=e, status_code=status.HTTP_401_UNAUTHORIZED, error_tag=True)
    except Exception as e:
        return send_response(content=e, status_code=status.HTTP_400_BAD_REQUEST, error_tag=True)

@router.get("/logout", status_code=status.HTTP_200_OK, summary="Logout the current user", response_description="Success message")
async def logout(background_tasks: BackgroundTasks, response: Response, token: str = Depends(auth_handler._O2AUTH2_SCHEME)) -> Union[User_Logout_Response, str]:
    """This api endpoint logs out an existing user. The user must be logged in.

    Args:
        response (Response): Response class instance.
        token (str, optional): JWT Token. Defaults to Depends(auth_handler._O2AUTH2_SCHEME).
    """
    try:
        user = auth_handler.get_current_user(token)
        background_tasks.add_task(logger.log, message=f"User: {user.get(USER_EMAIL_KEY)}")
        # logger.log(f"SUCCESSFUL: User: {user.get(USER_EMAIL_KEY)}, logged out", error_tag=False)
        
        response.set_cookie(key=ACCESS_TOKEN_KEY, value=None)
        background_tasks.add_task(logger.log, message=f"Token: {token}, removed")
        # logger.log(f"SUCCESSFUL: Token: {token}, removed", error_tag=False)
        
        return get_user_logout_response()
    except Invalid_User as e:
        return send_response(content=e, status_code=status.HTTP_401_UNAUTHORIZED, error_tag=True)
    except Exception as e:
        return send_response(content=e, status_code=status.HTTP_400_BAD_REQUEST, error_tag=True)
