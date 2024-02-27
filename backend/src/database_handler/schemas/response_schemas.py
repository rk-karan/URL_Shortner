from pydantic import BaseModel, Field
from src.database_handler.schemas.user_schemas import User_Information
from src.database_handler.schemas.url_schemas import URLS_Details, _Short_URL, _id
from src.constants import CREATE_URL_SUCCESS_MESSAGE, EDIT_URL_SUCCESS_MESSAGE
from src.constants import  DELETE_URL_SUCCESS_MESSAGE, LOGIN_SUCCESS_MESSAGE, SIGNUP_SUCCESS_MESSAGE, USER_PROFILE_INFORMATION_MESSAGE
from src.constants import HOME_PAGE_MESSAGE, CHANGE_PASSWORD_SUCCESS_MESSAGE, DELETE_USER_SUCCESS_MESSAGE, LOGOUT_SUCCESS_MESSAGE, VALIDATE_TOKEN_SUCCESS_MESSAGE

class _Access_Token(BaseModel):
    access_token : str = Field(default = None, title = "Token of the user", description = "The token of the user should be a string")
    type : str = Field(default = "Bearer", title = "Type of the token", description = "The type of the token should be a string")

class _Expiry(BaseModel):
    expiry: str = Field(default = None, title = "Expiry of the token", description = "The expiry of the token should be a string")

class Payload_Decoded(User_Information, _Expiry):
    pass

class _Message_Response(BaseModel):
    message : str = Field(default = "SUCCESSFUL", title = "Message of the response", description = "The message of the response should be a string")
    
class User_Login_Response(_Access_Token, _Message_Response):
    message : str = Field(default = LOGIN_SUCCESS_MESSAGE)

class User_Create_Response(_Message_Response):
    message : str = Field(default = SIGNUP_SUCCESS_MESSAGE)

class User_Password_Update_Response(_Message_Response):
    message : str = Field(default = CHANGE_PASSWORD_SUCCESS_MESSAGE)

class User_Profile_Response(User_Information, URLS_Details, _Message_Response):
    message : str = Field(default = USER_PROFILE_INFORMATION_MESSAGE)
    urls_count: int = Field(default = 0, title = "Count of the urls", description = "The count of the urls should be an integer")

class User_Delete_Response(_Message_Response):
    message : str = Field(default = DELETE_USER_SUCCESS_MESSAGE)
    
class User_Logout_Response(_Message_Response):
    message : str = Field(default = LOGOUT_SUCCESS_MESSAGE)

class Long_URL_Create_Response(_id, _Short_URL, URLS_Details, _Message_Response):
    message : str = Field(default = CREATE_URL_SUCCESS_MESSAGE)

class Long_URL_Edit_Response(URLS_Details, _Message_Response):
    message : str = Field(default = EDIT_URL_SUCCESS_MESSAGE)

class Long_URL_Delete_Response(URLS_Details, _Message_Response):
    message : str = Field(default = DELETE_URL_SUCCESS_MESSAGE)

class User_Validate_Token_Response(_Message_Response):
    pass
    
class Homepage_Response(_Message_Response):
    message : str = Field(default = HOME_PAGE_MESSAGE)
    hostname : str = Field(default = None, title = "Hostname of the client", description = "The hostname of the server should be a string")

