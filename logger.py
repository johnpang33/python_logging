import logging
import os

class Logger:
    def __init__(self, name: str, log_file: str = None, level: int = logging.DEBUG):
        """
        Initialize a logger instance.

        :param name: Name of the logger
        :param log_file: Log file name (optional)
        :param level: Logging level (default is DEBUG)
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Formatter for logs
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # File handler (optional)
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def get_logger(self):
        """Return the logger instance."""
        return self.logger
    
CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(CURRENT_DIRECTORY, 'app.log')
logger = Logger(name="main", log_file=log_file).get_logger()