import uvicorn
import socket
from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from logger import logger
from database_handler.models import Base
from database_handler.db_connector import db_connector

from utils.send_response import send_response
from database_handler.schemas import NEW_URL_REQUEST
from database_handler.crud import get_original_url

from decorators import log_info

from routes.user_routes import routes as user_routes
from routes.url_routes import routes as url_routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
logger.log("FastAPI app initialized")

app = FastAPI()

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Only allow requests from localhost:3000
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Allow the specified HTTP methods
    allow_headers=["*"],  # Allow all headers
)

try:
    Base.metadata.create_all(bind=db_connector.engine)
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

@app.get("/{short_url}", tags=["redirection"])
def redirect_short_url(short_url: str , db: Session = Depends(db_connector.get_db)):
    try:
        original_url = get_original_url(db , short_url)
        return RedirectResponse(url = original_url)
    except Exception as e:
        return send_response(content={"message": e}, status_code=500, error_tag=True)

app.include_router(user_routes.router)
app.include_router(url_routes.router)

if __name__ == "__main__":
    uvicorn.run("application:app", host="127.0.0.1", port=8000 , reload = True) 