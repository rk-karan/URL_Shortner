from fastapi.testclient import TestClient
from src.application import app, db_connector
from src.test_cases import Test_Case_Library

test_handler = Test_Case_Library(client=TestClient(app))

def test_home():
    test_handler.home_api_test()

def test_create_user():
    test_handler.create_user_api_test()

def test_logout_user():
    test_handler.logout_user_api_test()

def test_delete_user():
    test_handler.delete_user_api_test()

def test_change_password_user():
    test_handler.change_password_user_api_test()

def test_add_url():
    test_handler.create_short_url_api_test()

def test_edit_url():
    test_handler.edit_long_url_api_test()

def test_delete_url():
    test_handler.delete_long_url_api_test()

def setup() -> None:
    try:
        db_connector._Base.metadata.create_all(db_connector._engine)
        print("Database tables initialized")
    except Exception as e:
        print(f"Error initializing database tables: {e}")


# def teardown() -> None:
#     try:
#         db_connector._Base.metadata.drop_all(db_connector._engine)
#         print("Database tables de-initialized")
#     except Exception as e:
#         print(f"Error de-initializing database tables: {e}")
    