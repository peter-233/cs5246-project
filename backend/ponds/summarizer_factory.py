import dataclasses
from typing import Any

from pond import PooledObjectFactory, PooledObject

from supporter.summarizer.base_summarizer import BaseSummarizer
from supporter.summarizer.lda_summarizer import LDASummarizer


@dataclasses.dataclass
class Summarizer:
    summarizer: BaseSummarizer


class SummarizerFactory(PooledObjectFactory):

    def createInstance(self) -> PooledObject:
        core_summarizer = LDASummarizer()
        summarizer = Summarizer(core_summarizer)
        return PooledObject(summarizer)

    def destroy(self, pooled_object: PooledObject) -> None:
        del pooled_object

    def reset(self, pooled_object: PooledObject, **kwargs: Any) -> PooledObject:
        return pooled_object

    def validate(self, pooled_object: PooledObject) -> bool:
        return True


summarizer_factory = SummarizerFactory(pooled_maxsize=1, least_one=True)
