from config import LOG_FOLDER, LOG_FORMAT, LOG_FILE, LOG_MAX_BYTES, LOG_COUNT
from os.path import exists, join
from os import mkdir
from sys import stdout
import logging
from logging.handlers import RotatingFileHandler

if not exists(LOG_FOLDER):
    mkdir(LOG_FOLDER)

logger = logging.getLogger('app')
logger.setLevel(logging.INFO)
log_formatter = logging.Formatter(LOG_FORMAT)
file_handler = RotatingFileHandler(join(LOG_FOLDER, LOG_FILE),
                                   maxBytes=LOG_MAX_BYTES,
                                   backupCount=LOG_COUNT)
file_handler.setFormatter(log_formatter)
stream_handler = logging.StreamHandler(stdout)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
