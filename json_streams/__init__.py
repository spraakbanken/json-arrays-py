""" Handle JSON or JSON_LINES lazily. """
from pathlib import Path
from typing import Iterable, Optional
from typing import BinaryIO

from . import json_iter
from . import jsonl_iter
from . import utils


def choose_iter(name, json_format: Optional[utils.JsonFormat]):
    if json_format == utils.JsonFormat.JSON_LINES or utils.is_jsonl(name):
        return jsonl_iter
    return json_iter


def load(fp: BinaryIO, *, json_format: Optional[utils.JsonFormat] = None) -> Iterable:
    _iter = choose_iter(utils.get_name_of_file(fp), json_format)

    yield from _iter.load(fp)


def load_from_file(
    file_name: Path,
    *,
    json_format: Optional[utils.JsonFormat] = None,
    file_mode: str = "br"
) -> Iterable:
    _iter = choose_iter(file_name, json_format)

    yield from _iter.load_from_file(file_name, file_mode=file_mode)


def dump(in_iter_, fp: BinaryIO, *, json_format: Optional[utils.JsonFormat] = None):
    _iter = choose_iter(utils.get_name_of_file(fp), json_format)

    _iter.dump(in_iter_, fp)


def dump_to_file(
    in_iter_,
    file_name: Path,
    *,
    json_format: Optional[utils.JsonFormat] = None,
    file_mode: str = "bw"
):
    _iter = choose_iter(file_name, json_format)

    _iter.dump_to_file(in_iter_, file_name, file_mode=file_mode)


def sink(fp: BinaryIO, *, json_format: Optional[utils.JsonFormat] = None):
    _iter = choose_iter(utils.get_name_of_file(fp), json_format)

    return _iter.sink(fp)


def sink_from_file(
    file_name: Path,
    *,
    json_format: Optional[utils.JsonFormat] = None,
    file_mode: str = "bw"
):
    _iter = choose_iter(file_name, json_format)

    return _iter.sink_from_file(file_name, file_mode=file_mode)
