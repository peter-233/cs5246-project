from spacy_entity_linker.EntityElement import EntityElement

from supporter.explainer.base_explainer import BaseExplainer, ExplainResult, ExplainResultClazz
from supporter.identifier.base_identifier import IdentifyResult, IdentifyResultClazz

def get_wikipedia_link(entity: EntityElement) -> str:
    return f"https://en.wikipedia.org/wiki/{entity.get_label()}"

class SpacyLinkerNERExplainer(BaseExplainer):

    def explain(self, article: str, identify_result: IdentifyResult) -> dict[str, ExplainResult]:
        if identify_result.clazz != IdentifyResultClazz.NER:
            return {}

        return {
            "ext_link": ExplainResult(
                clazz=ExplainResultClazz.EXT_LINK,
                content=get_wikipedia_link(identify_result.entity),
            ),
            "ner_label": ExplainResult(
                clazz=ExplainResultClazz.NER_LABEL,
                content=identify_result.label,
            ),
        }