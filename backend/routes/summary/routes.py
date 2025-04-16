import dataclasses
import json

from flask import Blueprint, request, Response

from backend.models import ResultVo, ResultType, ResultCodeEnum

parse_result_bp = Blueprint('summary', __name__)


@parse_result_bp.route('/api/summary', methods=['POST'])
def parse_result():
    json_data: dict[any, any] = request.get_json()
    article: str = json_data['text']

    # generate a summary here
    summary = "this is a test summary"
    data = {
        "summary": summary
    }

    result_vo = ResultVo(ResultType.SUCCESS, data, rce=ResultCodeEnum.SUCCESS)
    result_vo_json = json.dumps(dataclasses.asdict(result_vo))
    return Response(result_vo_json, mimetype='application/json')
