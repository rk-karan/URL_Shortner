from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session

from database_handler.db_connector import db_connector

from database_handler.schemas import NEW_USER_REQUEST, TOKEN_RESPONSE
from utils.send_response import send_response
from logger import logger
from decorators import log_info

from database_handler.crud.users_crud.crud import add_user

from auth import JWT_Handler as auth_handler

router = APIRouter(
    prefix="/user",
    tags=["user"],
)

@router.post("/create_user", response_model = TOKEN_RESPONSE)
async def create_user(create_user_request: NEW_USER_REQUEST = Body(default=None), db: Session = Depends(db_connector.get_db) , endpoint = 'create_user'):
    try:
        user_obj = add_user(db , create_user_request)
        return user_obj
    except Exception as e:
        logger.log(f"Error creating user: {e}", error_tag=True)
        raise send_response(content={"error": e}, status_code=500, error_tag=True)