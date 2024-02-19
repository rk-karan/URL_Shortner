import os
import time
import socket
import uvicorn
from typing import Union
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, status
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from logger import logger
from utils import send_response
from database_handler.models import Base
from middleware import X_Process_Time_Middleware
from database_handler.crud import get_original_url
from routes.url_routes import routes as url_routes
<<<<<<< HEAD
from fastapi.middleware.cors import CORSMiddleware
=======
from routes.user_routes import routes as user_routes
from database_handler.db_connector import db_connector
from exceptions.exceptions import Invalid_Redirection_Request
>>>>>>> branch_rohit

app = FastAPI()
logger.log("FastAPI app initialized")

# Load Environment Variables
env_path = os.path.join(os.path.dirname(__file__), 'config', '.env')
load_dotenv(dotenv_path=env_path)

ORIGINS = os.getenv("ORIGINS")

app.add_middleware(X_Process_Time_Middleware)
app.add_middleware(CORSMiddleware, allow_origins=ORIGINS, allow_credentials=True, allow_methods=["*"], allow_headers=["*"],)

try:
    Base.metadata.create_all(bind=db_connector._engine)
    logger.log("Database tables initialized")
except Exception as e:
    logger.log(f"Error initializing database tables: {e}", error_tag=True)

# Routes
@app.get("/", tags=["test"], status_code=status.HTTP_200_OK, summary="Home Page", response_description="Welcome message")
def home() -> Union[dict, str]:
    content = {
        "message": "Welcome to the URL Shortener API!",
        "hostname": socket.gethostname()
    }
    logger.log(f"Home Page Accessed by {socket.gethostname()}")
    return content

@app.get("/{short_url}", tags=["redirection"], status_code=status.HTTP_302_FOUND, summary="Redirects to the original URL", response_description="Redirect response to the original URL")
def redirect_short_url(short_url: str , db: Session = Depends(db_connector.get_db)):
    print(short_url)
    try:
        original_url = get_original_url(db , short_url)
        logger.log(f"Redirecting from {short_url} to {original_url}")
        
        if not original_url:
            raise Invalid_Redirection_Request

        return RedirectResponse(url = original_url)
    except Exception as e:
        return send_response(content={e}, status_code=status.HTTP_400_BAD_REQUEST, error_tag=True)

app.include_router(user_routes.router)
app.include_router(url_routes.router)

if __name__ == "__main__":
    uvicorn.run("application:app", host="127.0.0.1", port=8000 , reload = True) 