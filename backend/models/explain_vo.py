from dataclasses import dataclass
from supporter.explainer.base_explainer import ExplainResultClazz


@dataclass
class ExplainVo:
    type: str = 'definition'
    content: str = ''
    def __init__(self, _type: ExplainResultClazz, content: str):
        self.type = _type.value
        self.content = content

