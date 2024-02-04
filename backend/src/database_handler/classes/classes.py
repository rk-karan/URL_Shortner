from pydantic import BaseModel

class CREATE_URL(BaseModel):
    long_url: str
    short_url: str