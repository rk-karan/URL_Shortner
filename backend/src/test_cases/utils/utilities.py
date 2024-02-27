import string
import random
from src.exceptions import Missing_Params

def get_random_string(length: int=5):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def generate_random_user_with_password():
    return {
        "name": get_random_string(),
        "email": f"{get_random_string()}@{get_random_string()}.com",
        "password": get_random_string()
    }

def generate_login_payload(email: str = None, password: str = None):
    if not email or not password:
        raise Missing_Params
    
    return {
        "username": email,
        "password": password,
        "grant_type": "password",
    }

def generate_user_password_change_payload(old_password: str = None, new_password: str = None):
    if not old_password or not new_password:
        raise Missing_Params
    
    return {
        "old_password": old_password,
        "new_password": new_password
    }

def generate_random_long_url_payload(long_url: str = None):
    return {
        "long_url": long_url if long_url else f"https://{get_random_string()}.com"
    }

def generate_long_url_edit_payload(id: int = None, old_long_url: str = None, new_long_url: str = None):
    if not old_long_url or not new_long_url or not id:
        raise Missing_Params
    
    return {
        "id": id,
        "old_long_url": old_long_url,
        "new_long_url": old_long_url
    }

def generate_long_url_delete_payload(id: int = None, long_url: str = None):
    if not long_url or not id:
        raise Missing_Params
    
    return {
        "id": id,
        "long_url": long_url
    }