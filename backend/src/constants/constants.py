## Exception messages

# Invalid user message. Generally occurs when the user is not authorized.
INVALID_USER_MESSAGE = "Invalid user"

# User exists message. Generally occurs when the user already exists.
USER_EXISTS_MESSAGE = "User already exists"

# Item not found message. Generally occurs when the item is not found in the database.
ITEM_NOT_FOUND_MESSAGE = "Item not found"

# Invalid base62 string message. Generally occurs when base62conversions operations runs into errors.
INVALID_BASE62_STRING = "Invalid base62 string"

# Missing parameters message. Generally occurs when the required parameters are not provided.
MISSING_PARAMS_MESSAGE = "Initialization parameters missing"

# Invalid redirection request message. Generally occurs when the redirection request is invalid.
INVALID_REDIRECT_REQUEST_MESSAGE = "Invalid redirection request"

## User CRUD messages

# Signup success message. Generally occurs when the user is signed up successfully.
SIGNUP_SUCCESS_MESSAGE = "User signed up successfully"

# Login success message. Generally occurs when the user is logged in successfully.
LOGIN_SUCCESS_MESSAGE = "User logged in successfully"

# Logout success message. Generally occurs when the user is logged out successfully.
LOGOUT_SUCCESS_MESSAGE = "User logged out successfully"

# User delete success message. Generally occurs when the user profile deleted successfully.
DELETE_USER_SUCCESS_MESSAGE = "User deleted successfully"

# User profile update success message. Generally occurs when the user profile is updated successfully.
CHANGE_PASSWORD_SUCCESS_MESSAGE = "Password changed successfully"

## URL CRUD messages

# URL create success message. Generally occurs when the URL is created successfully.
CREATE_URL_SUCCESS_MESSAGE = "URL created successfully"

# URL delete success message. Generally occurs when the URL is deleted successfully.
DELETE_URL_SUCCESS_MESSAGE = "URL deleted successfully"

# URL edit success message. Generally occurs when the URL is edited successfully.
EDIT_URL_SUCCESS_MESSAGE = "URL edited successfully"

## Authorization constants

# Access Token access key
ACCESS_TOKEN_KEY = "access_token"

# Authorization scheme.
AUTHORIZATION_SCHEME = "Bearer"

## Important dictionary keys

# Key to access user name
USER_NAME_KEY = "name"

# Key to access user email
USER_EMAIL_KEY = "email"

# Key to access user in payload
PAYLOAD_USER_KEY = "user"

# Key to access long url in request
LONG_URL_KEY = "long_url"

# Key to access expiry in payload
PAYLOAD_EXPIRY_KEY = "expiry"

# Key to access user password
USER_PASSWORD_KEY = "password"

# Key to access urls
URLS_KEY = "urls"


## Domain name
DOMAIN_NAME = "http://localhost:8000"

## NULL text
NULL_TEXT = "NULL"

## NULL Field in URLS_MAPPING DB
NULL_ENTRY_IN_URLS_MAPPING = {
    "email": NULL_TEXT,
    "long_url": NULL_TEXT
}

## Date time format
DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"