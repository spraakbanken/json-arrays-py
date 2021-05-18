"""
Utility library to load the underlying json library.

Imports `orjson` or `ujson` if either is present, otherwise it imports `json` from
the standard library.
"""


def get_backend(backend_name: str):
    """Import the backend named `backend`"""
    import importlib

    return importlib.import_module(f"json_streams.backends.{backend_name}")


def _default_backend():
    for backend_name in ("be_orjson", "be_ujson", "be_json"):
        try:
            return get_backend(backend_name)
        except ImportError:
            continue
    raise ImportError("no backends available")


backend = _default_backend()
del _default_backend

dumps = backend.dumps  # type: ignore
loads = backend.loads  # type: ignore


def load_from_file(file_name: str):
    """
    Load the JSON file with the given file_name.

    :param file_name: name of the file to load from.
    :return: the loaded JSON file.
    """
    with open(file_name, "br") as fp:
        return loads(fp.read())


def dump_to_file(obj, file_name: str):
    """
    Dump to a JSON file with the given file name.

    :param obj: the object to dump.
    :param file_name: name of the file to dump to.
    :return: anything returned from the backend.
    """
    with open(file_name, "bw") as fp:
        return fp.write(dumps(obj))
