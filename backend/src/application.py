import os
import socket
import uvicorn
from typing import Union
from logger import logger
from dotenv import load_dotenv
from utils import send_response
from sqlalchemy.orm import Session
from database_handler.models import Base
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from routes.url_routes import routes as url_routes
from routes.user_routes import routes as user_routes
from database_handler.db_connector import db_connector
from fastapi import FastAPI, Depends, status, BackgroundTasks
from exceptions.exceptions import Invalid_Redirection_Request
from middleware import Information_Middleware, RateLimitingMiddleware
from database_handler.crud import get_original_url, increment_hit_count
from database_handler.schemas import get_homepage_response, Homepage_Response

app = FastAPI()
logger.log("FastAPI app initialized")

# Load Environment Variables
env_path = os.path.join(os.path.dirname(__file__), 'config', '.env')
load_dotenv(dotenv_path=env_path)

ORIGINS = os.getenv("ORIGINS")
MAX_AGE_CORS_CACHE = int(os.getenv("MAX_AGE_CORS_CACHE"))
GZIP_MINIMUM_SIZE = int(os.getenv("GZIP_MINIMUM_SIZE"))

# app.add_middleware(RateLimitingMiddleware)
app.add_middleware(Information_Middleware)
app.add_middleware(CORSMiddleware, allow_origins=ORIGINS, allow_credentials=True, allow_methods=["*"], allow_headers=["*"], max_age=MAX_AGE_CORS_CACHE)
app.add_middleware(GZipMiddleware, minimum_size=GZIP_MINIMUM_SIZE)

try:
    Base.metadata.create_all(bind=db_connector._engine)
    logger.log("Database tables initialized")
except Exception as e:
    logger.log(f"Error initializing database tables: {e}", error_tag=True)

# Routes
@app.get("/", tags=["test"], status_code=status.HTTP_200_OK, summary="Home Page", response_description="Welcome message")
def home(background_tasks: BackgroundTasks) -> Union[Homepage_Response, str]:
    """This function is used to return the welcome message.

    Returns:
        Union[dict, str]: message, hostname
    """
    background_tasks.add_task(logger.log, message=f"Home Page Accessed by {socket.gethostname()}")
    # logger.log(f"Home Page Accessed by {socket.gethostname()}")
    return get_homepage_response(hostname= socket.gethostname())

@app.get("/{short_url}", tags=["redirection"], status_code=status.HTTP_301_MOVED_PERMANENTLY, summary="Redirects to the original URL", response_description="Redirect response to the original URL")
def redirect_short_url(background_tasks: BackgroundTasks, short_url: str , db: Session = Depends(db_connector.get_db)):
    try:
        original_url, _id = get_original_url(db=db , short_url=short_url)
        background_tasks.add_task(logger.log, message=f"Redirecting from {short_url} to {original_url}")
        # logger.log(f"Redirecting from {short_url} to {original_url}")
        
        if not original_url:
            raise Invalid_Redirection_Request

        background_tasks.add_task(increment_hit_count, db=db, entry_id=_id)
        return RedirectResponse(url = original_url)
    except Exception as e:
        return send_response(content={e}, status_code=status.HTTP_400_BAD_REQUEST, error_tag=True)

app.include_router(user_routes.router)
app.include_router(url_routes.router)

if __name__ == "__main__":
    uvicorn.run("application:app", host="127.0.0.1", port=8000 , reload = True) 