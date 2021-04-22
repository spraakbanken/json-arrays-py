"""Util functions.
"""
from enum import Enum
import os
from typing import Any, Generator, IO, Union


def get_name_of_file(fp: IO) -> str:
    if hasattr(fp, "name"):
        return fp.name
    return ""


def is_jsonl(name: str) -> bool:
    """Test if a filename is json lines.
    Also returns True for '<stdin>' and '<stdout>'.

    Arguments:
        name {str} -- name to test

    Returns:
        {bool} -- True if this name is jsonl.
    """
    if name in ["<stdin>", "<stdout>"]:
        return True
    _, suffix = os.path.splitext(name)
    # print('suffix = {suffix}'.format(suffix=suffix))
    return suffix in [".jsonl"]


def to_bytes(s: Union[str, bytes, bytearray]) -> Union[bytes, bytearray]:
    """Convert str to bytes, otherwise pass through s

    Args:
        s (Union[str, bytes, bytearray]): the argument to assure bytes

    Returns:
        Union[bytes, bytearray]: the possible converted argument
    """
    if isinstance(s, (bytes, bytearray)):
        return s
    else:
        return s.encode("utf-8")


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
