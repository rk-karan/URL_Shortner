from fastapi import APIRouter, Depends, Body, status
from sqlalchemy.orm import Session

from database_handler.db_connector import db_connector

from database_handler.schemas import NEW_URL_REQUEST
from utils.send_response import send_response
from logger import logger
from decorators import log_info

from database_handler.crud import create_short_url, delete_url
from auth import auth_handler

from database_handler.schemas import MESSAGE_RESPONSE, SHORT_URL_RESPONSE

from constants import DELETE_URL_SUCCESS_MESSAGE

router = APIRouter(
    prefix="/url",
    tags=["url"],
)

@router.post("/create_url")
def add_url(new_url: NEW_URL_REQUEST  = Body(default=None) ,  db: Session = Depends(db_connector.get_db), token: str = Depends(auth_handler.O2AUTH2_SCHEME)):
    try:
        user = auth_handler.get_current_user(token)
        short_url = create_short_url(db, create_url = new_url, email = user.get('email'))
        
        return SHORT_URL_RESPONSE(short_url=short_url).dict()
    except Exception as e:
        return send_response(content=e, status_code=status.HTTP_400_BAD_REQUEST, error_tag=True)

@router.put("/delete_url")
def delete_long_url(url_to_delete: NEW_URL_REQUEST = Body(default=None), db: Session = Depends(db_connector.get_db), token: str = Depends(auth_handler.O2AUTH2_SCHEME)):
    try:
        user = auth_handler.get_current_user(token)
        delete_url(db , long_url=url_to_delete.long_url ,email=user.get('email'))
        return MESSAGE_RESPONSE(message=DELETE_URL_SUCCESS_MESSAGE).dict()
    except Exception as e:
        return send_response(content=e, status_code=status.HTTP_400_BAD_REQUEST, error_tag=True)