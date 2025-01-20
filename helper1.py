import logging
from logger import logger
from helper1a import module1a_function

# Create a child logger for module1
logger = logger.getChild("module1")
logger.setLevel(logging.WARNING)

def module1_function():
    module1a_function()
    logger.info("module1_function is running")
    logger.debug("Debugging in module1")