'''

from logging import basicConfig, getLogger
from typing import Optional

LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

def configure_logging(level: str) -> None:
    basicConfig(format=LOG_FORMAT, datefmt=LOG_DATE_FORMAT, level=level)

    
-- In other py files:

from logging import getLogger

LOG = getLogger(__name__)

   ...
   LOG.warning("Could not read image ID for %s: %s", container.name, error)


'''

import logging
from logging.handlers import TimedRotatingFileHandler
##from typing import Optional

## config logging:
log_formatter = logging.Formatter('%(asctime)s ; %(levelname)s ; %(message)s')
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)

file_handler = TimedRotatingFileHandler("PyApi1.log", when="midnight", interval=1, backupCount=7) 
#file_handler = logging.FileHandler("PyApi1.log",encoding="UTF-8")
log_formatter = logging.Formatter('%(asctime)s ; %(levelname)s ; %(filename)s  ; %(message)s')
file_handler.setFormatter(log_formatter)

logger = logging.getLogger("PyApi1")        #  logger = logging.getLogger(__name__) # if only used in main.py
logger.setLevel(logging.DEBUG)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

# logging.basicConfig(level=logging.DEBUG, handlers=[console_handler, file_handler])
# def get_logger(name: Optional[str] = None) -> logging.Logger:
#     return logging.getLogger(name if name else "PyApi1")
