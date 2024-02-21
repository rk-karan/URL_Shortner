# from fastapi.testclient import TestClient
# from sqlalchemy import create_engine, StaticPool
# from sqlalchemy.orm import sessionmaker
# # from database_connector.database_connector import test_db_connector as db_connector
# import socket
# from ..application import app as application
# from ..database_handler.schemas import get_homepage_response

# import string
# import random

# client = TestClient(application)

# def get_random_string(length: int=5):
#     return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

# def generate_random_user_password():
#     return {
#         "name": get_random_string(),
#         "email": f"{get_random_string()}@{get_random_string()}.com",
#         "password": get_random_string()
#     }

# def test_home():
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json() == get_homepage_response(hostname= socket.gethostname())

