from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from logger import logger
import database_handler.models as models
from database_handler.db_connector import db_connector
from database_handler.classes import CREATE_URL
from database_handler.models import URLS_Mapping

from decorators import log_info

app = FastAPI()
logger.log("FastAPI app initialized")

try:
    models.Base.metadata.create_all(bind=db_connector.engine)
    logger.log("Database tables initialized")
except Exception as e:
    logger.log(f"Error initializing database tables: {e}", error_tag=True)

db_dependency = Annotated[Session, Depends(db_connector.get_db)]

@app.post("/create_short_url")
@log_info
async def create_short_url(create_url: CREATE_URL, db: db_dependency):
    try:
        add_url = URLS_Mapping(long_url=create_url.long_url, short_url=create_url.short_url)
        db.add(add_url)
        db.commit()
        db.refresh(add_url)
        
        return {"green":"green"}
    except Exception as e:
        logger.log(f"Error creating short url: {e}", error_tag=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")


