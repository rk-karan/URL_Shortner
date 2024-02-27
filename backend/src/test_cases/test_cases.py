from fastapi.testclient import TestClient
import socket
import json
from fastapi import status
from src.routes.response_handler import get_homepage_response, get_user_create_response, get_user_delete_response, get_user_logout_response, get_user_password_update_response, get_user_validate_token_response
from src.exceptions import Missing_Params
from src.test_cases.utils import generate_random_user_with_password, generate_login_payload, get_random_string, generate_user_password_change_payload, generate_random_long_url_payload, generate_long_url_edit_payload, generate_long_url_delete_payload
from src.constants import USER_EMAIL_KEY, USER_PASSWORD_KEY,  SHORT_URL_KEY, LONG_URL_KEY, ID_KEY

USER_LOGIN_URL = "/user/login"
USER_CREATE_URL = "/user/create_user"
USER_LOGOUT_URL = "/user/logout"
USER_CHANGE_PASSWORD_URL = "/user/change_password"
USER_VALIDATE_TOKEN_URL = "/user/validate_token"
USER_DELETE_URL = "/user/delete_user"

SHORT_URL_CREATE_URL = "/url/create_url"
LONG_URL_EDIT_URL = "/url/edit_url"
LONG_URL_DELETE_URL = "/url/delete_url"

ORIGINAL_URL_GET_URL = "/"

class Test_Case_Library():
    def __init__(self, client: TestClient = None):
        
        if not client:
            raise Missing_Params
        
        self._client = client
        
        self._HOME_URL = "/"
        
        self._USER_VALIDATE_TOKEN_URL = USER_VALIDATE_TOKEN_URL
        self._USER_CREATE_URL = USER_CREATE_URL
        self._USER_LOGIN_URL = USER_LOGIN_URL
        self._USER_LOGOUT_URL = USER_LOGOUT_URL
        self._USER_CHANGE_PASSWORD_URL = USER_CHANGE_PASSWORD_URL
        self._USER_DELETE_URL = USER_DELETE_URL
        
        self._SHORT_URL_CREATE_URL = SHORT_URL_CREATE_URL
        self._LONG_URL_EDIT_URL = LONG_URL_EDIT_URL
        self._LONG_URL_DELETE_URL = LONG_URL_DELETE_URL
            
    def execute_home(self):
        try:
            return self._client.get(self._HOME_URL)
        except Exception as e:
            raise e
        
    def execute_user_token_validation(self):
        try:
            return self._client.get(self._USER_VALIDATE_TOKEN_URL)
        except Exception as e:
            raise e
    
    def execute_user_create(self, user: dict = None):
        try:
            if not user:
                raise Missing_Params
            
            return self._client.post(self._USER_CREATE_URL, json=user, headers={"Content-Type": "application/json"})
        except Exception as e:
            raise e
    
    def execute_user_login(self, user: dict = None):
        try:
            if not user:
                raise Missing_Params
            return self._client.post(self._USER_LOGIN_URL, data=generate_login_payload(email=user.get(USER_EMAIL_KEY), password=user.get(USER_PASSWORD_KEY)), headers={"Content-Type": "application/x-www-form-urlencoded"})
        except Exception as e:
            raise e
    
    def execute_user_logout(self):
        try:
            return self._client.get(self._USER_LOGOUT_URL)
        except Exception as e:
            raise e
    
    def execute_user_delete(self):
        try:
            return self._client.delete(self._USER_DELETE_URL)
        except Exception as e:
            raise e
    
    def execute_user_change_password(self, user: dict = None, new_password: str = None):
        try:
            if not user or not new_password:
                raise Missing_Params
            
            return self._client.put(self._USER_CHANGE_PASSWORD_URL, json=generate_user_password_change_payload(old_password=user.get(USER_PASSWORD_KEY), new_password=new_password), headers={"Content-Type": "application/json"})
        except Exception as e:
            raise e

    def execute_short_url_create(self, long_url: str = None):
        try:
            if not long_url:
                raise Missing_Params
            
            return self._client.post(self._SHORT_URL_CREATE_URL, json=generate_random_long_url_payload(long_url=long_url), headers={"Content-Type": "application/json"})
        except Exception as e:
            raise e
    
    def execute_long_url_edit(self, id: int = None, old_long_url: str = None, new_long_url: str = None):
        try:
            if not id or not old_long_url or not new_long_url:
                raise Missing_Params
            return self._client.put(self._LONG_URL_EDIT_URL, json=generate_long_url_edit_payload(id=id, old_long_url=old_long_url, new_long_url=new_long_url), headers={"Content-Type": "application/json"})
        except Exception as e:
            raise e
    
    def execute_long_url_delete(self, id:int = None, long_url: str = None):
        try:
            if not long_url or not id:
                raise Missing_Params
            return self._client.put(self._LONG_URL_DELETE_URL, json=generate_long_url_delete_payload(id=id, long_url=long_url), headers={"Content-Type": "application/json"})
        except Exception as e:
            raise e
    
    def execute_get_original_url(self, short_url: str = None):
        try:
            if not short_url:
                raise Missing_Params
            result_string = short_url.replace("http://localhost:8000", "")
            return self._client.get(result_string)
        except Exception as e:
            raise e
    
    def assert_validate_token_success(self):
        try:
            response = self.execute_user_token_validation()
            
            assert response.status_code == status.HTTP_200_OK
            assert response.json() == get_user_validate_token_response()
        except Exception as e:
            raise e

    def assert_validate_token_failure(self):
        try:
            response = self.execute_user_token_validation()
            
            assert response.status_code == status.HTTP_401_UNAUTHORIZED
        except Exception as e:
            raise e
    
    def assert_create_user_success(self, user: dict = None):
        try:
            if not user:
                raise Missing_Params
            
            response = self.execute_user_create(user=user)
            
            assert response.status_code == status.HTTP_201_CREATED
            assert response.json() == get_user_create_response()
        except Exception as e:
            raise e

    def assert_login_success(self, user: dict = None):
        try:
            if not user:
                raise Missing_Params
            
            response = self.execute_user_login(user=user)
            assert response.status_code == status.HTTP_200_OK
            assert response.cookies["access_token"]
        
            self.assert_validate_token_success()
        except Exception as e:
            raise e

    def assert_login_failure(self, user: dict = None):
        try:
            if not user:
                raise Missing_Params
            response = self.execute_user_login(user=user)
            assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
            self.assert_validate_token_failure()
        except Exception as e:
            raise e

    def assert_logout_success(self):
        try:
            response = self.execute_user_logout()
            
            assert response.status_code == status.HTTP_200_OK
            assert response.json() == get_user_logout_response()
        
            self.assert_validate_token_failure()
        except Exception as e:
            raise e
    
    def assert_get_original_url_success(self, short_url: str = None, long_url: str = None):
        try:
            if not short_url or not long_url:
                raise Missing_Params
            response = self.execute_get_original_url(short_url=short_url)
            assert response.status_code == status.HTTP_200_OK
        except Exception as e:
            raise e
    
    def assert_get_original_url_failure(self, short_url: str = None):
        try:
            if not short_url:
                raise Missing_Params
            response = self.execute_get_original_url(short_url=short_url)
            assert response.status_code == status.HTTP_404_NOT_FOUND
        except Exception as e:
            raise e

    def home_api_test(self):
        response = self.execute_home()
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == get_homepage_response(hostname= socket.gethostname())

    def create_user_api_test(self):
        user = generate_random_user_with_password()

        self.assert_create_user_success(user=user)
        self.assert_login_success(user=user)

    def logout_user_api_test(self):
        user = generate_random_user_with_password()
    
        self.assert_create_user_success(user=user)
        self.assert_login_success(user=user)
        self.assert_logout_success()

    def delete_user_api_test(self):
        user = generate_random_user_with_password()
    
        self.assert_create_user_success(user=user)
        self.assert_login_success(user=user)
    
        response = self.execute_user_delete()
    
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == get_user_delete_response()
    
        self.assert_validate_token_failure()
        self.assert_login_failure(user=user)

    def change_password_user_api_test(self):
        user = generate_random_user_with_password()
    
        self.assert_create_user_success(user=user)
        self.assert_login_success(user=user)
    
        new_password = get_random_string()
    
        response = self.execute_user_change_password(user=user, new_password=new_password)
    
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == get_user_password_update_response()
    
        self.assert_validate_token_failure()
        self.assert_login_failure(user=user)
    
        user.update({USER_PASSWORD_KEY: new_password})
        self.assert_login_success(user=user)
        
    def create_short_url_api_test(self):
        user = generate_random_user_with_password()
    
        self.assert_create_user_success(user=user)
        self.assert_login_success(user=user)

        long_url = generate_random_long_url_payload()
        response = self.execute_short_url_create(long_url=long_url.get(LONG_URL_KEY))
    
        assert response.status_code == status.HTTP_201_CREATED
        assert json.loads(response.json()).get(SHORT_URL_KEY)
        assert json.loads(response.json()).get(ID_KEY)
        
        self.assert_get_original_url_success(short_url=json.loads(response.json()).get(SHORT_URL_KEY), long_url=long_url.get(LONG_URL_KEY))
        
    
    def edit_long_url_api_test(self):
        user = generate_random_user_with_password()
    
        self.assert_create_user_success(user=user)
        self.assert_login_success(user=user)
    
        long_url = generate_random_long_url_payload()
        response = self.execute_short_url_create(long_url=long_url.get(LONG_URL_KEY))
        short_url = json.loads(response.json()).get(SHORT_URL_KEY)
        assert response.status_code == status.HTTP_201_CREATED
        assert short_url
    
        new_long_url = generate_random_long_url_payload()
        response = self.execute_long_url_edit(id=json.loads(response.json()).get(ID_KEY), old_long_url=long_url.get(LONG_URL_KEY), new_long_url=new_long_url.get(LONG_URL_KEY))
        
        self.assert_get_original_url_success(short_url=short_url, long_url=new_long_url.get(LONG_URL_KEY))
    
    def delete_long_url_api_test(self):
        user = generate_random_user_with_password()
    
        self.assert_create_user_success(user=user)
        self.assert_login_success(user=user)
    
        long_url = generate_random_long_url_payload()
        response = self.execute_short_url_create(long_url=long_url.get(LONG_URL_KEY))
        short_url = json.loads(response.json()).get(SHORT_URL_KEY)
        assert response.status_code == status.HTTP_201_CREATED
        assert short_url
    
        response = self.execute_long_url_delete(id=json.loads(response.json()).get(ID_KEY), long_url=long_url.get(LONG_URL_KEY))
    
        assert response.status_code == status.HTTP_200_OK
    
        self.assert_get_original_url_failure(short_url=short_url)
        
        