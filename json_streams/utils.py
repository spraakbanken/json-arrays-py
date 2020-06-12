"""Util functions.
"""
import os
from typing import IO

from typing import Union


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
