""" This module contains the schemas for the user operations.
"""
from pydantic import BaseModel, Field, EmailStr

class _User_Name(BaseModel):
    name: str = Field(default = None, title = "Name of the user", description = "The name of the user should be a string")

class _User_Email(BaseModel):
    email: EmailStr = Field(default = None, title = "Email of the user", description = "The email of the user should be a string")

class _User_Password(BaseModel):
    password: str = Field(default = None, title = "Password of the user", description = "The password of the user should be a string")

class _User_Old_Password(BaseModel):
    old_password: str = Field(default = None, title = "Old password of the user", description = "The old password of the user should be a string")

class _User_New_Password(BaseModel):
    new_password: str = Field(default = None, title = "New password of the user", description = "The new password of the user should be a string")

class User_Details(_User_Name, _User_Email):
    pass

class User_Create_Request(User_Details, _User_Password):
    pass

class User_Login_Request(_User_Email, _User_Password):
    pass

class User_Password_Update_Request(_User_Old_Password, _User_New_Password):
    pass

class User_Information(BaseModel):
    user: User_Details = Field(default = None, title = "User details with name and email", description = "The user details should be a dictionary")