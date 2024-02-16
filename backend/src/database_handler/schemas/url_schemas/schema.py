from pydantic import BaseModel, Field
from constants import CREATE_URL_SUCCESS_MESSAGE, EDIT_URL_SUCCESS_MESSAGE

class NEW_URL_REQUEST(BaseModel):
    long_url: str = Field(..., title = "Long URL which will be shortened", description = "The long URL should be a string")

class SHORT_URL_RESPONSE(NEW_URL_REQUEST):
    short_url: str
    message : str = Field(default = CREATE_URL_SUCCESS_MESSAGE, title = "Message of the response", description = "The message of the response should be a string")
    
class EDIT_LONG_URL(BaseModel):
    new_long_url: str = Field(..., title = "New Long URL", description = "The new long URL should be a string")
    old_long_url: str = Field(..., title = "Old Long URL", description = "The old long URL should be a string")
    
class EDIT_LONG_URL_RESPONSE(EDIT_LONG_URL):
    message : str = Field(default = EDIT_URL_SUCCESS_MESSAGE, title = "Message of the response", description = "The message of the response should be a string")