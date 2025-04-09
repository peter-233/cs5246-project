import os
import spacy

from supporter.identifier.base_identifier import BaseIdentifier, IdentifyResult, IdentifyResultClazz


class PersonalizeIdentifier(BaseIdentifier):
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

    def __check_overlap(self, span: tuple[int, int], results: list[IdentifyResult]) -> bool:
        s1, e1 = span[0], span[1]
        for result in results:
            s2, e2 = result.start_inclusive, result.end_exclusive
            _s1, _e1, _s2, _e2 = (s1, e1, s2, e2) if s1 < s2 else (s2, e2, s1, e1)
            if _s2 < _e1:
                return True
        return False

    def identify(self, article: str) -> list[IdentifyResult]:
        tokens = self.nlp(article)
        results: list[IdentifyResult] = []
        for ent in tokens.ents:
            results.append(IdentifyResult(
                start_inclusive=ent.start_char,
                end_exclusive=ent.end_char+1,
                text=ent.text,
                clazz=IdentifyResultClazz.NER,
                hard_level=None,
                token=None,
                label=ent.label_,
            ))

        for token in tokens:
            if token.pos_ not in self.HARD_POS:
                continue
            if token.lemma_ in self.easy_words:
                continue

            span = (token.idx, token.idx + len(token.text))
            if self.__check_overlap(span, results):
                continue

            result = IdentifyResult(
                start_inclusive=token.idx,
                end_exclusive=token.idx + len(token.text),
                text=token.text,
                clazz=IdentifyResultClazz.HARD,
                hard_level=1.0,
                token=token,
                label=None,
            )
            results.append(result)
        return results
