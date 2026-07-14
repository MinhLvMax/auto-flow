from src.loggers import main_logger

class BaseNode:
    def __init__(self, logger = None):
        self.loger = logger or main_logger