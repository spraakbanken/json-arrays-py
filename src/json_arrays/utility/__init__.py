"""Util functions."""

import os
import typing as t
from collections.abc import Generator
from enum import Enum

from json_arrays import _types


def get_name_of_file(fp: _types.File | None) -> str:
    """Return the name if fp has the attribute 'name' otherwise empty string."""
    return str(fp.name) if fp and hasattr(fp, "name") else ""


def is_jsonl(name: _types.Pathlike) -> bool:
    """Test if a filename is json lines.

    Also returns True for '<stdin>' and '<stdout>'.

    Arguments:
        name: name to test

    Returns:
        True if this name is jsonl.
    """
    if name in {"<stdin>", "<stdout>"}:
        return True
    base, suffix = os.path.splitext(str(name))  # noqa: PTH122
    if suffix in {".gz", ".bz2"}:
        _, suffix = os.path.splitext(base)  # noqa: PTH122
    # print('suffix = {suffix}'.format(suffix=suffix))
    return suffix in {".jsonl", ".jl", ".ndjson"}


def is_gzip(name: _types.Pathlike) -> bool:
    """Test if a filename is gzip."""
    _, suffix = os.path.splitext(str(name))  # noqa: PTH122
    return suffix == ".gz"


def is_bzip2(name: _types.Pathlike) -> bool:
    """Test if a filename is bzip2."""
    _, suffix = os.path.splitext(str(name))  # noqa: PTH122
    return suffix == ".bz2"


def to_bytes(s: str | bytes | bytearray) -> bytes | bytearray:
    """Convert str to bytes, otherwise pass through.

    Args:
        s: the argument to assure bytes

    Returns:
         the possible converted argument
    """
    return s if isinstance(s, bytes | bytearray) else s.encode("utf-8")


class Sink:
    """A utility that wraps a co-routine, and closes it."""

    def __init__(self, sink: Generator[None, t.Any, None]) -> None:
        """Wrap the given sink."""
        self.sink = sink

    def __enter__(self) -> Generator[None, t.Any, None]:
        """Prepare the generator and return it."""
        next(self.sink)
        return self.sink

    def __exit__(self, exc_type: t.Any, exc_value: t.Any, exc_traceback: t.Any) -> None:
        """Call close on the wrapped generator."""
        self.sink.close()


class JsonFormat(str, Enum):
    """Format of json."""

    JSON = "json"
    JSON_LINES = "jsonl"
