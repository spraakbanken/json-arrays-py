""" Handle JSON-LINES lazily. """
from pathlib import Path
from typing import Dict
from typing import BinaryIO
from typing import Iterable
from typing import Union

from json_streams import jsonlib
from json_streams import utils

# pylint: disable=unsubscriptable-object


def dump(data: Union[Dict, Iterable], fp: BinaryIO):

    if isinstance(data, dict):
        fp.write(jsonlib.dumps(data))
        fp.write(b"\n")
        return

    try:
        for obj in data:
            fp.write(jsonlib.dumps(obj))
            fp.write(b"\n")
    except TypeError:
        fp.write(jsonlib.dumps(data))
        fp.write(b"\n")


def load(fp: BinaryIO) -> Iterable:
    for line in fp:
        yield jsonlib.loads(line)


def load_from_file(file_name: Path, *, file_mode: str = None):
    if not file_mode:
        file_mode = "br"
    assert "b" in file_mode
    with open(file_name, file_mode) as fp:
        yield from load(fp)  # type: ignore


def dump_to_file(obj, file_name: Path, *, file_mode: str = None):
    if not file_mode:
        file_mode = "bw"
    assert "b" in file_mode
    with open(file_name, file_mode) as fp:
        dump(obj, fp)  # type: ignore


def sink(fp: BinaryIO):
    return utils.Sink(jsonl_sink(fp))


def sink_from_file(file_name: Path, *, file_mode: str = None):
    if not file_mode:
        file_mode = "bw"
    assert "b" in file_mode
    fp = open(file_name, file_mode)
    return utils.Sink(jsonl_sink(fp, close_file=True))  # type: ignore


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
