"""Util functions."""

import os
from enum import Enum
from typing import Any, Generator, Union

from json_arrays import _types

# pylint: disable=unsubscriptable-object


def get_name_of_file(fp: _types.File) -> str:
    return fp.name if hasattr(fp, "name") else ""


def is_jsonl(name: _types.Pathlike) -> bool:
    """Test if a filename is json lines.
    Also returns True for '<stdin>' and '<stdout>'.

    Arguments:
        name {str} -- name to test

    Returns:
        {bool} -- True if this name is jsonl.
    """
    if name in ["<stdin>", "<stdout>"]:
        return True
    base, suffix = os.path.splitext(str(name))
    if suffix in [".gz", ".bz2"]:
        _, suffix = os.path.splitext(base)
    # print('suffix = {suffix}'.format(suffix=suffix))
    return suffix in [".jsonl", ".jl", ".ndjson"]


def is_gzip(name: _types.Pathlike) -> bool:
    """Test if a filename is gzip."""
    _, suffix = os.path.splitext(str(name))
    return suffix == ".gz"


def is_bzip2(name: _types.Pathlike) -> bool:
    """Test if a filename is gzip."""
    _, suffix = os.path.splitext(str(name))
    return suffix == ".bz2"


def to_bytes(s: Union[str, bytes, bytearray]) -> Union[bytes, bytearray]:
    """Convert str to bytes, otherwise pass through s

    Args:
        s (Union[str, bytes, bytearray]): the argument to assure bytes

    Returns:
        Union[bytes, bytearray]: the possible converted argument
    """
    return s if isinstance(s, (bytes, bytearray)) else s.encode("utf-8")


class Sink:
    def __init__(self, sink: Generator[None, Any, None]):
        self.sink = sink

    def __enter__(self):
        next(self.sink)
        return self.sink

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.sink.close()


class JsonFormat(str, Enum):
    JSON = "json"
    JSON_LINES = "jsonl"
