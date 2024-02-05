from datetime import timedelta, datetime
import time
import jwt
import os
from dotenv import load_dotenv
from passlib.context import CryptContext

from logger import logger
from database_handler.schemas import USER_LOGIN, TOKEN_RESPONSE

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
class JWT_Handler:
    def __init__(self):
        try:
            self.logger = logger
            
            if not SECRET_KEY or not ALGORITHM or not ACCESS_TOKEN_EXPIRE_MINUTES:
                raise Exception("SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES are required")
            
            self.SECRET_KEY = SECRET_KEY
            self.ALGORITHM = ALGORITHM
            self.ACCESS_TOKEN_EXPIRE_MINUTES = ACCESS_TOKEN_EXPIRE_MINUTES
        except Exception as e:
            self.logger.log(f"Error in JWT_Handler Initialization: {e}", error_tag=True)
            raise e
    
    def signJWT(self, user: USER_LOGIN):
        payload = {
            'email': user.email,
            'expiry': str(datetime.utcnow() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES))
        }
        
        token = TOKEN_RESPONSE(access_token=jwt.encode(payload, self.SECRET_KEY, algorithm=self.ALGORITHM))
        return token
    
    def decodeJWT(self, token: str):
        try:
            if not token:
                raise Exception("Token is required")
            
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except Exception as e:
            return None
        


