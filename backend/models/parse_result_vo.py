from dataclasses import dataclass, field

from .explain_vo import ExplainVo
from supporter.identifier import IdentifyResultClazz


@dataclass
class ParseResultVo:
    type: str = 'hard'
    startInclusive: int = 0
    endExclusive: int = 0
    explains: list[ExplainVo] = field(default_factory=list)

    def __init__(self, _type: IdentifyResultClazz, startInclusive: int, endExclusive: int, explains: list[ExplainVo]):
        self.type = _type.value
        self.startInclusive = startInclusive
        self.endExclusive = endExclusive
        self.explains = explains




