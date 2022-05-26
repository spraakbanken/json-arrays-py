import builtins
import gzip

from json_streams import types, utility

# pylint: disable=redefining-builtins

def open(file_name: types.Pathlike, mode = "rb") -> types.File:
    assert "b" in mode
    if utility.is_gzip(file_name):
        return gzip.GzipFile(file_name, mode)
    else:
        return builtins.open(file_name, mode)

