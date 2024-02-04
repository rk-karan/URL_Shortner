from functools import wraps
from logger import logger

def log_info(func):
    """A decorator to log initiation and execution completion of any function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.log(f"Function {func.__name__} called with keyword arguments: {kwargs} arguments: {args}")
        try:
            result = func(*args, **kwargs)
            logger.log(f"SUCCESSFUL: Executed Function {func.__name__}")
        except Exception as e:
            logger.log(f"UNSUCCESSFUL: Could not execute Function {func.__name__} returned: {e}", error_tag=True)
            pass
        return result
    return wrapper