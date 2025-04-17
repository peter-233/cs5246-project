import dataclasses
import json

from flask import Blueprint, request, Response

from backend.models import ResultVo, ResultType, ResultCodeEnum
from supporter.utils import fetch_article

fetch_article_bp = Blueprint('summary', __name__)


@fetch_article_bp.route('/api/summary', methods=['GET'])
def parse_result():
    url: str = request.args.get('url')

    article = fetch_article(url)
    data = {
        "article": article,
    }

    result_vo = ResultVo(ResultType.SUCCESS, data, rce=ResultCodeEnum.SUCCESS)
    result_vo_json = json.dumps(dataclasses.asdict(result_vo))
    return Response(result_vo_json, mimetype='application/json')
