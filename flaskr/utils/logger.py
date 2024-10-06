import logging
from config.config import Config

config=Config()

class Logger():
    def __init__(self):
        self.environment_data = {
            "environment": config.ENVIRONMENT,
            "appName": config.APP_NAME
        }
    def info(self, message, object = {}):
        logging.info(message, {**object, **self.environment_data})
    
    def debug(self, message, object = {}):
        logging.debug(message, {**object, **self.environment_data})
    
    def error(self, message, object = {}):
        logging.error(message, {**object, **self.environment_data})
    
    def exception(self, message, object = {}):
        logging.exception(message, {**object, **self.environment_data})
    
    def warn(self, message, object = {}):
        logging.warn(message, {**object, **self.environment_data})