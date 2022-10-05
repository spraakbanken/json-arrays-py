import builtins
import gzip

from json_streams import types, utility

# pylint: disable=redefined-builtin

def open(file_name: types.Pathlike, mode = "rb") -> types.File:
    assert "b" in mode
    if utility.is_gzip(file_name):
        return gzip.GzipFile(file_name, mode)  # type: ignore
    else:
        return builtins.open(file_name, mode)

