from src import log

class BaseNode:
    def __init__(self, logger = None):
        self.logger = logger or log.get_logger(__name__)
        pass

    def __call__(self, raw_state):
        self.logger.info(f"{self.__class__.__name__} started")
        try:
            return self.run(raw_state)
        except Exception:
            self.logger.exception(f"{self.__class__.__name__} failed")
            raise
        finally:
            self.logger.info(f"{self.__class__.__name__} finished")

    def run(self, raw_state):
        raise NotImplementedError