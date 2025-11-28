"""Utility library to load the underlying json library.

Imports `orjson` if it is present, otherwise it imports `json` from
the standard library.
"""

import typing as t

from json_arrays import _types, files


def get_backend(backend_name: str) -> t.Any:
    """Import the backend named `backend`."""
    import importlib  # noqa: PLC0415

    return importlib.import_module(f"json_arrays.jsonlib.backends.{backend_name}")


def _default_backend() -> t.Any:
    for backend_name in ("be_orjson", "be_json"):
        try:
            return get_backend(backend_name)
        except ImportError:  # noqa: PERF203
            continue
    raise ImportError("no backends available")


backend = _default_backend()
del _default_backend

dumps = backend.dumps  # type: ignore
loads = backend.loads  # type: ignore


def load_from_file(file_name: _types.Pathlike, file_mode: str = "rb", **kwargs: t.Any) -> t.Any:
    """Load the JSON file with the given file_name.

    Args:
        file_name: name of the file to load from.
        file_mode: mode to open the file in (must include `b`), defaults to `rb`
        kwargs: keyword arguments to loads

    Returns:
        the loaded JSON file.
    """
    with files.open_file(file_name, file_mode) as fp:
        return loads(fp.read(), **kwargs)


def dump_to_file(
    obj: t.Any, file_name: _types.Pathlike, file_mode: str = "wb", **kwargs: t.Any
) -> t.Any:
    """Dump to a JSON file with the given file name.

    Args:
        obj: the object to dump.
        file_name: name of the file to dump to.
        file_mode: mode to open the file with (must contain `b`), defaults to `wb`
        kwargs: keyword arguments that is passed to `dumps` from the backend

    Returns:
        anything returned from the backend.
    """
    with files.open_file(file_name, file_mode) as fp:
        return fp.write(dumps(obj, **kwargs))
