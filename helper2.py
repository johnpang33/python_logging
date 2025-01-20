from logger import logger

# Create a child logger for module2
logger = logger.getChild("module2")

def module2_function():
    logger.warning("module2_function is running")
    logger.error("An error occurred in module2")