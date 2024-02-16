from logger import logger
from auth import auth_handler
from decorators import log_info

from sqlalchemy.orm import Session

from utils.send_response import send_response
from constants import DELETE_URL_SUCCESS_MESSAGE, USER_EMAIL_KEY
from database_handler.schemas import NEW_URL_REQUEST

from fastapi import APIRouter, Depends, Body, status

from database_handler.db_connector import db_connector
from database_handler.crud import create_short_url, delete_url
from database_handler.schemas import MESSAGE_RESPONSE, SHORT_URL_RESPONSE



router = APIRouter(
    prefix="/url",
    tags=["url"],
)

@router.post("/create_url", status_code=status.HTTP_201_CREATED)
async def add_url(new_url: NEW_URL_REQUEST  = Body(default=None) ,  db: Session = Depends(db_connector.get_db), token: str = Depends(auth_handler._O2AUTH2_SCHEME)):
    """This api endpoint is used to create new urls. User must be logged in. 

    Args:
        new_url (NEW_URL_REQUEST, optional): NEW_URL_REQUEST class. Defaults to Body(default=None).
        db (Session, optional): DB Session. Defaults to Depends(db_connector.get_db).
        token (str, optional): JWT Token. Defaults to Depends(auth_handler._O2AUTH2_SCHEME).

    Returns:
        SHORT_URL_RESPONSE: Shortened url.
    """
    try:
        user = auth_handler.get_current_user(token)
        short_url = create_short_url(db, create_url = new_url, email = user.get(USER_EMAIL_KEY))
        
        return SHORT_URL_RESPONSE(short_url=short_url, long_url=new_url.long_url).dict()
    except Exception as e:
        return send_response(content=e, status_code=status.HTTP_400_BAD_REQUEST, error_tag=True)

@router.put("/delete_url", status_code=status.HTTP_200_OK)
async def delete_long_url(url_to_delete: NEW_URL_REQUEST = Body(default=None), db: Session = Depends(db_connector.get_db), token: str = Depends(auth_handler._O2AUTH2_SCHEME)):
    """This api endpoint is used to delete created short urls. User must be logged in.

    Args:
        url_to_delete (NEW_URL_REQUEST, optional): NEW_URL_REQUEST class. Defaults to Body(default=None).
        db (Session, optional): DB Session. Defaults to Depends(db_connector.get_db).
        token (str, optional): JST Token. Defaults to Depends(auth_handler._O2AUTH2_SCHEME).

    Returns:
        _type_: _description_
    """
    try:
        user = auth_handler.get_current_user(token)
        delete_url(db , long_url=url_to_delete.long_url ,email=user.get(USER_EMAIL_KEY))
        return MESSAGE_RESPONSE(message=DELETE_URL_SUCCESS_MESSAGE).dict()
    except Exception as e:
        return send_response(content=e, status_code=status.HTTP_400_BAD_REQUEST, error_tag=True)