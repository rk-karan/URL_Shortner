""" This module contains all the custom exceptions that are raised in the application.
"""
from constants import INVALID_USER_MESSAGE, ITEM_NOT_FOUND_MESSAGE, INVALID_BASE62_STRING, USER_EXISTS_MESSAGE, MISSING_PARAMS_MESSAGE, INVALID_REDIRECT_REQUEST_MESSAGE

class INVALID_USER_EXCEPTION(Exception):
    def __init__(self, message=INVALID_USER_MESSAGE):
        self.message = message
        super().__init__(self.message)

class NOT_FOUND_EXCEPTION(Exception):
    def __init__(self, message=ITEM_NOT_FOUND_MESSAGE):
        self.message = message
        super().__init__(self.message)

class INVALID_BASE62_STRING(Exception):
    def __init__(self, message=INVALID_BASE62_STRING):
        self.message = message
        super().__init__(self.message)

class USER_ALREADY_EXISTS_EXCEPTION(Exception):
    def __init__(self, message=USER_EXISTS_MESSAGE):
        self.message = message
        super().__init__(self.message)

class MISSING_PARAMS_EXCEPTION(Exception):
    def __init__(self, message=MISSING_PARAMS_MESSAGE):
        self.message = message
        super().__init__(self.message)

class Invalid_Redirection_Request(Exception):
    def __init__(self, message=INVALID_REDIRECT_REQUEST_MESSAGE):
        self.message = message
        super().__init__(self.message)