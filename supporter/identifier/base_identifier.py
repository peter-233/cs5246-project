from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

import spacy.tokens
from spacy_entity_linker.EntityElement import EntityElement


class IdentifyResultClazz(Enum):
    HARD = "hard"
    NER = "ner"


@dataclass
class IdentifyResult:
    start_inclusive: int
    end_exclusive: int
    text: str

    clazz: IdentifyResultClazz
    hard_level: Optional[float]  # activate if clazz == ResultClazz.HARD
    token: Optional[spacy.tokens.Token]  # activate if clazz == ResultClazz.HARD
    label: Optional[str]  # activate if clazz == ResultClazz.NER
    entity: Optional[EntityElement]  # activate if clazz == ResultClazz.NER


class BaseIdentifier(ABC):

    @abstractmethod
    def identify(self, article: str) -> list[IdentifyResult]:
        pass
