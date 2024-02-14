from pydantic import BaseModel, Field, EmailStr

class USER(BaseModel):
    name : str = Field(default = None, title = "Name of the user", description = "The name of the user should be a string")
    email : EmailStr = Field(default = None, title = "Email of the user", description = "The email of the user should be a string")
    
class NEW_USER_REQUEST(USER):
    password : str = Field(default = None, title = "Password of the user", description = "The password of the user should be a string")

class USER_LOGIN(BaseModel):
    email : EmailStr = Field(default = None, title = "Email of the user", description = "The email of the user should be a string")
    password : str = Field(default = None, title = "Password of the user", description = "The password of the user should be a string")
    
class TOKEN_RESPONSE(BaseModel):
    access_token : str = Field(default = None, title = "Token of the user", description = "The token of the user should be a string")
    type : str = Field(default = "Bearer", title = "Type of the token", description = "The type of the token should be a string")