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

    # Get current date parts
    now = datetime.now()
    current_year = str(now.year)
    current_month = f"{now.month:02d}"
    log_dir = os.path.join("logs", current_year, current_month)
    os.makedirs(log_dir, exist_ok=True)

    # Set parameters and default values of logger
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Create a File Handler to log into a file
    filename = log_dir + os.sep + now.strftime('logs_%Y_%m_%d.log')
    file_handler = logging.FileHandler(filename, mode="a", encoding='utf-8')
    file_handler.setFormatter(formatter)

    # Create a Stream Handler for stream's output on console
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.INFO)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    # Add discord logger
    discord_logger = logging.getLogger("discord")
    discord_logger.setLevel(logging.DEBUG)
    discord_logger.addHandler(stream_handler)

    return logger
