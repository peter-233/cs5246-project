import dataclasses
import json

from flask import Blueprint, Response, request, g

from backend.ponds import main_pond, pipelines_factory
from backend.utils import identify_explains_to_result
from supporter.explainer.base_explainer import ExplainResult
from supporter.identifier import IdentifyResult

parse_result_bp = Blueprint('parse-result', __name__)


@parse_result_bp.before_request
def before_request():
    pipelines = main_pond.borrow(pipelines_factory)
    g.pipelines = pipelines
    g.identify_pipeline = pipelines.use().identify_pipeline
    g.explain_pipeline = pipelines.use().explain_pipeline


@parse_result_bp.teardown_request
def teardown_request(exception):
    g.identify_pipeline = None
    g.explain_pipeline = None
    pipelines, g.pipelines = g.pipelines, None
    main_pond.recycle(pipelines, pipelines_factory)


@parse_result_bp.route('/api/parse-result', methods=['POST'])
def parse_result():
    json_data: dict[any, any] = request.get_json()
    article: str = json_data['text']
    identify_pipeline = g.identify_pipeline
    explain_pipeline = g.explain_pipeline
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
