""" Handle JSON-LINES lazily. """
from typing import Iterable
from typing import Union

from json_streams import files, jsonlib
from json_streams import utility
from json_streams import types

# pylint: disable=unsubscriptable-object


def dump(data: Union[dict, Iterable], fp: types.File, **kwargs):

    if isinstance(data, dict):
        fp.write(jsonlib.dumps(data, **kwargs))
        fp.write(b"\n")
        return

    try:
        for obj in data:
            fp.write(jsonlib.dumps(obj, **kwargs))
            fp.write(b"\n")
    except TypeError:
        fp.write(jsonlib.dumps(data, **kwargs))
        fp.write(b"\n")


def load(fp: types.File, **kwargs) -> Iterable:
    for line in fp:
        yield jsonlib.loads(line, **kwargs)


def load_from_file(file_name: types.Pathlike, *, file_mode: str = "rb", **kwargs):
    with files.open_file(file_name, file_mode) as fp:
        yield from load(fp, **kwargs)  # type: ignore


def dump_to_file(obj, file_name: types.Pathlike, *, file_mode: str = "wb", **kwargs):
    with files.open_file(file_name, file_mode) as fp:
        dump(obj, fp, **kwargs)  # type: ignore


def sink(fp: types.File):
    return utility.Sink(jsonl_sink(fp))


def sink_from_file(file_name: types.Pathlike, *, file_mode: str = "wb"):
    fp = files.open_file(file_name, file_mode)

    return utility.Sink(jsonl_sink(fp, close_file=True))  # type: ignore


def jsonl_sink(fp: types.File, *, close_file: bool = False):
    try:
        while True:
            value = yield
            fp.write(jsonlib.dumps(value))
            fp.write(b"\n")
    except GeneratorExit:
        pass
    if close_file:
        fp.close()
