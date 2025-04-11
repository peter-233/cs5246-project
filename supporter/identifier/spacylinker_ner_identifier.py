import spacy
from spacy.tokens import Token, Span
from spacy_entity_linker.EntityCollection import EntityCollection
from spacy_entity_linker.EntityElement import EntityElement

from supporter.identifier.base_identifier import BaseIdentifier, IdentifyResultClazz, IdentifyResult


def get_span_idx(start_inclusive: int, end_exclusive: int, results: list[IdentifyResult]) -> int:
    """
    find the overlapped span in identify result list

    Args:
        start_inclusive: span start index (inclusive)
        end_exclusive: span end index (exclusive)
        results: identify result list

    Returns:
        index of the first overlapped span in identify result list, -1 if not found
    """
    idx = -1
    for i, result in enumerate(results):
        s1, e1 = start_inclusive, end_exclusive
        s2, e2 = result.start_inclusive, result.end_exclusive
        _s1, _e1, _s2, _e2 = (s1, e1, s2, e2) if s1 < s2 else (s2, e2, s1, e1)
        if _s2 < _e1:
            idx = i
            break
    return idx


# https://github.com/egerber/spacy-entity-linker
class SpacyLinkerNERIdentifier(BaseIdentifier):
    nlp: spacy.Language

    def __init__(self):
        super().__init__()
        self.nlp = spacy.load("en_core_web_sm")
        self.nlp.add_pipe("entityLinker", last=True)

    def identify(self, article: str) -> list[IdentifyResult]:
        identify_results: list[IdentifyResult] = list()

        doc = self.nlp(article)
        all_linked_entities: EntityCollection = doc._.linkedEntities
        for ent in all_linked_entities:
            assert isinstance(ent, EntityElement)
            span: Span = ent.get_span()
            start_idx = doc[span.start].idx
            end_idx = doc[span.end - 1].idx + len(doc[span.end - 1].text)
            identify_results.append(IdentifyResult(
                start_inclusive=start_idx,
                end_exclusive=end_idx,
                text=span.text,
                clazz=IdentifyResultClazz.NER,
                hard_level=None,
                token=None,
                label=ent.get_label(),
                entity=ent
            ))

        identify_results, linker_results = list(), identify_results
        for ent in doc.ents:
            assert isinstance(ent, Span)
            start_idx = doc[ent.start].idx
            end_idx = doc[ent.end - 1].idx + len(doc[ent.end - 1].text)
            idx = get_span_idx(start_idx, end_idx, linker_results)
            if idx >= 0:
                linker_identify_result = linker_results[idx]
                identify_result = IdentifyResult(
                    start_inclusive=linker_identify_result.start_inclusive,
                    end_exclusive=linker_identify_result.end_exclusive,
                    text=linker_identify_result.text,
                    clazz=linker_identify_result.clazz,
                    hard_level=linker_identify_result.hard_level,
                    token=linker_identify_result.token,
                    label=spacy.explain(ent.label_),
                    entity=linker_identify_result.entity
                )
                identify_results.append(identify_result)

        return identify_results
