import os
from dotenv import load_dotenv
from src.exceptions import Invalid_Base62_String

# Load Environment Variables
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', '.env')
load_dotenv(dotenv_path=env_path)

CHARACTERS = os.getenv("CHARACTERS")
MAX_LIMIT = int(os.getenv("MAX_LIMIT"))

def decimal_to_base62(decimal_num: int):
    """This function is used to convert decimal number to base62 integer.

    Args:
        decimal_num (int): Decimal Number

    Returns:
        str: Base62 Integer
    """
    try:
        if not decimal_num:
            raise Invalid_Base62_String
        if decimal_num > MAX_LIMIT:
            raise Invalid_Base62_String
        base62_string = ""
        decimal_num = MAX_LIMIT - decimal_num

        while decimal_num > 0:
            remainder = decimal_num % 62
            base62_string = CHARACTERS[remainder] + base62_string
            decimal_num //= 62

        return base62_string or "0"
    except Exception as e:
        raise e

def base62_to_decimal(base62_string: str):
    """This function is used to convert base62 integer to decimal number.

    Args:
        base62_string (str): Base62 Integer

    Returns:
        int: Decimal Number
    """
    try:
        if not base62_string:
            raise Invalid_Base62_String
        base62_dict = {char: index for index, char in enumerate(CHARACTERS)}
        decimal_num = 0
        base = 62
        
        for char in base62_string:
            decimal_num = decimal_num * base + base62_dict[char]
        
        if decimal_num > MAX_LIMIT:
            raise Invalid_Base62_String
        
        return MAX_LIMIT - decimal_num
    except Exception as e:
        raise e
