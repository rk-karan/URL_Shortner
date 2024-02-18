""" This module contains the schemas for the user operations.
"""
from pydantic import BaseModel, Field, EmailStr
from constants import LOGIN_SUCCESS_MESSAGE, SIGNUP_SUCCESS_MESSAGE

class USER(BaseModel):
    name : str = Field(default = None, title = "Name of the user", description = "The name of the user should be a string")
    email : EmailStr = Field(default = None, title = "Email of the user", description = "The email of the user should be a string")
    
class USER_CREATE_REQUEST(USER):
    password : str = Field(default = None, title = "Password of the user", description = "The password of the user should be a string")

class USER_CREATE_RESPONSE(USER):
    message : str = Field(default = SIGNUP_SUCCESS_MESSAGE, title = "Message of the response", description = "The message of the response should be a string")

class USER_LOGIN_REQUEST(BaseModel):
    email : EmailStr = Field(default = None, title = "Email of the user", description = "The email of the user should be a string")
    password : str = Field(default = None, title = "Password of the user", description = "The password of the user should be a string")
    
class USER_LOGIN_RESPONSE(BaseModel):
    access_token : str = Field(default = None, title = "Token of the user", description = "The token of the user should be a string")
    type : str = Field(default = "Bearer", title = "Type of the token", description = "The type of the token should be a string")
    message : str = Field(default = LOGIN_SUCCESS_MESSAGE, title = "Message of the response", description = "The message of the response should be a string")
    
class USER_PASSWORD_UPDATE_REQUEST(BaseModel):
    old_password : str = Field(default = None, title = "Old password of the user", description = "The old password of the user should be a string")
    new_password : str = Field(default = None, title = "New password of the user", description = "The new password of the user should be a string")

class USER_PROFILE_RESPONSE(BaseModel):
    user: USER = Field(default = None, title = "User details", description = "The user details should be a dictionary")
    urls: list = Field(default = [], title = "Urls of the user", description = "The urls of the user should be a list of dictionaries")
    urls_count: int = Field(default = 0, title = "Count of the urls", description = "The count of the urls should be an integer")
    current_access_token: str = Field(default = None, title = "Current access token", description = "The current access token should be a string") 
    
class MESSAGE_RESPONSE(BaseModel):
    message : str = Field(default = "SUCCESSFUL", title = "Message of the response", description = "The message of the response should be a string")