"""Handle JSON or JSON_LINES lazily."""
import sys
import typing
from typing import BinaryIO, Iterable, Optional

from json_streams import encoders, json_iter, jsonl_iter, types, utility

__all__ = ["encoders", "json_iter", "jsonl_iter", "types", "utility"]


def choose_iter(name, json_format: Optional[utility.JsonFormat]):
    if json_format == utility.JsonFormat.JSON_LINES or utility.is_jsonl(name):
        return jsonl_iter
    return json_iter


def load(fp: BinaryIO, *, json_format: Optional[utility.JsonFormat] = None) -> Iterable:
    _iter = choose_iter(utility.get_name_of_file(fp), json_format)

    yield from _iter.load(fp)


def load_from_file(
    file_name: typing.Optional[types.Pathlike],
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
        _iter = choose_iter(file_name, json_format)

        yield from _iter.load_from_file(file_name, file_mode=file_mode, **kwargs)

    elif use_stdin_as_default:
        yield from jsonl_iter.load(sys.stdin.buffer, **kwargs)
    else:
        raise ValueError("You can't read from a empty file")


def dump(in_iter_, fp: BinaryIO, *, json_format: Optional[utility.JsonFormat] = None):
    _iter = choose_iter(utility.get_name_of_file(fp), json_format)

    _iter.dump(in_iter_, fp)


def dump_to_file(
    in_iter_,
    file_name: typing.Optional[types.Pathlike],
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
        _iter = choose_iter(file_name, json_format)

        _iter.dump_to_file(in_iter_, file_name, file_mode=file_mode, **kwargs)

    elif use_stdout_as_default:
        jsonl_iter.dump(in_iter_, sys.stdout.buffer, **kwargs)
    elif use_stderr_as_default:
        jsonl_iter.dump(in_iter_, sys.stderr.buffer, **kwargs)
    else:
        raise ValueError("file_name can't be empty")


def sink(fp: BinaryIO, *, json_format: Optional[utility.JsonFormat] = None):
    _iter = choose_iter(utility.get_name_of_file(fp), json_format)

    return _iter.sink(fp)


def sink_from_file(
    file_name: typing.Optional[types.Pathlike],
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
        if use_stdout_as_default:
            return jsonl_iter.sink(sys.stdout.buffer)
        if use_stderr_as_default:
            return jsonl_iter.sink(sys.stderr.buffer)
        raise ValueError("file_name can't be empty")

    _iter = choose_iter(file_name, json_format)

    return _iter.sink_from_file(file_name, file_mode=file_mode)
