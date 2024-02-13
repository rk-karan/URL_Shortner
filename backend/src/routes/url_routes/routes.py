from fastapi import APIRouter, Depends, Body
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from database_handler.db_connector import db_connector

from database_handler.schemas import NEW_URL_REQUEST
from utils.send_response import send_response
from logger import logger
from decorators import log_info

from database_handler.crud import create_short_url, get_original_url, delete_url
from auth import auth_handler

router = APIRouter(
    prefix="/url",
    tags=["url"],
)

@router.post("/create_url")
def add_url(new_url: NEW_URL_REQUEST  = Body(default=None) ,  db: Session = Depends(db_connector.get_db), token: str = Depends(auth_handler.O2AUTH2_SCHEME)):
    try:
        user = auth_handler.get_current_user(token)
        obj = create_short_url(db ,create_url=new_url, email = user.get('email'))
        return obj
    except Exception as e:
        return send_response(content={"error": e}, status_code=500, error_tag=True)

@router.delete("/delete_url")
def delete_long_url(url_to_delete: NEW_URL_REQUEST = Body(default=None), db: Session = Depends(db_connector.get_db), token: str = Depends(auth_handler.O2AUTH2_SCHEME)):
    try:
        user = auth_handler.get_current_user(token)
        delete_url(db , long_url=url_to_delete.long_url ,email=user.get('email'))
        
        content = {
            "message": "URL deleted successfully"
        }
        return send_response(content=content, status_code=200)
    except Exception as e:
        return send_response(content={"error": e}, status_code=500, error_tag=True)

@router.get("/{short_url}")
def redirect_short_url(short_url: str , db: Session = Depends(db_connector.get_db)):
    original_url = get_original_url(db , short_url)
    return RedirectResponse(url = original_url)