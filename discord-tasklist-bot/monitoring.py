import logging
from datetime import datetime
import os

logger = logging.getLogger("TasklistBot")


def setup_logger():
    """
    Setup the default logger

    Returns :
        The logger
    """

    os.makedirs("logs", exist_ok=True)

    # Set parameters and default values of logger
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Create a File Handler to log into a file
    filename = "logs"+os.sep + datetime.now().strftime('logs_%Y_%m_%d_%H_%M.log')
    file_handler = logging.FileHandler(filename)
    file_handler.setFormatter(formatter)

    # Create a Stream Handler for stream's output on console
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.INFO)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)


    discord_logger = logging.getLogger("discord")
    discord_logger.setLevel(logging.DEBUG)
    discord_logger.addHandler(stream_handler)
    
     # If you want to silence the default root logger output
    logging.getLogger().handlers.clear()

    return logger