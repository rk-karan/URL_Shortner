import os
from logger import logger
from dotenv import load_dotenv
from decorators import log_info

load_dotenv()

CHARACTERS = os.getenv("CHARACTERS")
MAX_LIMIT = int(os.getenv("MAX_LIMIT"))

@log_info
def decimal_to_base62(decimal_num: int):
    """This function is used to convert decimal number to base62 integer.

    Args:
        decimal_num (int): Decimal Number

    Returns:
        str: Base62 Integer
    """
    try:
        if not decimal_num:
            raise Exception("Input is empty")
        if decimal_num > MAX_LIMIT:
            raise Exception("Input is greater than the maximum limit")
        base62_string = ""
        decimal_num = MAX_LIMIT - decimal_num

        while decimal_num > 0:
            remainder = decimal_num % 62
            base62_string = CHARACTERS[remainder] + base62_string
            decimal_num //= 62

        return base62_string or "0"
    except Exception as e:
        raise e

@log_info
def base62_to_decimal(base62_string: str):
    """This function is used to convert base62 integer to decimal number.

    Args:
        base62_string (str): Base62 Integer

    Returns:
        int: Decimal Number
    """
    try:
        if not base62_string:
            raise Exception("Input is empty")
        base62_dict = {char: index for index, char in enumerate(CHARACTERS)}
        decimal_num = 0
        base = 62
        print(base62_dict)
        print(base62_string)
        for char in base62_string:
            decimal_num = decimal_num * base + base62_dict[char]
        return MAX_LIMIT - decimal_num
    except Exception as e:
        raise e
