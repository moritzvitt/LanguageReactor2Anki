import logging
import time 
import os

# get time 
current_time = time.strftime("%Y%m%d%H%M%S", time.localtime())

# Configure logger name and level (adjust as needed)
logger_name = __name__  # Use the module name as the logger name
log_level = logging.INFO

# write log in to folder

log_dir = "./logs"  # Replace with your desired directory
# Create the directory if it doesn't exist
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, f'{current_time}_app.log')

log_format = ('\n'
              '================================================================\n'
              '%(asctime)s - %(levelname)s - %(name)s - [%(funcName)s:%(lineno)d]\n'
              'Message: %(message)s\n'
              '----------------------------------------------------------------\n')

logging.basicConfig(
    filename=log_file,
    level=log_level,
    format=log_format
)

# Get the logger instance
logger = logging.getLogger(logger_name)



import logging
import pandas as pd

# Define the log_io decorator
def log_io(func):
    def wrapper(*args, **kwargs):
        # Log function inputs

        logger.info(f"Function {func.__name__} called with args: {args} and kwargs: {kwargs}")

        # Call the function and get the result
        result = func(*args, **kwargs)

        # Log function output
        if isinstance(result, pd.DataFrame):
            logger.info(f"Function {func.__name__} returned a DataFrame with shape: {result.shape}")
        else:
            logger.info(f"Function {func.__name__} returned: {result}")

        return result
    return wrapper
