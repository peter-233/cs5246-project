import os
import spacy

from supporter.identifier.base_identifier import BaseIdentifier, IdentifyResult, IdentifyResultClazz


class PersonalizeHardIdentifier(BaseIdentifier):
    RESOURCE_ROOT = "resources/"
    VOCAB_ROOT = os.path.join(RESOURCE_ROOT, "data/english-vocabulary")
    VOCAB_FILES = [
        "1_Junior.txt",
        "2_HighSchool.txt",
        "3_CET4.txt",
        "4_CET6.txt",
        "5_PostGraduate.txt",
    ]
    HARD_POS = {
        "ADJ", "ADV", "NOUN", "VERB"
    }

    easy_words: set[str] = set()
    nlp: spacy.Language = spacy.load("en_core_web_sm")

    def __init__(self):
        super().__init__()
        vocab_paths = {os.path.join(self.VOCAB_ROOT, file) for file in self.VOCAB_FILES}
        for path in vocab_paths:
            self.__load_from_vocab_txt(path)

    def __load_from_vocab_txt(self, path: str) -> None:
        with open(path, 'r', encoding="utf8") as f:
            for line in f:
                self.easy_words.add(line.split("\t")[0].lower())

    def identify(self, article: str) -> list[IdentifyResult]:
        tokens = self.nlp(article)
        results: list[IdentifyResult] = []

        for token in tokens:
            if token.pos_ not in self.HARD_POS:
                continue
            if token.lemma_ in self.easy_words:
                continue

            result = IdentifyResult(
                start_inclusive=token.idx,
                end_exclusive=token.idx + len(token.text),
                text=token.text,
                clazz=IdentifyResultClazz.HARD,
                hard_level=1.0,
                token=token,
                label=None,
                entity=None,
            )
            results.append(result)
        return results
