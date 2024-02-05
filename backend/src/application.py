import uvicorn
import socket
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Annotated
import json

from logger import logger
import database_handler.models.user_models.models as user_models
import database_handler.models.url_models.models as url_models
from database_handler.db_connector import db_connector

from utils.send_response import send_response

from decorators import log_info

from routes.user_routes import routes as user_routes

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

# @app.post("/create_short_url", response_model = CREATE_URL)
# # @log_info
# def create_short_url(create_url_request: CREATE_URL_REQUEST, db: Session = Depends(db_connector.get_db) , endpoint = 'create_short_url'):
#     try:
#         url_obj = add_url(db , create_url_request)
#         return send_response(content=url_obj, status_code=200)
#     except Exception as e:
#         logger.log(f"Error creating short url: {e}", error_tag=True)
#         raise send_response(content={"error": e}, status_code=500, error_tag=True)


if __name__ == "__main__":
    uvicorn.run("application:app", host="127.0.0.1", port=8000 , reload = True)