import logging
from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger("General")
logger.setLevel(logging.DEBUG)

handler = TimedRotatingFileHandler(
    "backend/logs/log.log",
    interval=1,
    when="midnight",
    backupCount=7,
    encoding='utf-8'
)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)