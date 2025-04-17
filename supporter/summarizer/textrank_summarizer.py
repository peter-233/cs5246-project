import numpy as np
import spacy
from sklearn.metrics.pairwise import cosine_similarity

from supporter.summarizer.base_summarizer import BaseSummarizer


class TextRankSummarizer(BaseSummarizer):
    def __init__(self, num_sentences: int = 4):
        super().__init__()
        self.num_sentences = num_sentences
        self.nlp = spacy.load("en_core_web_sm")

    def __clean(self, text: str) -> list[str]:
        doc = self.nlp(text)
        sentences = [s.text.strip() for s in doc.sents]
        sentences = list(dict.fromkeys(sentences))
        sentences = [s for s in sentences if len(s.split()) >= 5]
        return sentences

    def __tokenize(self, text: list[str]) -> list[list[str]]:
        sentences = []
        for t in text:
            doc = self.nlp(t)
            sentence = []
            for token in doc:
                if token.is_alpha and not token.is_stop and token.pos_ in ["NOUN", "VERB", "ADJ", "PROPN"]:
                    sentence.append(token.text)
            sentences.append(sentence)
        return sentences

    def __lemmatize(self, text: list[list[str]]) -> list[list[str]]:
        sentences = []
        for t in text:
            doc = self.nlp(" ".join(t))
            sentence = []
            for token in doc:
                sentence.append(token.lemma_.lower())
            sentences.append(sentence)
        return sentences

    def __similarity(self, text: list[list[str]]) -> np.ndarray:
        tfidf = []
        for t in text:
            sentence = " ".join(t) if isinstance(t, list) else str(t)
            doc = self.nlp(sentence)
            tfidf.append(doc.vector)
        similarity = cosine_similarity(tfidf)
        return similarity

    def __textrank(self, similarity, text, top=3):
        n = len(similarity)
        scores = np.array([1] * n)
        alpha = 0.9
        for i in range(100):
            tmp = (1 - alpha) + alpha * similarity.T.dot(scores)
            scores = tmp
        idx = np.argsort(scores)[-top:][::-1]
        return [text[i] for i in sorted(idx)]

    def summarize(self, article: str) -> str:
        sentences = self.__clean(article)
        sentences1 = self.__tokenize(sentences)
        sentences2 = self.__lemmatize(sentences1)
        sentences3 = self.__similarity(sentences2)
        ans = self.__textrank(sentences3, sentences, self.num_sentences)
        return " ".join(ans)
