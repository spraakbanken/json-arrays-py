"""Handle JSON lazily."""

import typing as t
from collections.abc import Generator, Iterable

import ijson  # type: ignore

from json_arrays import _types, files, jsonlib, shared, utility


def dump(data: dict | Iterable, fileobj: _types.FileWrite, **kwargs: t.Any) -> None:
    """Dump array to a file object.

    Parameters
    ----------
    data : dict | Iterable
        Iterable object to write.
    fileobj : _types.File
        File object to write to. Must be writable.

    """
    fp = files.BinaryFileWrite(fileobj=fileobj)
    writer = shared.JsonArrayWriter()
    for chunk in writer.dumps(data, **kwargs):
        fp.write(chunk)
    fp.close()


def dumps(obj: dict | Iterable, **kwargs: t.Any) -> Iterable[bytes]:
    """Dump array as a iterable of bytes."""
    writer = shared.JsonArrayWriter()
    yield from writer.dumps(obj, **kwargs)


def load(fileobj: _types.FileRead, *, use_float: bool = True, **kwargs: t.Any) -> Iterable:
    """Load an array from a File-like object as an iterator."""
    fp = files.BinaryFileRead(fileobj=fileobj)
    kwargs = {"use_float": use_float} | kwargs
    yield from ijson.items(fp.file, "item", **kwargs)


def load_from_file(
    file_name: _types.Pathlike, *, file_mode: str = "rb", **kwargs: t.Any
) -> Iterable:
    """Load an array from a filename as an iterator."""
    with files.open_file(file_name, file_mode) as fp:
        yield from load(fp, **kwargs)  # type: ignore


def dump_to_file(
    gen: Iterable, file_name: _types.Pathlike, *, file_mode: str = "wb", **kwargs: t.Any
) -> None:
    """Dump an `Iterable` to filename."""
    with files.open_file(file_name, file_mode) as fp:
        return dump(gen, fp, **kwargs)  # type: ignore


def sink(fileobj: _types.FileWrite) -> utility.Sink:
    """Create a writable sink to write a JSON file as a co-routine."""
    fp = files.BinaryFileWrite(fileobj=fileobj)
    return utility.Sink(json_sink(fp, close_file=fp.needs_closing))  # type: ignore


def sink_from_file(file_name: _types.Pathlike, *, file_mode: str = "wb") -> utility.Sink:
    """Create a file and create a co-routine to write JSON to."""
    fp = files.open_file(file_name, file_mode)
    return utility.Sink(json_sink(fp, close_file=True))  # type: ignore


def json_sink(fp: _types.FileWrite, *, close_file: bool = False) -> Generator[None, t.Any, None]:
    """Co-routine for writing JSON."""
    is_first_value = True
    first_value = None
    try:
        while True:
            value = yield
            if is_first_value and first_value:
                fp.write(b"[\n")
                fp.write(jsonlib.dumps(first_value))
                is_first_value = False
                fp.write(b",\n")
                fp.write(jsonlib.dumps(value))
            elif is_first_value:
                first_value = value
            else:
                fp.write(b",\n")
                fp.write(jsonlib.dumps(value))
    except GeneratorExit:
        if is_first_value and first_value:
            fp.write(jsonlib.dumps(first_value))
        else:
            fp.write(b"\n]")
    if close_file:
        fp.close()
