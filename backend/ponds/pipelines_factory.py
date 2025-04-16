import dataclasses
from typing import Any

from pond import PooledObjectFactory, PooledObject

from supporter.embedder import BertEmbedder
from supporter.explainer import ExplainPipeline, SpacyLinkerNERExplainer, SimilarityHardExplainer
from supporter.identifier import IdentifyPipeline, SpacyLinkerNERIdentifier, PersonalizeHardIdentifier


@dataclasses.dataclass
class Pipelines:
    identify_pipeline: IdentifyPipeline
    explain_pipeline: ExplainPipeline


class PipelinesFactory(PooledObjectFactory):
    def createInstance(self) -> PooledObject:
        identify_pipeline = IdentifyPipeline(
            SpacyLinkerNERIdentifier(),
            PersonalizeHardIdentifier(),
        )
        explain_pipeline = ExplainPipeline(
            SpacyLinkerNERExplainer(),
            SimilarityHardExplainer(BertEmbedder()),
        )
        p = Pipelines(identify_pipeline, explain_pipeline)
        return PooledObject(p)

    def destroy(self, pooled_object: PooledObject) -> None:
        del pooled_object

    def reset(self, pooled_object: PooledObject, **kwargs: Any) -> PooledObject:
        return pooled_object

    def validate(self, pooled_object: PooledObject) -> bool:
        return True


pipelines_factory = PipelinesFactory(pooled_maxsize=1, least_one=True)
