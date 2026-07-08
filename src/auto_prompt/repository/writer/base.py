from abc import ABC, abstractmethod


class Writer(ABC):
    @abstractmethod
    def save(self, data, output: str) -> None:
        """Save the output to a file"""
        pass
