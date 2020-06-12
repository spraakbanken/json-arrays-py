"""
Utility library to load the underlying json library.

Imports `orjson` or `ujson` if either is present, otherwise it imports `json` from
the standard library.
"""
try:
    from orjson import dumps, loads

    PREFERRED_READ_MODE = "br"
    PREFERRED_WRITE_MODE = "bw"
except ImportError:
    try:
        from ujson import dumps, loads  # pylint: disable=unused-import

        PREFERRED_READ_MODE = "br"
        PREFERRED_WRITE_MODE = "bw"
    except ImportError:
        from json import dumps, loads  # noqa: F401

        PREFERRED_READ_MODE = "r"
        PREFERRED_WRITE_MODE = "w"


def load_from_file(file_name: str):
    """
    Load the JSON file with the given file_name.

    :param file_name: name of the file to load from.
    :return: the loaded JSON file.
    """
    with open(file_name, PREFERRED_READ_MODE) as fp:
        return loads(fp.read())


def dump_to_file(obj, file_name: str):
    """
    Dump to a JSON file with the given file name.

    :param obj: the object to dump.
    :param file_name: name of the file to dump to.
    :return: anything returned from the backend.
    """
    with open(file_name, PREFERRED_WRITE_MODE) as fp:
        return fp.write(dumps(obj))
