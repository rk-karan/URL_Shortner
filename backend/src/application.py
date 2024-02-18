import uvicorn
import socket
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse

from logger import logger
from utils import send_response
from database_handler.models import Base
from database_handler.crud import get_original_url
from routes.url_routes import routes as url_routes
from routes.user_routes import routes as user_routes
from database_handler.db_connector import db_connector
from exceptions.exceptions import Invalid_Redirection_Request

app = FastAPI()
logger.log("FastAPI app initialized")

try:
    Base.metadata.create_all(bind=db_connector._engine)
    logger.log("Database tables initialized")
except Exception as e:
    logger.log(f"Error initializing database tables: {e}", error_tag=True)


@app.get("/", tags=["test"])
def home():
    response = {
        "message": "Welcome to the URL Shortener API!",
        "hostname": socket.gethostname()
    }
    logger.log(f"Home Page Accessed by{socket.gethostname()}")
    return send_response(content=response, status_code=200)

@app.get("/{short_url}", tags=["redirection"])
def redirect_short_url(short_url: str , db: Session = Depends(db_connector.get_db)):
    try:
        original_url = get_original_url(db , short_url)
        logger.log(f"Redirecting from {short_url} to {original_url}")
        
        if not original_url:
            raise Invalid_Redirection_Request

        return RedirectResponse(url = original_url)
    except Exception as e:
        return send_response(content={e}, status_code=500, error_tag=True)

app.include_router(user_routes.router)
app.include_router(url_routes.router)

if __name__ == "__main__":
    uvicorn.run("application:app", host="127.0.0.1", port=8000 , reload = True) 