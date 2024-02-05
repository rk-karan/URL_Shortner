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
    access_token : str = Field(default = None, title = "Access Token", description = "The jwt access token for the user")
    token_type : str = Field(default = "bearer", title = "Token Type", description = "The type of the token")