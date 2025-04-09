from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

from supporter.identifier import IdentifyResult

class ExplainResultClazz(Enum):
    DEFINITION = "definition"
    EXAMPLE = "example"
    EXT_LINK = "ext_link"

@dataclass
class ExplainResult:
    clazz: ExplainResultClazz
    content: str

class BaseExplainer(ABC):
    @abstractmethod
    def explain(self, article: str, identify_result: IdentifyResult) -> dict[str: ExplainResult]:
        pass
