from dataclasses import dataclass
from enum import Enum


@dataclass
class ResultCodeEnumItem:
    code: int
    msg: str

    def __init__(self, code: int, msg: str):
        self.code = code
        self.msg = msg


class ResultCodeEnum(Enum):
    SUCCESS = ResultCodeEnumItem(200, 'operation succeed.')
    ERROR = ResultCodeEnumItem(500, 'operation failed, server internal error.')


class ResultType(Enum):
    SUCCESS = 'success'
    ERROR = 'error'
    WARNING = 'warning'
    INFO = 'info'
    NONE = 'none'


@dataclass
class ResultVo:
    type: str = 'none'
    code: int = 0
    data: any = None
    msg: str = ''

    def __init__(self, _type: ResultType, data: any, code: int = None, msg: str = None, rce: ResultCodeEnum = None):
        self.type = _type.value
        self.data = data

        if rce is not None:
            self.code = rce.value.code
            self.msg = rce.value.msg
        elif code is not None and msg is not None:
            self.code = code
            self.msg = msg
        else:
            raise Exception('unable to solve ResultVo code and msg.')
