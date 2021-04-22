""" Handle JSON or JSON_LINES lazily. """
from pathlib import Path
from typing import Iterable, Optional
from typing import BinaryIO
import sys

from . import json_iter
from . import jsonl_iter
from . import utils


def choose_iter(name, json_format: Optional[utils.JsonFormat]):
    if json_format == utils.JsonFormat.JSON_LINES or utils.is_jsonl(name):
        return jsonl_iter
    return json_iter


def load(fp: BinaryIO, *, json_format: Optional[utils.JsonFormat] = None) -> Iterable:
    _iter = choose_iter(utils.get_name_of_file(fp), json_format)

    yield from _iter.load(fp)


def load_from_file(
    file_name: Path,
    *,
    json_format: Optional[utils.JsonFormat] = None,
    file_mode: str = "br",
    use_stdin_as_default: bool = False,
) -> Iterable:
    """Lazily load from given file_name.

    Reads from stdin if `use_stdin_as_default` is set and file_name is falsy.

    Args:
        file_name (Path): name of file to load from
        json_format (Optional[utils.JsonFormat], optional): Explicit set format of json file. Defaults to None.
        file_mode (str, optional): mode to open the file in. Defaults to "br".
        use_stdin_as_default (bool, optional): reads from stdin if file_name is None. Defaults to False.

    Returns:
        Iterable: [description]

    Yields:
        Iterator[Iterable]: [description]
    """
    if not file_name:
        if use_stdin_as_default:
            yield from jsonl_iter.load(sys.stdin.buffer)
        else:
            raise ValueError("You can't read from a empty file")
    else:
        _iter = choose_iter(file_name, json_format)

        yield from _iter.load_from_file(file_name, file_mode=file_mode)


def dump(in_iter_, fp: BinaryIO, *, json_format: Optional[utils.JsonFormat] = None):
    _iter = choose_iter(utils.get_name_of_file(fp), json_format)

    _iter.dump(in_iter_, fp)


def dump_to_file(
    in_iter_,
    file_name: Path,
    *,
    json_format: Optional[utils.JsonFormat] = None,
    file_mode: str = "bw",
    use_stdout_as_default: bool = False,
    use_stderr_as_default: bool = False,
):
    """Open file and dump json to it.

    Args:
        in_iter_ (Any): The data to dump.
        file_name (Path): The path to write to
        json_format (Optional[utils.JsonFormat], optional): the json format to write in. Defaults to None.
        file_mode (str, optional): the mode to open the file in. Defaults to "bw".
        use_stdout_as_default (bool, optional): use stdout if file_name is empty. Defaults to False.
        use_stdout_as_default (bool, optional): use stdout if file_name is empty. Defaults to False.
    """
    if not file_name:
        if use_stdout_as_default:
            jsonl_iter.dump(in_iter_, sys.stdout.buffer)
        elif use_stderr_as_default:
            jsonl_iter.dump(in_iter_, sys.stderr.buffer)
        else:
            raise ValueError(f"file_name can't be empty")
    else:
        _iter = choose_iter(file_name, json_format)

        _iter.dump_to_file(in_iter_, file_name, file_mode=file_mode)


def sink(fp: BinaryIO, *, json_format: Optional[utils.JsonFormat] = None):
    _iter = choose_iter(utils.get_name_of_file(fp), json_format)

    return _iter.sink(fp)


def sink_from_file(
    file_name: Path,
    *,
    json_format: Optional[utils.JsonFormat] = None,
    file_mode: str = "bw",
    use_stdout_as_default: bool = False,
    use_stderr_as_default: bool = False,
):
    """Open file and use it as json sink.

    Args:
        in_iter_ (Any): The data to dump.
        file_name (Path): The path to write to
        json_format (Optional[utils.JsonFormat], optional): the json format to write in. Defaults to None.
        file_mode (str, optional): the mode to open the file in. Defaults to "bw".
        use_stdout_as_default (bool, optional): use stdout if file_name is empty. Defaults to False.
        use_stderr_as_default (bool, optional): use stderr if file_name is empty. Defaults to False.
    """
    if not file_name:
        if use_stdout_as_default:
            return jsonl_iter.sink(sys.stdout.buffer)
        elif use_stderr_as_default:
            return jsonl_iter.sink(sys.stderr.buffer)
        else:
            raise ValueError(f"file_name can't be empty")

    _iter = choose_iter(file_name, json_format)

    return _iter.sink_from_file(file_name, file_mode=file_mode)
