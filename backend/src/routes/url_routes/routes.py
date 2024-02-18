import time

from logger import logger
from auth import auth_handler
from utils import send_response

from typing import Union
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Body, status, Response

from utils import get_processing_time
from database_handler.db_connector import db_connector
from constants import DELETE_URL_SUCCESS_MESSAGE, USER_EMAIL_KEY, URLS_KEY, X_PROCESS_TIME_KEY
from database_handler.crud import create_short_url, delete_url, edit_long_url, get_user_profile_content
from database_handler.schemas import MESSAGE_RESPONSE, LONG_URL_DELETE_REQUEST, LONG_URL_CREATE_RESPONSE, LONG_URL_CREATE_REQUEST, LONG_URL_EDIT_REQUEST, LONG_URL_EDIT_RESPONSE

router = APIRouter(
    prefix="/url",
    tags=["url"],
)

@router.post("/create_url", status_code=status.HTTP_201_CREATED)
async def add_url(response: Response, long_url_create_request: LONG_URL_CREATE_REQUEST  = Body(default=None) ,  db: Session = Depends(db_connector.get_db), token: str = Depends(auth_handler._O2AUTH2_SCHEME)) -> Union[LONG_URL_CREATE_RESPONSE, dict]:
    """This api endpoint is used to create new urls. User must be logged in. 

    Args:
        new_url (LONG_URL_CREATE_REQUEST): NEW_URL_REQUEST class. Defaults to Body(default=None).
        db (Session, optional): DB Session. Defaults to Depends(db_connector.get_db).
        token (str, optional): JWT Token. Defaults to Depends(auth_handler._O2AUTH2_SCHEME).

    Returns:
        SHORT_URL_RESPONSE: Shortened url.
    """
    try:
        start_time = time.time()
        user = auth_handler.get_current_user(token)
        logger.log(f"User: {user.get(USER_EMAIL_KEY)}", error_tag=False)
         
        short_url = create_short_url(db, long_url = long_url_create_request.long_url, email = user.get(USER_EMAIL_KEY))
        logger.log(f"SUCCESSFUL: Short URL: {short_url}, created", error_tag=False)
        
        content = get_user_profile_content(db, user)
        
        response.headers[X_PROCESS_TIME_KEY] = get_processing_time(start_time)
        return LONG_URL_CREATE_RESPONSE(short_url=short_url, long_url=long_url_create_request.long_url, urls=content.get(URLS_KEY)).dict()
    except Exception as e:
        return send_response(content=e, status_code=status.HTTP_400_BAD_REQUEST, error_tag=True)
    
@router.put("/edit_url", status_code=status.HTTP_200_OK)
async def edit_url(response: Response, long_url_edit_request: LONG_URL_EDIT_REQUEST, db: Session = Depends(db_connector.get_db), token: str = Depends(auth_handler._O2AUTH2_SCHEME)) -> Union[LONG_URL_EDIT_RESPONSE, dict]:
    """This api endpoint is used to edit created short urls. User must be logged in.

    Args:
        url_to_change (LONG_URL_EDIT_REQUEST): LONG_URL_EDIT_REQUEST class.
        db (Session): DB Session. Defaults to Depends(db_connector.get_db).
        token (str): JWT Token. Defaults to Depends(auth_handler._O2AUTH2_SCHEME).
    """
    try:
        start_time = time.time()
        user = auth_handler.get_current_user(token)
        logger.log(f"User: {user.get(USER_EMAIL_KEY)}", error_tag=False)
        
        edit_long_url(db, new_long_url=long_url_edit_request.new_long_url, old_long_url=long_url_edit_request.old_long_url, entry_id=int(long_url_edit_request.entry_id), email=user.get(USER_EMAIL_KEY))
        logger.log(f"SUCCESSFUL: Short URL Edited", error_tag=False)
        
        content = get_user_profile_content(db, user)
        
        response.headers[X_PROCESS_TIME_KEY] = get_processing_time(start_time)
        return LONG_URL_EDIT_RESPONSE(entry_id=long_url_edit_request.entry_id, new_long_url=long_url_edit_request.new_long_url, old_long_url=long_url_edit_request.old_long_url, urls=content.get(URLS_KEY)).dict()
    except Exception as e:
        return send_response(content=e, status_code=status.HTTP_400_BAD_REQUEST, error_tag=True)
        

@router.put("/delete_url", status_code=status.HTTP_200_OK)
async def delete_long_url(response: Response, long_url_delete_request: LONG_URL_DELETE_REQUEST = Body(default=None), db: Session = Depends(db_connector.get_db), token: str = Depends(auth_handler._O2AUTH2_SCHEME)) -> Union[MESSAGE_RESPONSE, dict]:
    """This api endpoint is used to delete created short urls. User must be logged in.

    Args:
        url_to_delete (NEW_URL_REQUEST, optional): NEW_URL_REQUEST class. Defaults to Body(default=None).
        db (Session, optional): DB Session. Defaults to Depends(db_connector.get_db).
        token (str, optional): JST Token. Defaults to Depends(auth_handler._O2AUTH2_SCHEME).
    """
    try:
        start_time = time.time()
        user = auth_handler.get_current_user(token)
        logger.log(f"User: {user.get(USER_EMAIL_KEY)}", error_tag=False)
        
        delete_url(db , entry_id=int(long_url_delete_request.entry_id),long_url=long_url_delete_request.long_url, email=user.get(USER_EMAIL_KEY))
        logger.log(f"SUCCESSFUL: Short URL Deleted", error_tag=False)
        
        response.headers[X_PROCESS_TIME_KEY] = get_processing_time(start_time)
        return MESSAGE_RESPONSE(message=DELETE_URL_SUCCESS_MESSAGE).dict()
    except Exception as e:
        return send_response(content=e, status_code=status.HTTP_400_BAD_REQUEST, error_tag=True)