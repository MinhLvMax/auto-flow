from src.loggers import main_logger

class BaseNode:
    def __init__(self, logger = None):
        self.loger = logger or main_logger

    def __call__(self, raw_state):
        self.loger.info(f"{self.__class__.__name__} started")
        try:
            return self.run(raw_state)
        except Exception:
            self.loger.exception(f"{self.__class__.__name__} failed")
            raise
        finally:
            self.loger.info(f"{self.__class__.__name__} finished")

    def run(self, raw_state):
        raise NotImplementedError