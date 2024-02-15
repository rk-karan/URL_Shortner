from constants import ITEM_NOT_FOUND_MESSAGE

class NOT_FOUND_EXCEPTION(Exception):
    def __init__(self, message=ITEM_NOT_FOUND_MESSAGE):
        self.message = message
        super().__init__(self.message)