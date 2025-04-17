from supporter.summarizer.base_summarizer import BaseSummarizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer


class LSASummarizer(BaseSummarizer):
    def __init__(self):
        super().__init__()

    def summarize(self, article: str) -> str:
        parser = PlaintextParser.from_string(article, Tokenizer("english"))
        summarizer = LsaSummarizer()
        ans = summarizer(parser.document, sentences_count=4)
        summary = " ".join([str(sent) for sent in ans])
        return summary
