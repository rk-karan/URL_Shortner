""" This module is used to log the messages to the console and to the log file.
"""
import os
import sys
import locale
import logging
from colorama import Fore, Style

LOG_LEVEL = logging.INFO
LOG_FORMATTER = "%(asctime)s - %(levelname)s - %(filename)s - %(message)s"
LOG_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "log.log")

class _logger:
    def __init__(self, log_formatter=LOG_FORMATTER, log_file_path=LOG_FILE_PATH, log_level=LOG_LEVEL):
        
        try:
            if not log_file_path:
                raise Exception("log_file_path is required")
            
            self.logger = logging.getLogger()
            self.logger.setLevel(int(log_level))
        
            self.formatter = logging.Formatter(log_formatter)
            self.log_file_path = log_file_path
        
            self.add_console_handler()
            self.add_file_handler()

        except Exception as e:
            self.log(f"Error in Logger Initialization: {e}")
        
    def add_console_handler(self):
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(self.formatter)
        
        self.logger.addHandler(consoleHandler)
    
    def add_file_handler(self):
        fileHandler = logging.FileHandler(self.log_file_path, 'w')
        fileHandler.setFormatter(self.formatter)
        
        self.logger.addHandler(fileHandler)
    
    def get_logger(self):
        return self.logger
    
    def log(self, message=None, error_tag=False):
        
        try:
            if not error_tag:
                if "SUCCESSFUL" in message:
                    colored_message = f"\n\n{Fore.GREEN}{message}{Style.RESET_ALL}\n\n"
                    self.logger.info(colored_message)
                else:
                    self.logger.info(message)
            else:
                if "UNSUCCESSFUL" in message:
                    colored_message = f"\n\n{Fore.RED}{message}{Style.RESET_ALL}\n\n"
                    self.logger.info(colored_message)
                else:
                    self.logger.error(message)
    
        except UnicodeDecodeError as e:
            os.environ["PYTHONIOENCODING"] = "utf-8"
            locale.setlocale(category=locale.LC_ALL, locale="en_GB.UTF-8")
            print(message.encode('utf-8', errors='ignore'))
            pass
        except Exception as e:
            print("Some Error Occurred.")
            pass
        
        sys.stdout.flush()


logger = _logger()
logger.log(f"New logger initialized at {LOG_FILE_PATH}")
