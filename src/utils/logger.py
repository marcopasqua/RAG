import logging
import os
import sys

LOG_LEVEL = logging.INFO

default_formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d:%(funcName)s] %(message)s",
)
stream_handler = logging.StreamHandler(stream=sys.stderr)
stream_handler.setLevel(LOG_LEVEL)
stream_handler.setFormatter(default_formatter)
logger = logging.getLogger(__name__)
logger.addHandler(stream_handler)
logger.setLevel(LOG_LEVEL)
logger.propagate = False