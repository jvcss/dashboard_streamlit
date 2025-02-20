import logging
from utils.logger import Logger

class ErrorHandler:
    logger = Logger.get_logger("ErrorHandler")

    @staticmethod
    def handle_error(e):
        ErrorHandler.logger.error(f"Error occurred: {str(e)}")
