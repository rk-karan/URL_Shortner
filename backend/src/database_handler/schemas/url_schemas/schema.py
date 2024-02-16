from pydantic import BaseModel, Field
from constants import CREATE_URL_SUCCESS_MESSAGE

class NEW_URL_REQUEST(BaseModel):
    long_url: str = Field(..., title = "Long URL which will be shortened", description = "The long URL should be a string")

class SHORT_URL_RESPONSE(NEW_URL_REQUEST):
    short_url: str
    message : str = Field(default = CREATE_URL_SUCCESS_MESSAGE, title = "Message of the response", description = "The message of the response should be a string")