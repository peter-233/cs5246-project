from supporter.explainer.base_explainer import BaseExplainer, ExplainResult
from supporter.identifier.base_identifier import IdentifyResult


class ExplainPipeline:
    explain_sequence: list[BaseExplainer] = list()

    def __init__(self, *explainers: BaseExplainer):
        self.explain_sequence = list(explainers)

    def execute(self, article: str, identify_result: IdentifyResult) -> dict[str, ExplainResult]:
        """
        follow the explainer sequence to explain the identify_result.
        Note that the explanation behind will overwrite the explanation before.

        Args:
            article: the article to explain
            identify_result: the result of identify

        Returns:
            the explanations of the identify_result
        """
        result = dict()

        for explainer in self.explain_sequence:
            result.update(explainer.explain(article, identify_result))

        return result
