When you need to implement complex logging in Python, especially in larger applications, you might require advanced features such as rotating log files, different logging levels for different modules, logging to multiple outputs (console, file, remote services), or custom logging formats. Python’s built-in logging module is flexible enough to handle these scenarios, but it may require a bit of configuration.

Here’s a breakdown of how to implement complex logging in Python, touching on multiple common requirements:

1. Logging Configuration with logging.config
You can use logging.config to define logging configurations via dictionaries or external configuration files (like .ini or .yaml). This makes your code more modular and easy to adjust.

Example: Complex Logging with Dictionary Configuration
python
Copy
Edit
import logging
import logging.config

# Define the logging configuration dictionary
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{asctime} {name} {levelname} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'app.log',
            'formatter': 'simple',
        },
        'rotating_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'rotated_app.log',
            'maxBytes': 5 * 1024 * 1024,  # 5 MB
            'backupCount': 3,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'myapp': {
            'handlers': ['console', 'file', 'rotating_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'myapp.module1': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}

# Apply the logging configuration
logging.config.dictConfig(LOGGING_CONFIG)

# Get loggers
logger = logging.getLogger('myapp')
module1_logger = logging.getLogger('myapp.module1')

# Log messages
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
module1_logger.warning("This is a warning in module1")
Explanation
verbose and simple formatters: These control the structure of log messages.
RotatingFileHandler: This handler automatically rotates the log file when it reaches a specified size, creating backups.
Loggers: Different loggers can have distinct handlers and levels. For example, myapp logs everything to all handlers, while myapp.module1 only logs warnings to the console.
2. Rotating and Timed Log Files
Using RotatingFileHandler (as seen in the example above) or TimedRotatingFileHandler, you can manage log files automatically. You can either rotate logs based on file size or time.

Timed Rotating File Example
python
Copy
Edit
import logging
from logging.handlers import TimedRotatingFileHandler

# Create a custom timed rotating file handler
handler = TimedRotatingFileHandler(
    'app_timed.log', when='midnight', interval=1, backupCount=7
)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add handler to the logger
logger = logging.getLogger('myapp')
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# Log something
logger.info("This log will rotate at midnight and keep 7 days of backups.")
In this setup:

The log file (app_timed.log) will be rotated at midnight.
Only 7 days' worth of logs will be kept, with older logs being deleted.
3. Logging to Multiple Destinations (Console, File, Remote)
To log to multiple destinations like the console, files, and even remote systems (e.g., a remote server via SocketHandler), you can configure multiple handlers.

Example: Logging to Console, File, and Remote Server
python
Copy
Edit
import logging
from logging.handlers import SocketHandler, RotatingFileHandler

# Set up logging to console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)

# Set up logging to file with rotation
file_handler = RotatingFileHandler('app.log', maxBytes=10*1024*1024, backupCount=5)
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

# Set up logging to a remote server (UDP or TCP)
remote_handler = SocketHandler('localhost', 514)
remote_handler.setLevel(logging.ERROR)
remote_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
remote_handler.setFormatter(remote_formatter)

# Create logger and add handlers
logger = logging.getLogger('myapp')
logger.setLevel(logging.DEBUG)
logger.addHandler(console_handler)
logger.addHandler(file_handler)
logger.addHandler(remote_handler)

# Log messages
logger.debug("This message will go to the console and file.")
logger.error("This message will go to the console, file, and remote server.")
StreamHandler: Logs to the console.
RotatingFileHandler: Logs to a file with automatic rotation.
SocketHandler: Sends logs to a remote server (useful for centralized logging).
4. Custom Handlers and Filters
Sometimes, you may need more control over how logs are handled. You can create custom handlers or filters to manipulate logs before they are processed.

Custom Handler Example
python
Copy
Edit
import logging

class CustomHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        print(f"Custom log entry: {log_entry}")

# Create logger
logger = logging.getLogger('myapp')

# Add custom handler
custom_handler = CustomHandler()
custom_handler.setLevel(logging.DEBUG)
custom_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(custom_handler)

# Log a message
logger.debug("This is a custom log handler in action!")
Custom Filter Example
python
Copy
Edit
class CustomFilter(logging.Filter):
    def filter(self, record):
        return "secret" not in record.getMessage()

# Create logger
logger = logging.getLogger('myapp')

# Add custom filter
logger.addFilter(CustomFilter())

# Log messages
logger.info("This is a normal message.")
logger.info("This message contains a secret and will be filtered.")
Custom Handler: Defines how log records are output (in the example, we're simply printing them with a custom prefix).
Custom Filter: Filters log messages based on custom logic.
5. Complex Log Message Formatting
You can use custom formats for your log messages. For example, you might want to include additional information such as the thread name, process ID, or the user running the application.

Example: Advanced Log Formatting
python
Copy
Edit
import logging

# Create a custom formatter with advanced fields
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s - '
    'Thread: %(threadName)s - Process: %(process)d'
)

# Set up a console handler with the custom formatter
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# Create the logger
logger = logging.getLogger('myapp')
logger.setLevel(logging.DEBUG)
logger.addHandler(console_handler)

# Log a message
logger.debug("This is an advanced formatted log message.")
This log message would include:

Time (asctime)
Logger name (name)
Log level (levelname)
The log message itself (message)
Thread name (threadName)
Process ID (process)
6. Remote Logging (Syslog, HTTP, and More)
If you need to log to remote services, Python’s logging module supports handlers for Syslog, HTTP, and other services.

Example: Sending Logs via HTTP
python
Copy
Edit
from logging.handlers import HTTPHandler

# Configure HTTPHandler to send logs to a web server
http_handler = HTTPHandler(
    host='localhost:5000', url='/log', method='POST'
)
http_handler.setLevel(logging.WARNING)
http_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

# Add handler to logger
logger = logging.getLogger('myapp')
logger.setLevel(logging.DEBUG)
logger.addHandler(http_handler)

# Log a message
logger.warning("This will be sent to the HTTP server.")
Conclusion
To implement complex logging in Python, you should:

Leverage logging.config for centralized, modular configuration.
Use RotatingFileHandler and TimedRotatingFileHandler to manage log file sizes and backups.
Log to multiple destinations, including remote servers, using custom handlers.
Utilize custom filters and handlers to customize how logs are processed.
Apply advanced formatting to your logs for detailed, structured output.
This will help you build a flexible, maintainable logging system suitable for complex applications.

Let me know if you'd like further examples or if you have specific use cases in mind!