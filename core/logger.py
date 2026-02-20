import logging
from logging.handlers import TimedRotatingFileHandler


logger = logging.getLogger('general')
logger.setLevel(logging.DEBUG)

handler = TimedRotatingFileHandler(filename='./logs/log.txt', when="midnight",interval=1, backupCount=1, encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)


class Handler_info(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.INFO


console_handler = logging.StreamHandler()
console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)
console_handler.addFilter(Handler_info())
logger.addHandler(console_handler)

logger.propagate = False