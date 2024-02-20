import json
from fastapi.encoders import jsonable_encoder
from ..user_schemas.schema import User_Details
from exceptions.exceptions import Missing_Params
from ..response_schemas.schema import User_Password_Update_Response, Homepage_Response
from constants import JSON_RESPONSE_INDENT, JSON_RESPONSE_SORT_KEYS, JSON_RESPONSE_DEFAULT
from ..response_schemas.schema import User_Login_Response, User_Create_Response, Payload_Decoded, User_Logout_Response
from ..response_schemas.schema import User_Profile_Response, Long_URL_Create_Response, Long_URL_Edit_Response, User_Validate_Token_Response, User_Delete_Response

def make_response(item = None):
    if not item:
        raise Missing_Params
    # return json.dumps(jsonable_encoder(item), sort_keys=JSON_RESPONSE_SORT_KEYS, indent=JSON_RESPONSE_INDENT, default=JSON_RESPONSE_DEFAULT)
    return item.dict()

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

def get_user_create_response(name: str = None, email: str = None):
    if not name or not email:
        raise Missing_Params
    return make_response(User_Create_Response(user= get_user_details(name= name, email= email)))

def get_user_profile_response(name: str = None, email: str = None, urls =[], access_token: str = None):
    if not name or not email or not access_token:
        raise Missing_Params
    return make_response(User_Profile_Response(user= get_user_details(name= name, email= email), urls=urls, urls_count= len(urls), access_token= access_token))

def get_user_password_update_response():
    return make_response(User_Password_Update_Response())

def get_user_validate_token_response():
    return make_response(User_Validate_Token_Response())

def get_user_delete_response():
    return make_response(User_Delete_Response())

def get_user_logout_response():
    return make_response(User_Logout_Response())

def get_long_url_create_response(short_url: str = None, long_url: str = None, urls=[]):
    if not short_url or not long_url:
        raise Missing_Params
    return make_response(Long_URL_Create_Response(short_url= short_url, long_url= long_url, urls=urls))

def get_long_url_edit_response(urls = []):
    if not urls:
        raise Missing_Params
    return make_response(Long_URL_Edit_Response(urls=urls))

def get_long_url_delete_response(urls = []):
    if not urls:
        raise Missing_Params
    return make_response(Long_URL_Edit_Response(urls=urls))

def get_homepage_response(hostname: str = None):
    if not hostname:
        raise Missing_Params
    return make_response(Homepage_Response(hostname= hostname))
    
    