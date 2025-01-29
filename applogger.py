import logging
from logging.handlers import TimedRotatingFileHandler


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
