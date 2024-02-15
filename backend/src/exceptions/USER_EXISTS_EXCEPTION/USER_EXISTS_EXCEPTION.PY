from constants import USER_EXISTS_MESSAGE

class USER_EXISTS_EXCEPTION(Exception):
    def __init__(self, message=USER_EXISTS_MESSAGE):
        self.message = message
        super().__init__(self.message)