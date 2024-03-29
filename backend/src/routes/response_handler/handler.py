import json
from fastapi.encoders import jsonable_encoder
from src.database_handler.schemas.user_schemas import User_Details
from src.exceptions import Missing_Params
from src.database_handler.schemas.response_schemas import User_Password_Update_Response, Homepage_Response
from src.constants import JSON_RESPONSE_INDENT, JSON_RESPONSE_SORT_KEYS, JSON_RESPONSE_DEFAULT
from src.database_handler.schemas.response_schemas import User_Login_Response, User_Create_Response, Payload_Decoded, User_Logout_Response, Long_URL_Delete_Response
from src.database_handler.schemas.response_schemas import User_Profile_Response, Long_URL_Create_Response, Long_URL_Edit_Response, User_Validate_Token_Response, User_Delete_Response

def make_response(item = None):
    if not item:
        raise Missing_Params
    return json.dumps(jsonable_encoder(item), sort_keys=JSON_RESPONSE_SORT_KEYS, indent=JSON_RESPONSE_INDENT, default=JSON_RESPONSE_DEFAULT)
    # return item.dict()

def get_user_details(name: str = None, email: str = None):
    if not name or not email:
        raise Missing_Params
    return User_Details(name = name, email = email).dict()

def get_payload_decoded(name: str = None, email: str = None):
    if not name or not email:
        raise Missing_Params
    return Payload_Decoded(user= get_user_details(name= name, email= email)).dict()

def get_login_response(access_token: str = None):
    if not access_token:
        raise Missing_Params
    return make_response(User_Login_Response(access_token= access_token))

def get_user_create_response():
    return make_response(User_Create_Response())

def get_user_profile_response(name: str = None, email: str = None, urls =[]):
    if not name or not email:
        raise Missing_Params
    return make_response(User_Profile_Response(user= get_user_details(name= name, email= email), urls=urls, urls_count= len(urls)))

def get_user_password_update_response():
    return make_response(User_Password_Update_Response())

def get_user_validate_token_response():
    return make_response(User_Validate_Token_Response())

def get_user_delete_response():
    return make_response(User_Delete_Response())

def get_user_logout_response():
    return make_response(User_Logout_Response())

def get_long_url_create_response(id:int = None, short_url: str = None, long_url: str = None, urls=[]):
    if not short_url or not long_url or not id:
        raise Missing_Params
    return make_response(Long_URL_Create_Response(id=id, short_url= short_url, long_url= long_url, urls=urls))

def get_long_url_edit_response(urls = []):
    return make_response(Long_URL_Edit_Response(urls=urls))

def get_long_url_delete_response(urls = []):
    return make_response(Long_URL_Delete_Response(urls=urls))

def get_homepage_response(hostname: str = None):
    if not hostname:
        raise Missing_Params
    return make_response(Homepage_Response(hostname= hostname))
    
    