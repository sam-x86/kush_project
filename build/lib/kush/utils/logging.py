# kush-framework/kush/utils/logging.py
"""
Logging utilities
"""

import logging
import sys
from colorama import Fore, Style

class Logger:
    def __init__(self, name="kush", level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        file_handler = logging.FileHandler('kush.log')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
    
    def info(self, message: str):
        self.logger.info(message)
        print(f"{Fore.GREEN}[+] {message}{Style.RESET_ALL}")
    
    def warning(self, message: str):
        self.logger.warning(message)
        print(f"{Fore.YELLOW}[!] {message}{Style.RESET_ALL}")
    
    def error(self, message: str):
        self.logger.error(message)
        print(f"{Fore.RED}[-] {message}{Style.RESET_ALL}")

def setup_logging(level=logging.INFO):
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('kush.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
