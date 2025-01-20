import os
from logger import logger
from helper1 import module1_function
from helper2 import module2_function

# Log messages


if __name__ == "__main__":
    logger.info("Application has started")
    logger.debug("This is a debug message")
    logger.info("Application started")
    logger.warning("This is a warning")
    logger.error("An error occurred")
    logger.critical("Critical issue!")

    # Call functions from other modules
    module1_function()
    module2_function()

    logger.info("Application has finished")