from loguru import logger
import sys

logger.disable("scribepy")


def custom_logger(sink=sys.stderr, level="WARNING"):
    logger.remove()
    logger.configure(handlers=[{"sink": sink, "level": level}])
    logger.enable("scribepy")
