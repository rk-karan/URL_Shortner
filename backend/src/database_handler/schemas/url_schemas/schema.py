""" This module contains the schemas for the url operations.
"""
from typing import List
from datetime import datetime
from pydantic import BaseModel, Field

class _id(BaseModel):
    id: int = Field(default=None, title = "id of the Long_URL", description = "The id of the long url should be an integer")
    
class _Long_URL(BaseModel):
    long_url: str = Field(default=None, title = "Long URL which will be shortened", description = "The long URL should be a string")

class _Short_URL(BaseModel):
    short_url: str = Field(default=None, title = "Short URL", description = "The short URL should be a string")

class _Entry_Id(BaseModel):
    entry_id: int = Field(default=None, title = "id of the Long_URL", description = "The id of the long url should be an integer")

class _New_Long_URL(BaseModel):
    new_long_url: str = Field(default=None, title = "New Long URL", description = "The new long URL should be a string")

class _Old_Long_URL(BaseModel):
    old_long_url: str = Field(default=None, title = "Old Long URL", description = "The old long URL should be a string")

class _Hit_Count(BaseModel):
    hit_count: int = Field(default=None, title = "Hit count of the Long_URL", description = "The hit count of the long url should be an integer")

class _Created_On(BaseModel):
    created_on: datetime = Field(default=None, title = "Created on of the Long_URL", description = "The created on of the long url should be a string")

class _Edited_On(BaseModel):
    edited_on: datetime = Field(default=None, title = "Last edit datetime of the Long_URL", description = "The edited on of the long url should be a string")

class Long_URL_Create_Request(_Long_URL):
    pass

class Long_URL_Edit_Request(_New_Long_URL, _Old_Long_URL, _Entry_Id):
    pass

class Long_URL_Delete_Request(_Long_URL, _Entry_Id):
    pass

class _URL_Details(_id, _Long_URL, _Short_URL, _Hit_Count, _Created_On, _Edited_On):
    pass

class URLS_Details(BaseModel):
    urls: List[_URL_Details] = Field(default = [], title = "Urls of the user", description = "The urls of the user should be a list of dictionaries")