import dataclasses
from typing import Any

from pond import PooledObjectFactory, PooledObject

from supporter.summarizer import LDASummarizer, LSASummarizer, BartSummarizer, TextRankSummarizer


@dataclasses.dataclass
class Summarizer:
    lda_summarizer: LDASummarizer
    textrank_summarizer: TextRankSummarizer
    lsa_summarizer: LSASummarizer
    bart_summarizer: BartSummarizer


class SummarizerFactory(PooledObjectFactory):

    def createInstance(self) -> PooledObject:
        lda_summarizer = LDASummarizer()
        textrank_summarizer = TextRankSummarizer()
        lsa_summarizer = LSASummarizer()
        bart_summarizer = BartSummarizer()
        summarizer = Summarizer(
            lda_summarizer,
            textrank_summarizer,
            lsa_summarizer,
            bart_summarizer
        )
        return PooledObject(summarizer)

    def destroy(self, pooled_object: PooledObject) -> None:
        del pooled_object

    def reset(self, pooled_object: PooledObject, **kwargs: Any) -> PooledObject:
        return pooled_object

    def validate(self, pooled_object: PooledObject) -> bool:
        return True


summarizer_factory = SummarizerFactory(pooled_maxsize=1, least_one=True)
