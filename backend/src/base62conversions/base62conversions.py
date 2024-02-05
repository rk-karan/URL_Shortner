from logger import logger
from decorators import log_info

CHARACTERS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
MAX_LIMIT = 70000

@log_info
def decimal_to_base62(decimal_num: int):

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
        logger.log(f"Error converting decimal to base62: {e}", error_tag=True)
        raise e

@log_info
def base62_to_decimal(base62_string: str):
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
        logger.log(f"Error converting base62 to decimal: {e}", error_tag=True)
        raise e
