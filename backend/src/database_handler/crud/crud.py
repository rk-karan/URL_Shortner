from sqlalchemy.orm import Session
from ..models import URLS_Mapping
from ..classes import CREATE_URL, CREATE_URL_REQUEST

def add_url(db: Session , create_url_request: CREATE_URL_REQUEST):
    short_url = ""
    url_obj = CREATE_URL(long_url=create_url_request.long_url, short_url=short_url)
    db_url = URLS_Mapping(url_obj)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return url_obj
