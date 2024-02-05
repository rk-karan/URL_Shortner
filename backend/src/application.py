import socket
import uvicorn
from fastapi import FastAPI

from logger import logger
from routes import user_routes
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

if __name__ == "__main__":
    uvicorn.run("application:app", host="127.0.0.1", port=8000 , reload = True)