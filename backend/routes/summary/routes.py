import dataclasses
import json

from flask import Blueprint, request, Response, g

from backend.models import ResultVo, ResultType, ResultCodeEnum
from backend.ponds import main_pond, summarizer_factory

summary_bp = Blueprint('summary', __name__)


@summary_bp.before_request
def before_request():
    summarizer = main_pond.borrow(summarizer_factory)
    g.summarizer = summarizer
    g.core_summarizer = summarizer.use().summarizer


@summary_bp.teardown_request
def teardown_request(exception):
    g.core_summarizer = None
    summarizer, g.summarizer = g.summarizer, None
    main_pond.recycle(summarizer, summarizer_factory)


@summary_bp.route('/api/summary', methods=['POST'])
def parse_result():
    json_data: dict[any, any] = request.get_json()
    article: str = json_data['text']

    # generate a summary here
    summary = g.core_summarizer.summarize(article)
    data = {
        "summary": summary
    }

    result_vo = ResultVo(ResultType.SUCCESS, data, rce=ResultCodeEnum.SUCCESS)
    result_vo_json = json.dumps(dataclasses.asdict(result_vo))
    return Response(result_vo_json, mimetype='application/json')
