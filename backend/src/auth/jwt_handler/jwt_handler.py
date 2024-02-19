"""This module is used to handle JWT operations.
"""

import os
import jwt
from dotenv import load_dotenv
from datetime import datetime, timedelta
from passlib.context import CryptContext

from logger import logger
from constants import PAYLOAD_USER_KEY, PAYLOAD_EXPIRY_KEY, DATE_TIME_FORMAT
from exceptions.exceptions import Invalid_User, Missing_Params
from ..OAuth2.OAuth2PasswordBearerWithCookie import OAuth2PasswordBearerWithCookie

# Load Environment Variables
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config', '.env')
load_dotenv(dotenv_path=env_path)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# Constants
ENCRYPTION_SCHEME = "bcrypt"
TOKEN_URL = "/user/login"
DEPRECATION_WARNING = "auto"

# Setup Bcrypt Context
BCRYPT_CONTEXT = CryptContext(schemes=[ENCRYPTION_SCHEME], deprecated=DEPRECATION_WARNING)

# Setup OAuth2 Scheme
O2AUTH2_SCHEME = OAuth2PasswordBearerWithCookie(tokenUrl=TOKEN_URL)

class JWT_Handler:
    """This class is used to handle JWT operations.
    """
    def __init__(self):
        try:
            self._logger = logger
            
            if not SECRET_KEY or not ALGORITHM or not ACCESS_TOKEN_EXPIRE_MINUTES or not BCRYPT_CONTEXT:
                raise Missing_Params
            
            self._SECRET_KEY = SECRET_KEY
            self._ALGORITHM = ALGORITHM
            self._ACCESS_TOKEN_EXPIRE_MINUTES = ACCESS_TOKEN_EXPIRE_MINUTES
            self._HASHING_CONTEXT = BCRYPT_CONTEXT
            self._O2AUTH2_SCHEME = O2AUTH2_SCHEME

        except Exception as e:
            self._logger.log(f"Error in JWT_Handler Initialization: {e}", error_tag=True)
            raise e
    
    def verify_password(self, plain_password, hashed_password):
        """This method is used to verify the password.

        Args:
            plain_password (string): Password in plain text
            hashed_password (string): Hashed Password

        Returns:
            bool: True if password is verified, False otherwise
        """
        return self._HASHING_CONTEXT.verify(plain_password, hashed_password)
    
    def get_hashed_password(self, password):
        """This method is used to get the hashed password.

        Args:
            password (string): Password in plain text

        Returns:
            string: Hashed Password
        """
        return self._HASHING_CONTEXT.hash(password)
    
    def create_access_token(self, payload: dict = {}):
        """This method is used to create the access token. (Encoding)

        Args:
            payload (dict, optional): Payload to encode. Defaults to {}.

        Returns:
            text: JWT Token
        """
        to_encode = payload.copy()
        expiry = str(datetime.utcnow() + timedelta(minutes=self._ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"expiry": expiry})
        encoded_jwt = jwt.encode(to_encode, self._SECRET_KEY, algorithm=self._ALGORITHM)
        return encoded_jwt
    
    def decode_token(self, token: str):
        """This method is used to decode the token. (Decoding)

        Args:
            token (str): JWT Token
        Returns:
            dict: The decoded payload
        """
        try:
            payload = jwt.decode(token, self._SECRET_KEY, algorithms=[self._ALGORITHM])
            return payload
        except Exception as e:
            raise e
    
    def verify_token(self, token: str):
        """This method is used to verify the token.

        Args:
            token (str): JWT Token

        Raises:
            INVALID_USER_EXCEPTION: If the token is invalid

        Returns:
            dict: The payload of the token
        """
        try:
            if not token or token == "":
                raise Invalid_User
            
            payload = self.decode_token(token)
            if not payload or not payload.get(PAYLOAD_EXPIRY_KEY) or not payload.get(PAYLOAD_USER_KEY) or datetime.utcnow() > datetime.strptime(payload.get(PAYLOAD_EXPIRY_KEY), DATE_TIME_FORMAT):
                raise Invalid_User
            
            return payload
        except Exception as e:
            raise e
        
    def get_current_user(self, token: str):
        """This method is used to get the current user from the token.

        Args:
            token (str): JWT Token

        Returns:
            dict: The user payload
        """
        try:
            payload = self.verify_token(token)
            return payload.get(PAYLOAD_USER_KEY)
        except Exception as e:
            raise Invalid_User(e)

# Initialize the JWT Handler
auth_handler = JWT_Handler()