from pydantic import BaseModel, Field, EmailStr
from constants import LOGIN_SUCCESS_MESSAGE

class USER(BaseModel):
    name : str = Field(default = None, title = "Name of the user", description = "The name of the user should be a string")
    email : EmailStr = Field(default = None, title = "Email of the user", description = "The email of the user should be a string")
    
class NEW_USER_REQUEST(USER):
    password : str = Field(default = None, title = "Password of the user", description = "The password of the user should be a string")

class USER_LOGIN(BaseModel):
    email : EmailStr = Field(default = None, title = "Email of the user", description = "The email of the user should be a string")
    password : str = Field(default = None, title = "Password of the user", description = "The password of the user should be a string")
    
class LOGIN_RESPONSE(BaseModel):
    access_token : str = Field(default = None, title = "Token of the user", description = "The token of the user should be a string")
    type : str = Field(default = "Bearer", title = "Type of the token", description = "The type of the token should be a string")
    message : str = Field(default = LOGIN_SUCCESS_MESSAGE, title = "Message of the response", description = "The message of the response should be a string")
    
class USER_PASSWORD_CHANGE(BaseModel):
    new_password : str = Field(default = None, title = "New password of the user", description = "The new password of the user should be a string")
    
class MESSAGE_RESPONSE(BaseModel):
    message : str = Field(default = "SUCCESSFUL", title = "Message of the response", description = "The message of the response should be a string")