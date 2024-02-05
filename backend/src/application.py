import socket
from fastapi import FastAPI, Depends, HTTPException, Body, Request, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import Annotated
import json

from logger import logger
import database_handler.models.user_models.models as user_models
import database_handler.models.url_models.models as url_models
from database_handler.db_connector import db_connector

from utils.send_response import send_response
from database_handler.schemas import NEW_URL_REQUEST
from database_handler.crud import create_short_url, get_original_url

from decorators import log_info
from utils.send_response import send_response
from database_handler.models import url_models
from database_handler.models import user_models
from database_handler.db_connector import db_connector

app = FastAPI()
logger.log("FastAPI app initialized")

try:
    user_models.Base.metadata.create_all(bind=db_connector.engine)
    url_models.Base.metadata.create_all(bind=db_connector.engine)
    logger.log("Database tables initialized")
except Exception as e:
    logger.log(f"Error initializing database tables: {e}", error_tag=True)


@app.get("/", tags=["test"])
@log_info
def home():
    response = {
        "message": "Welcome to the URL Shortener API!",
        "hostname": socket.gethostname()
    }
    return send_response(content=response, status_code=200)

app.include_router(user_routes.router)

@app.post("/shortUrl")
def add_url( request: Request, create_url: NEW_URL_REQUEST  = Body(default=None) ,  db: Session = Depends(db_connector.get_db)):
    hostname = request.url.hostname
    obj = create_short_url(db , create_url, hostname)
    return obj

@app.get("/{short_url}")
def redirect_short_url(response: Response, short_url: str , db: Session = Depends(db_connector.get_db)):
    original_url = get_original_url(db , short_url)
    response = RedirectResponse(url = original_url)
    return response
if __name__ == "__main__":
    uvicorn.run("application:app", host="127.0.0.1", port=8000 , reload = True)