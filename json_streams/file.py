import builtins
import gzip

from json_streams import types, utility


def open(file_name: types.Pathlike, mode = "rb"): # -> types.File:
    if utility.is_gzip(file_name):
        return gzip.GzipFile(file_name, mode)
    else:
        return builtins.open(file_name, mode)

