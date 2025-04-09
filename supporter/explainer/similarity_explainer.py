import nltk
import numpy as np
from nltk import data
from nltk.corpus import wordnet as wn

from supporter.embedder.base_embedder import BaseEmbedder
from supporter.explainer.base_explainer import BaseExplainer, ExplainResult, ExplainResultClazz
from supporter.identifier import IdentifyResult, IdentifyResultClazz

from supporter.utils import POSConverter


class SimilarityExplainer(BaseExplainer):
    RESOURCE_DATA_ROOT = "resources/data"
    embedder: BaseEmbedder = None

    def __init__(self, embedder):
        super().__init__()
        nltk.download('wordnet', download_dir=self.RESOURCE_DATA_ROOT)
        data.path.append(self.RESOURCE_DATA_ROOT)
        self.embedder = embedder

    def __get_synset_embedding(self, synset: str, definition: str) -> np.ndarray:
        emb_sent = f"{synset}, {definition}."
        synset_pos = (0, len(synset))
        emb = self.embedder.get_word_embedding(emb_sent, synset_pos)
        return emb

    def __get_cosine_similarity(self, emb1: np.ndarray, emb2: np.ndarray) -> float:
        return np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))

    def explain(self, article: str, identify_result: IdentifyResult) -> dict[str: ExplainResult]:
        assert self.embedder is not None, "Embedder is not initialized"
        if identify_result.clazz != IdentifyResultClazz.HARD:
            return {}

        token = identify_result.token
        wn_pos = POSConverter().decode(token.pos_, POSConverter.SPACY_FORMAT).encode(POSConverter.WORDNET_FORMAT)
        synsets = wn.synsets(token.lemma_, pos=wn_pos)
        if len(synsets) == 0:
            return {}
        if len(synsets) == 1:
            return {
                "definition": ExplainResult(
                    clazz = ExplainResultClazz.DEFINITION,
                    content = synsets[0].definition(),
                ),
            }

        synset_embeddings = {syn: self.__get_synset_embedding(token.lemma_, syn.definition()) for syn in synsets}

        target_embedding = self.embedder.get_word_embedding(article, (
            identify_result.start_inclusive, identify_result.end_exclusive))
        items = list(synset_embeddings.items())
        min_syn, min_emb = min(items, key=lambda item: self.__get_cosine_similarity(item[1], target_embedding))

        return {
            "definition": ExplainResult(
                clazz = ExplainResultClazz.DEFINITION,
                content = min_syn.definition(),
            ),
        }


