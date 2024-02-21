from typing import Union
from logger import logger
from auth import auth_handler
from utils import send_response
from sqlalchemy.orm import Session
from constants import USER_EMAIL_KEY
from exceptions.exceptions import Invalid_User
from database_handler.db_connector import db_connector
from fastapi import APIRouter, Depends, Body, status, BackgroundTasks
from database_handler.crud import create_short_url, delete_url, edit_long_url, get_user_profile_content
from database_handler.schemas import Long_URL_Edit_Request, Long_URL_Edit_Response, Long_URL_Delete_Request
from database_handler.schemas import Long_URL_Create_Request, Long_URL_Create_Response, Long_URL_Delete_Response
from database_handler.schemas import get_long_url_create_response, get_long_url_edit_response, get_long_url_delete_response

router = APIRouter(
    prefix="/url",
    tags=["url"],
)

@router.post("/create_url", status_code=status.HTTP_201_CREATED, summary="Create a new url", response_description="Shortened URL")
async def add_url(background_tasks: BackgroundTasks, long_url_create_request: Long_URL_Create_Request  = Body(default=None) ,  db: Session = Depends(db_connector.get_db), token: str = Depends(auth_handler._O2AUTH2_SCHEME)) -> Union[Long_URL_Create_Response, str]:
    """This api endpoint is used to create new urls. User must be logged in. 

    Args:
        new_url (LONG_URL_CREATE_REQUEST): NEW_URL_REQUEST class. Defaults to Body(default=None).
        db (Session, optional): DB Session. Defaults to Depends(db_connector.get_db).
        token (str, optional): JWT Token. Defaults to Depends(auth_handler._O2AUTH2_SCHEME).

    Returns:
        SHORT_URL_RESPONSE: Shortened url.
    """
    try:
        user = auth_handler.get_current_user(token)
        background_tasks.add_task(logger.log, message=f"User: {user.get(USER_EMAIL_KEY)}")
        # logger.log(f"User: {user.get(USER_EMAIL_KEY)}", error_tag=False)
         
        short_url = create_short_url(db, long_url = long_url_create_request.long_url, email = user.get(USER_EMAIL_KEY))
        background_tasks.add_task(logger.log, message=f"SUCCESSFUL: Short URL: {short_url}, created")
        # logger.log(f"SUCCESSFUL: Short URL: {short_url}, created", error_tag=False)
        
        content = get_user_profile_content(db, user)

        return get_long_url_create_response(short_url=short_url, long_url=long_url_create_request.long_url, urls=content)
    except Invalid_User as e:
        return send_response(content=e, status_code=status.HTTP_401_UNAUTHORIZED, error_tag=True)
    except Exception as e:
        return send_response(content=e, status_code=status.HTTP_400_BAD_REQUEST, error_tag=True)
    
@router.put("/edit_url", status_code=status.HTTP_200_OK, summary="Edit a url", response_description="Success message")
async def edit_url(background_tasks: BackgroundTasks, long_url_edit_request: Long_URL_Edit_Request, db: Session = Depends(db_connector.get_db), token: str = Depends(auth_handler._O2AUTH2_SCHEME)) -> Union[Long_URL_Edit_Response, str]:
    """This api endpoint is used to edit created short urls. User must be logged in.

    Args:
        url_to_change (LONG_URL_EDIT_REQUEST): LONG_URL_EDIT_REQUEST class.
        db (Session): DB Session. Defaults to Depends(db_connector.get_db).
        token (str): JWT Token. Defaults to Depends(auth_handler._O2AUTH2_SCHEME).
    """
    try:
        user = auth_handler.get_current_user(token)
        background_tasks.add_task(logger.log, message=f"User: {user.get(USER_EMAIL_KEY)}")
        # logger.log(f"User: {user.get(USER_EMAIL_KEY)}", error_tag=False)
        
        edit_long_url(db, new_long_url=long_url_edit_request.new_long_url, old_long_url=long_url_edit_request.old_long_url, entry_id=int(long_url_edit_request.id), email=user.get(USER_EMAIL_KEY))
        background_tasks.add_task(logger.log, message=f"SUCCESSFUL: Short URL Edited")
        # logger.log(f"SUCCESSFUL: Short URL Edited", error_tag=False)
        
        content = get_user_profile_content(db, user)

        return get_long_url_edit_response(urls=content)
    except Invalid_User as e:
        return send_response(content=e, status_code=status.HTTP_401_UNAUTHORIZED, error_tag=True)
    except Exception as e:
        return send_response(content=e, status_code=status.HTTP_400_BAD_REQUEST, error_tag=True)

@router.put("/delete_url", status_code=status.HTTP_200_OK, summary="Delete a url", response_description="Success message")
async def delete_long_url(background_tasks: BackgroundTasks, long_url_delete_request: Long_URL_Delete_Request = Body(default=None), db: Session = Depends(db_connector.get_db), token: str = Depends(auth_handler._O2AUTH2_SCHEME)) -> Union[Long_URL_Delete_Response, str]:
    """This api endpoint is used to delete created short urls. User must be logged in.

    Args:
        url_to_delete (NEW_URL_REQUEST, optional): NEW_URL_REQUEST class. Defaults to Body(default=None).
        db (Session, optional): DB Session. Defaults to Depends(db_connector.get_db).
        token (str, optional): JST Token. Defaults to Depends(auth_handler._O2AUTH2_SCHEME).
    """
    try:
        user = auth_handler.get_current_user(token)
        background_tasks.add_task(logger.log, message=f"User: {user.get(USER_EMAIL_KEY)}")
        # logger.log(f"User: {user.get(USER_EMAIL_KEY)}", error_tag=False)
        
        delete_url(db , entry_id=int(long_url_delete_request.id),long_url=long_url_delete_request.long_url, email=user.get(USER_EMAIL_KEY))
        background_tasks.add_task(logger.log, message=f"SUCCESSFUL: Short URL Deleted")
        # logger.log(f"SUCCESSFUL: Short URL Deleted", error_tag=False)
        
        content = get_user_profile_content(db, user)
        background_tasks.add_task(logger.log, message=f"Sending content: {content}")
        
        return get_long_url_delete_response(urls=content)
    except Invalid_User as e:
        return send_response(content=e, status_code=status.HTTP_401_UNAUTHORIZED, error_tag=True)
    except Exception as e:
        return send_response(content=e, status_code=status.HTTP_400_BAD_REQUEST, error_tag=True)