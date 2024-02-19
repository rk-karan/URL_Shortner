""" This module contains the schemas for the url operations.
"""
from dataclasses import dataclass
from pydantic import BaseModel, Field
from constants import CREATE_URL_SUCCESS_MESSAGE, EDIT_URL_SUCCESS_MESSAGE

@dataclass
class LONG_URL_CREATE_REQUEST(BaseModel):
    long_url: str = Field(..., title = "Long URL which will be shortened", description = "The long URL should be a string")

@dataclass
class LONG_URL_CREATE_RESPONSE(LONG_URL_CREATE_REQUEST):
    short_url: str
    urls: list = Field(default = [], title = "List of all the URLs", description = "The list of all the URLs should be a list")
    message : str = Field(default = CREATE_URL_SUCCESS_MESSAGE, title = "Message of the response", description = "The message of the response should be a string")

@dataclass    
class LONG_URL_EDIT_REQUEST(BaseModel):
    new_long_url: str = Field(..., title = "New Long URL", description = "The new long URL should be a string")
    old_long_url: str = Field(..., title = "Old Long URL", description = "The old long URL should be a string")
    entry_id: int = Field(..., title = "id of the Long_URL", description = "The id of the long url should be an integer")

@dataclass
class LONG_URL_EDIT_RESPONSE(LONG_URL_EDIT_REQUEST):
    urls: list = Field(default = [], title = "List of all the URLs", description = "The list of all the URLs should be a list")
    message : str = Field(default = EDIT_URL_SUCCESS_MESSAGE, title = "Message of the response", description = "The message of the response should be a string")

@dataclass
class LONG_URL_DELETE_REQUEST(BaseModel):
    entry_id: int = Field(..., title = "id of the Long_URL", description = "The id of the long url should be an integer")
    long_url: str = Field(..., title = "Long URL which will be deleted", description = "The long URL should be a string")