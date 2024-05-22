import logging
import time
import pandas as pd
from functools import wraps
import os

# Enhanced log format
log_format = ('\n'
              '================================================================\n'
              '%(asctime)s - %(levelname)s - %(name)s - [%(funcName)s:%(lineno)d]\n'
              '%(message)s\n'
              '----------------------------------------------------------------\n')

current_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
log_dir = "./logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f'{current_time}_app.log')

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format=log_format
)

logger = logging.getLogger(__name__)

def log_io(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        log_messages = []

        # Log function input details
        log_messages.append(f"Function {func.__name__} called with {len(args)} positional arguments and {len(kwargs)} keyword arguments.")
        
        for i, arg in enumerate(args):
            if isinstance(arg, pd.DataFrame):
                log_messages.append(f"Function {func.__name__} - Argument {i}: DataFrame with shape: {arg.shape}")
            else:
                log_messages.append(f"Function {func.__name__} - Argument {i} ({type(arg)}): {arg}")
        
        for k, v in kwargs.items():
            if isinstance(v, pd.DataFrame):
                log_messages.append(f"Function {func.__name__} - Keyword argument {k}: DataFrame with shape: {v.shape}")
            else:
                log_messages.append(f"Function {func.__name__} - Keyword argument ({type(v)}) {k}: {v}")

        # Call the function and get the result
        result = func(*args, **kwargs)

        # Log function output details   
        if isinstance(result, pd.DataFrame):
            log_messages.append(f"Function {func.__name__} returned a DataFrame with shape: {result.shape}")
        elif isinstance(result, tuple):
            types = ', '.join([str(type(item)) for item in result])
            log_messages.append(f"Function {func.__name__} returned a tuple of types ({types})")
        else:
            log_messages.append(f"Function {func.__name__} returned ({type(result)}): {result}")

        # Capture the end time and calculate execution duration
        end_time = time.time()
        duration = end_time - start_time
        log_messages.append(f"Function {func.__name__} executed in {duration:.4f} seconds")

        # Log all messages at once
        logger.info("\n".join(log_messages))

        return result
    return wrapper

