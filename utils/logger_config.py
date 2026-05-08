import logging
import os
from datetime import datetime

def setup_logger():
    """
    Configure and return a custom logger for the framework.
    """
    # Create logs directory if it doesn't exist
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # Log file name with timestamp
    log_file = os.path.join("logs", f"test_execution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

    # Create logger
    logger = logging.getLogger("Bright_Automation")
    logger.setLevel(logging.DEBUG)

    # Clear any existing handlers to avoid duplicates
    if logger.hasHandlers():
        logger.handlers.clear()

    # Create file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Single instance of logger to be shared
logger = setup_logger()
