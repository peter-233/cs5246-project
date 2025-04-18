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
    g.lda_summarizer = summarizer.use().lda_summarizer
    g.textrank_summarizer = summarizer.use().textrank_summarizer
    g.lsa_summarizer = summarizer.use().lsa_summarizer
    g.bart_summarizer = summarizer.use().bart_summarizer


@summary_bp.teardown_request
def teardown_request(exception):
    g.lda_summarizer = None
    g.textrank_summarizer = None
    g.lsa_summarizer = None
    g.bart_summarizer = None
    summarizer, g.summarizer = g.summarizer, None
    main_pond.recycle(summarizer, summarizer_factory)


@summary_bp.route('/api/summary', methods=['POST'])
def parse_result():
    json_data: dict[any, any] = request.get_json()
    article: str = json_data['text']
    method: str = json_data['method']

    # generate a summary here
    if method == 'lda':
        summary = g.lda_summarizer.summarize(article)
    elif method == 'textrank':
        summary = g.textrank_summarizer.summarize(article)
    elif method == 'lsa':
        summary = g.lsa_summarizer.summarize(article)
    elif method == 'bart':
        summary = g.bart_summarizer.summarize(article)
    else:
        raise ValueError(f'method not supported: {method}')

    data = {
        "summary": summary
    }

    result_vo = ResultVo(ResultType.SUCCESS, data, rce=ResultCodeEnum.SUCCESS)
    result_vo_json = json.dumps(dataclasses.asdict(result_vo))
    return Response(result_vo_json, mimetype='application/json')
