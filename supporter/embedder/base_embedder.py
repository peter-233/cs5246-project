from abc import ABC, abstractmethod

import numpy as np


class BaseEmbedder(ABC):
    @abstractmethod
    def embed(self, text: str) -> dict[str, any]:
        pass

    @abstractmethod
    def get_word_embedding(self, text: str, word_pos: tuple[int, int]) -> np.ndarray:
        pass