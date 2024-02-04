import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Annotated
import json

from logger import logger
import database_handler.models as models
from database_handler.db_connector import db_connector
from database_handler.classes import CREATE_URL_REQUEST, CREATE_URL
from database_handler.crud import add_url

from decorators import log_info

app = FastAPI()
logger.log("FastAPI app initialized")

try:
    models.Base.metadata.create_all(bind=db_connector.engine)
    logger.log("Database tables initialized")
except Exception as e:
    logger.log(f"Error initializing database tables: {e}", error_tag=True)

@log_info
def send_response(content=None, status_code=None):
    try:
        if content is None or status_code is None:
            raise Exception("content and status_code must be present")
        logger.log(f"SUCCESSFUL: Status Code: {status_code} with Response: {content}")
        return JSONResponse(content = content.dict(), status_code=status_code)
    except Exception as e:
        logger.log(f"UNSUCCESSFUL: Sending response failed. status_code: {status_code} response: {content} error: {e}")
        pass



@app.post("/create_short_url", response_model = CREATE_URL)
# @log_info
def create_short_url(create_url_request: CREATE_URL_REQUEST, db: Session = Depends(db_connector.get_db) , endpoint = 'create_short_url'):
    try:
        url_obj = add_url(db , create_url_request)
        return JSONResponse(content=url_obj.dict(), status_code=200)
    except Exception as e:
        logger.log(f"Error creating short url: {e}", error_tag=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")


if __name__ == "__main__":
    uvicorn.run("application:app", host="127.0.0.1", port=8000 , reload = True)