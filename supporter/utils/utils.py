from __future__ import annotations

from nltk.corpus import wordnet as wn


class POSConverter:
    NLTK_FORMAT = 1
    SPACY_FORMAT = 2
    WORDNET_FORMAT = 3
    COCA_FORMAT = 4

    def __init__(self):
        self.pos = None

        self.NLTK_ENCODE_MAP = {
            "NOUN": "n",
            "VERB": "v",
            "ADJ": "a",
            "ADV": "r",
            "ADJ_SAT": "s"
        }
        self.NLTK_DECODE_MAP = {v: k for k, v in self.NLTK_ENCODE_MAP.items()}

        self.SPACY_ENCODE_MAP = {
            "NOUN": "NOUN",
            "VERB": "VERB",
            "ADJ": "ADJ",
            "ADV": "ADV",
            "ADJ_SAT": "ADJ",
        }
        self.SPACY_DECODE_MAP = {v: k for k, v in self.SPACY_ENCODE_MAP.items() if k != "ADJ_SAT"}

        self.WORDNET_ENCODE_MAP = {
            "NOUN": wn.NOUN,
            "VERB": wn.VERB,
            "ADJ": wn.ADJ,
            "ADV": wn.ADV,
            "ADJ_SAT": wn.ADJ_SAT,
        }
        self.WORDNET_DECODE_MAP = {v: k for k, v in self.WORDNET_ENCODE_MAP.items()}

        self.COCA_ENCODE_MAP = {
            "NOUN": "N",
            "VERB": "V",
            "ADJ": "J",
            "ADV": "R",
        }
        self.COCA_DECODE_MAP = {v: k for k, v in self.COCA_ENCODE_MAP.items()}

    def encode(self, format: int):
        """
        encode(i.e. map) the POS value inside the class to the target format

        Args:
            format: target POS format

        Returns:
            target format's POS value

        """
        if format == POSConverter.NLTK_FORMAT:
            return self.NLTK_ENCODE_MAP[self.pos]
        elif format == POSConverter.SPACY_FORMAT:
            return self.SPACY_ENCODE_MAP[self.pos]
        elif format == POSConverter.WORDNET_FORMAT:
            return self.WORDNET_ENCODE_MAP[self.pos]
        elif format == POSConverter.COCA_FORMAT:
            return self.COCA_ENCODE_MAP[self.pos]
        else:
            raise ValueError(f"Invalid format: {format}")

    def decode(self, pos: str, format: int) -> POSConverter:
        """
        decode(i.e. map) the POS value from the target format to the class value

        Args:
            pos: POS value
            format: the given format

        Returns:
            self, which can be immediately used to encode() call
        """
        if format == POSConverter.NLTK_FORMAT:
            self.pos = self.NLTK_DECODE_MAP[pos]
        elif format == POSConverter.SPACY_FORMAT:
            self.pos = self.SPACY_DECODE_MAP[pos]
        elif format == POSConverter.WORDNET_FORMAT:
            self.pos = self.WORDNET_DECODE_MAP[pos]
        elif format == POSConverter.COCA_FORMAT:
            self.pos = self.COCA_DECODE_MAP[pos]
        else:
            raise ValueError(f"Invalid format: {format}")
        return self


def extract_sentence_by_word_position(article: str, start_pos: int, end_pos: int) -> tuple[int, int]:
    """
    extract the sentence containing the given word positions from the article

    Args:
        article: text of full article
        start_pos: word start position (inclusive)
        end_pos: word end position (exclusive)

    Returns:
        sentence start position (inclusive), sentence end position (exclusive)
    """
    if start_pos < 0 or end_pos > len(article) or start_pos >= end_pos:
        raise ValueError("Invalid word positions")

    sentence_endings = ['.', '!', '?']

    sentence_start = start_pos
    while sentence_start > 0:
        if article[sentence_start - 1] in sentence_endings and (
                sentence_start == len(article) or
                article[sentence_start] == ' ' or
                article[sentence_start] == '\n'
        ):
            break
        sentence_start -= 1

    sentence_end = end_pos
    while sentence_end < len(article):
        if article[sentence_end] in sentence_endings:
            sentence_end += 1
            break
        sentence_end += 1

    return sentence_start, sentence_end
