from abc import ABC, abstractmethod

class Reader(ABC):
    @abstractmethod
    def parse(self, path):
        pass