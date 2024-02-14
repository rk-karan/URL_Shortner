import jwt
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

from passlib.context import CryptContext

from ..OAuth2.OAuth2PasswordBearerWithCookie import OAuth2PasswordBearerWithCookie

from logger import logger

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

BCRYPT_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
O2AUTH2_SCHEME = OAuth2PasswordBearerWithCookie(tokenUrl="/user/login")

class JWT_Handler:
    def __init__(self):
        try:
            self.logger = logger
            if not SECRET_KEY or not ALGORITHM or not ACCESS_TOKEN_EXPIRE_MINUTES or not BCRYPT_CONTEXT:
                raise Exception("SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES are required")
            self.SECRET_KEY = SECRET_KEY
            self.ALGORITHM = ALGORITHM
            self.ACCESS_TOKEN_EXPIRE_MINUTES = ACCESS_TOKEN_EXPIRE_MINUTES
            self.HASHING_CONTEXT = BCRYPT_CONTEXT
            self.O2AUTH2_SCHEME = O2AUTH2_SCHEME

        except Exception as e:
            self.logger.log(f"Error in JWT_Handler Initialization: {e}", error_tag=True)
            raise e
    
    def verify_password(self, plain_password, hashed_password):
        return self.HASHING_CONTEXT.verify(plain_password, hashed_password)
    
    def get_hashed_password(self, password):
        return self.HASHING_CONTEXT.hash(password)
    
    def create_access_token(self, payload: dict = {}):
        to_encode = payload.copy()
        expiry = str(datetime.utcnow() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"expiry": expiry})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt
    
    def decode_token(self, token: str):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            return payload
        except Exception as e:
            raise e
    
    def verify_token(self, token: str):
        try:
            if not token or token == "":
                raise Exception("Invalid token")
            
            payload = self.decode_token(token)
            # print(payload)
            
            if not payload or not payload.get("expiry") or not payload.get("user") or datetime.utcnow() > datetime.strptime(payload.get("expiry"), "%Y-%m-%d %H:%M:%S.%f"):
                raise Exception("Invalid token")
            
            return payload
        except Exception :
            return None
        
    def get_current_user(self, token: str):
        payload = self.verify_token(token)
        return payload.get("user") if payload else None     

auth_handler = JWT_Handler()