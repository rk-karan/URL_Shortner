from pydantic import BaseModel

class NEW_URL_REQUEST(BaseModel):
    long_url: str

class NEW_URL(NEW_URL_REQUEST):
    short_url: str