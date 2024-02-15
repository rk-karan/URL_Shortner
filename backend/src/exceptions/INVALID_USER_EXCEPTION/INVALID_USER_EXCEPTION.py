from constants import INVALID_USER_MESSAGE

class INVALID_USER_EXCEPTION(Exception):
    def __init__(self, message=INVALID_USER_MESSAGE):
        self.message = message
        super().__init__(self.message)