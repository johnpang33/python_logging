from logger import logger
import logging

logger = logger.getChild("module1").getChild("module1a")
logger.setLevel(logging.DEBUG)

def module1a_function():
    logger.info("module1_function is running")
    logger.debug("Debugging in module1")