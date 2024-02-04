from pydantic import BaseModel

class CREATE_URL_REQUEST(BaseModel):
    long_url: str
class CREATE_URL(CREATE_URL_REQUEST):
    short_url: str
    # class Config:
    #     orm_mode = True