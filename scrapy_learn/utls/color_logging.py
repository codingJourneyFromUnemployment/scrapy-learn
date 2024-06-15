import logging
from colorama import Fore, Style, init, Back

init(autoreset=True)

class ColorFormatter(logging.Formatter):
    Colors = {
      "WARNING": Fore.YELLOW,
      "ERROR": Fore.RED,
      "INFO": Fore.GREEN,
      "DEBUG": Fore.BLUE,
      "CRITICAL": Fore.MAGENTA
    }
    
    def format(self, record):
        color = self.COLORS.get(record.levelname, "")
        if color:
            record.msg = color + record.msg
        return logging.Formatter.format(self, record)
      

