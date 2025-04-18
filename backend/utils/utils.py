import dataclasses
import json

from flask import Response

from backend.models.explain_vo import ExplainVo
from backend.models.parse_result_vo import ParseResultVo
from backend.models.result_vo import ResultVo, ResultType, ResultCodeEnum
from supporter.explainer.base_explainer import ExplainResult
from supporter.identifier import IdentifyResult


def identify_explains_to_result(identify_explains: list[tuple[IdentifyResult, dict[str, ExplainResult]]]) -> ResultVo:
    parse_result_vo_list: list[ParseResultVo] = list()
    for identify_result, explains in identify_explains:
        explain_vo_list: list[ExplainVo] = [ExplainVo(explain.clazz, explain.content) for explain in explains.values()]
        parse_result_vo = ParseResultVo(identify_result.clazz, identify_result.start_inclusive,
                                        identify_result.end_exclusive, explain_vo_list)
        parse_result_vo_list.append(parse_result_vo)

    result_vo = ResultVo(ResultType.SUCCESS, parse_result_vo_list, rce=ResultCodeEnum.SUCCESS)
    return result_vo

def generate_internal_error_response(err: any) -> Response:
    result_vo = ResultVo(ResultType.ERROR, str(err), rce=ResultCodeEnum.ERROR)
    result_vo_json = json.dumps(dataclasses.asdict(result_vo))
    return Response(result_vo_json, mimetype='application/json')

