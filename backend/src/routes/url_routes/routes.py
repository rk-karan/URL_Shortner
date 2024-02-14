from fastapi import APIRouter, Depends, Body, Response, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from database_handler.db_connector import db_connector

from database_handler.schemas import NEW_URL_REQUEST
from utils.send_response import send_response
from logger import logger
from decorators import log_info

from database_handler.crud import create_short_url, get_original_url
from auth import OAuth2PasswordBearerWithCookie
from typing import Annotated
from auth import auth_handler

router = APIRouter(
    prefix="/url",
    tags=["url"],
)

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/user/login")

@router.post("/create_url")
def add_url(new_url: NEW_URL_REQUEST  = Body(default=None) ,  db: Session = Depends(db_connector.get_db), token: str = Depends(oauth2_scheme)):
    try:
        user = auth_handler.get_current_user(token)
        obj = create_short_url(db ,create_url=new_url, email = user.get('email'))
        return obj
    except Exception as e:
        return send_response(content={"error": e}, status_code=500, error_tag=True)

@router.get("/{short_url}")
def redirect_short_url(short_url: str , db: Session = Depends(db_connector.get_db)):
    original_url = get_original_url(db , short_url)
    return RedirectResponse(url = original_url)