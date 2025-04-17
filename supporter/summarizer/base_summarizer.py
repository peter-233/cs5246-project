from abc import ABC, abstractmethod


class BaseSummarizer(ABC):
    @abstractmethod
    def summary(self, article: str) -> str:
        pass
