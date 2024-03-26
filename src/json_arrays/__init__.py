"""Handle JSON or JSON_LINES lazily."""

import sys
import typing
from typing import BinaryIO, Iterable, Optional

from json_arrays import _types, encoders, json_iter, jsonl_iter, jsonlib, utility
from json_arrays.utility import JsonFormat

__all__ = [
    "encoders",
    "json_iter",
    "jsonl_iter",
    "jsonlib",
    "utility",
    "load",
    "load_from_file",
    "dump",
    "dump_to_file",
    "sink",
    "sink_from_file",
    "JsonFormat",
]


# pylint: disable=unsubscriptable-object
def _choose_iter(name, json_format: Optional[utility.JsonFormat]):
    if json_format == utility.JsonFormat.JSON_LINES or utility.is_jsonl(name):
        return jsonl_iter
    return json_iter


def load(fp: BinaryIO, *, json_format: Optional[utility.JsonFormat] = None) -> Iterable:
    """Dump an iterable to file-like object.

    Examples:
        Loading iterable in JSON format:
        >>> import io
        >>> import json_arrays
        >>> in_json = io.BytesIO(b'[{"a": 1}, {"a": 2}]')
        >>> iter = json_arrays.load(in_json)
        >>> list(iter)
        [{'a': 1}, {'a': 2}]

        Loading iterable in JSON_LINES format:
        >>> import io
        >>> import json_arrays
        >>> in_jsonl = io.BytesIO(b'{"a": 1}\\n{"a": 2}\\n')
        >>> iter = json_arrays.load(in_jsonl, json_format="jsonl")
        >>> list(iter)
        [{'a': 1}, {'a': 2}]
    """
    _iter = _choose_iter(utility.get_name_of_file(fp), json_format)

    yield from _iter.load(fp)


def load_from_file(
    file_name: typing.Optional[_types.Pathlike],
    *,
    json_format: Optional[utility.JsonFormat] = None,
    file_mode: str = "rb",
    use_stdin_as_default: bool = False,
    **kwargs,
) -> Iterable:
    """Lazily load from given file_name.

    Reads from stdin if `use_stdin_as_default` is set and file_name is falsy.

    Parameters:
        file_name : Path
            name of file to load from
        json_format : utility.JsonFormat, optional, default=None
            Explicit set format of json file
        file_mode : str, optional, default="rb"
            mode to open the file in.
        use_stdin_as_default : bool, optional, default=False
            reads from stdin if file_name is None

    Yields:
        JSON value
            lazily loaded from file
    """
    if file_name is not None:
        _iter = _choose_iter(file_name, json_format)

        yield from _iter.load_from_file(file_name, file_mode=file_mode, **kwargs)
    elif use_stdin_as_default:
        if json_format == JsonFormat.JSON:
            yield from json_iter.load(sys.stdin.buffer, **kwargs)
        else:
            yield from jsonl_iter.load(sys.stdin.buffer, **kwargs)
    else:
        raise ValueError("You must give a FILENAME or USE_STDIN_AS_DEFAULT=`True`")


def dump(in_iter_, fp: BinaryIO, *, json_format: Optional[utility.JsonFormat] = None):
    """Dump an iterable to BinaryIO-object.

    Examples:
        Dumping iterable in JSON format:
        >>> import io
        >>> import json_arrays
        >>> data = [{"a": 1}, {"a": 2}]
        >>> out_json = io.BytesIO()
        >>> json_arrays.dump(data, out_json)
        >>> out_json.getvalue()
        b'[{"a":1},{"a":2}]'

        Dumping iterable in JSON_LINES format:
        >>> import io
        >>> import json_arrays
        >>> data = [{"a": 1}, {"a": 2}]
        >>> out_jsonl = io.BytesIO()
        >>> json_arrays.dump(data, out_jsonl, json_format="jsonl")
        >>> out_jsonl.getvalue()
        b'{"a":1}\\n{"a":2}\\n'
    """
    _iter = _choose_iter(utility.get_name_of_file(fp), json_format)

    _iter.dump(in_iter_, fp)


def dump_to_file(
    in_iter_,
    file_name: typing.Optional[_types.Pathlike],
    *,
    json_format: Optional[utility.JsonFormat] = None,
    file_mode: str = "wb",
    use_stdout_as_default: bool = False,
    use_stderr_as_default: bool = False,
    **kwargs,
):
    """Open file and dump json to it.

    Parameters:
        in_iter_ : Iterable
            The data to dump.
        file_name : Path
            The path to write to
        json_format : utility.JsonFormat, optional, default=None
            the json format to write in.
        file_mode : str, optional, default="wb"
            the mode to open the file in.
        use_stdout_as_default : bool, optional, default=False
            use stdout if file_name is empty.
        use_stderr_as_default : bool, optional, default=False
            use stderr if file_name is empty.
    """
    if file_name is not None:
        _iter = _choose_iter(file_name, json_format)

        _iter.dump_to_file(in_iter_, file_name, file_mode=file_mode, **kwargs)

    elif use_stdout_as_default or use_stderr_as_default:
        buffer = sys.stdout.buffer if use_stdout_as_default else sys.stderr.buffer
        if json_format == JsonFormat.JSON:
            json_iter.dump(in_iter_, buffer, **kwargs)
        else:
            jsonl_iter.dump(in_iter_, buffer, **kwargs)
    else:
        raise ValueError(
            "You must give a FILENAME or USE_STDOUT_AS_DEFAULT=`True` or USE_STDERR_AS_DEFAULT=`True`"  # noqa: E501
        )


def sink(fp: BinaryIO, *, json_format: Optional[utility.JsonFormat] = None):
    _iter = _choose_iter(utility.get_name_of_file(fp), json_format)

    return _iter.sink(fp)


def sink_from_file(
    file_name: typing.Optional[_types.Pathlike],
    *,
    json_format: Optional[utility.JsonFormat] = None,
    file_mode: str = "wb",
    use_stdout_as_default: bool = False,
    use_stderr_as_default: bool = False,
):
    """Open file and use it as json sink.

    Args:
        file_name : Path
            the path to write to
        json_format : utility.JsonFormat, optional, default=None
            the json format to write in.
        file_mode : str, optional, default="wb"
            the mode to open the file in.
        use_stdout_as_default : bool, optional, default=False
            use stdout if file_name is empty.
        use_stderr_as_default : bool, optional, default=False
            use stderr if file_name is empty.
    """
    if not file_name:
        if use_stdout_as_default or use_stderr_as_default:
            buffer = sys.stdout.buffer if use_stdout_as_default else sys.stderr.buffer
            return (
                json_iter.sink(buffer)
                if json_format == JsonFormat.JSON
                else jsonl_iter.sink(buffer)
            )
        raise ValueError(
            "You must give a FILENAME or USE_STDOUT_AS_DEFAULT=`True` or USE_STDERR_AS_DEFAULT=`True`"  # noqa: E501
        )

    _iter = _choose_iter(file_name, json_format)

    return _iter.sink_from_file(file_name, file_mode=file_mode)
