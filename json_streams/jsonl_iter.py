""" Handle JSON-LINES lazily. """
import gzip
from typing import Dict
from typing import BinaryIO
from typing import Iterable
from typing import Union

from json_streams import jsonlib
from json_streams import utility
from json_streams.utility import types

# pylint: disable=unsubscriptable-object


def dump(data: Union[Dict, Iterable], fp: BinaryIO, **kwargs):

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


def load(fp: BinaryIO, **kwargs) -> Iterable:
    for line in fp:
        yield jsonlib.loads(line, **kwargs)


def load_from_file(file_name: types.Pathlike, *, file_mode: str = None, **kwargs):
    if not file_mode:
        file_mode = "br"
    assert "b" in file_mode
    if utility.is_gzip(file_name):
        with gzip.open(file_name) as fp_gz:
            yield from load(fp_gz, **kwargs)
    else:
        with open(file_name, file_mode) as fp:
            yield from load(fp, **kwargs)  # type: ignore


def dump_to_file(obj, file_name: types.Pathlike, *, file_mode: str = None, **kwargs):
    if not file_mode:
        file_mode = "wb"
    assert "b" in file_mode
    if utility.is_gzip(file_name):
        with gzip.open(file_name, file_mode) as fp_gz:
            dump(obj, fp_gz, **kwargs)
    else:
        with open(file_name, file_mode) as fp:
            dump(obj, fp, **kwargs)  # type: ignore


def sink(fp: BinaryIO):
    return utility.Sink(jsonl_sink(fp))


def sink_from_file(file_name: types.Pathlike, *, file_mode: str = None):
    if not file_mode:
        file_mode = "wb"
    assert "b" in file_mode
    if utility.is_gzip(file_name):
        fp = gzip.GzipFile(file_name, mode=file_mode)
    else:
        fp = open(file_name, file_mode)

    return utility.Sink(jsonl_sink(fp, close_file=True))  # type: ignore


def jsonl_sink(fp: BinaryIO, *, close_file: bool = False):
    try:
        while True:
            value = yield
            fp.write(jsonlib.dumps(value))
            fp.write(b"\n")
    except GeneratorExit:
        pass
    if close_file:
        fp.close()
