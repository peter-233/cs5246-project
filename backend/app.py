import dataclasses
import json

from flask import Flask
from flask import Response
from flask import request
from flask_cors import CORS

from backend.utils import identify_explains_to_result
from supporter.embedder import BertEmbedder
from supporter.explainer import SimilarityHardExplainer, ExplainPipeline, SpacyLinkerNERExplainer
from supporter.explainer.base_explainer import ExplainResult
from supporter.identifier import PersonalizeHardIdentifier, IdentifyResult, SpacyLinkerNERIdentifier
from supporter.identifier.identify_pipeline import IdentifyPipeline

app = Flask(__name__)
CORS(app)

identify_pipeline = IdentifyPipeline(
    SpacyLinkerNERIdentifier(),
    PersonalizeHardIdentifier(),
)
explain_pipeline = ExplainPipeline(
    SpacyLinkerNERExplainer(),
    SimilarityHardExplainer(BertEmbedder()),
)


@app.route('/api/parse-result', methods=['POST'])
def parse_result():
    json_data: dict[any, any] = request.get_json()
    article: str = json_data['text']

    identify_results = identify_pipeline.execute(article)
    identify_explains: list[tuple[IdentifyResult, dict[str, ExplainResult]]] = list()
    for identify_result in identify_results:
        explain_result = explain_pipeline.execute(article, identify_result)
        if explain_result == {}:
            continue
        identify_explains.append((identify_result, explain_result))

    result_vo = identify_explains_to_result(identify_explains)
    result_vo_json = json.dumps(dataclasses.asdict(result_vo))
    return Response(result_vo_json, mimetype='application/json')


if __name__ == '__main__':
    app.run()
