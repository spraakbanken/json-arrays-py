"""Handle JSON-LINES lazily."""

import contextlib
import typing as t
from collections.abc import Generator, Iterable

from json_arrays import _types, files, jsonlib, shared, utility


def dump(data: dict | Iterable, fileobj: _types.FileWrite, **kwargs: t.Any) -> None:
    """Serialize the given data to JSON in Json Lines format."""
    fp = files.BinaryFileWrite(fileobj=fileobj)
    writer = shared.JsonArrayWriter(json_lines=True)
    did_write = False
    for chunk in writer.dumps(data, **kwargs):
        fp.write(chunk)
        did_write = True
    if did_write:
        fp.write(b"\n")
    fp.close()


def load(fileobj: _types.FileRead, **kwargs: t.Any) -> Iterable:
    """Load from a JSON file as an iterable."""
    fp = files.BinaryFileRead(fileobj=fileobj)
    for line in fp.file:
        yield jsonlib.loads(line, **kwargs)


def load_from_file(
    file_name: _types.Pathlike, *, file_mode: t.Literal["rb"] = "rb", **kwargs: t.Any
) -> Iterable:
    """Open a file and load JSON from the file."""
    with files.open_file(file_name, file_mode) as fp:
        yield from load(fp, **kwargs)


def dump_to_file(
    obj: t.Any,
    file_name: _types.Pathlike,
    *,
    file_mode: t.Literal["wb", "ab", "xb"] = "wb",
    **kwargs: t.Any,
) -> None:
    """Create a file and write JSON to the file."""
    with files.open_file(file_name, file_mode) as fp:
        dump(obj, fp, **kwargs)


def sink(fileobj: _types.FileWrite) -> utility.Sink:
    """Create a writeable sink from a file to write Json Lines."""
    fp = t.cast(_types.FileWrite, files.BinaryFileWrite(fileobj=fileobj))
    return utility.Sink(jsonl_sink(fp, close_file=False))


def sink_from_file(
    file_name: _types.Pathlike, *, file_mode: t.Literal["wb", "ab", "xb"] = "wb"
) -> utility.Sink:
    """Create a writeable sink from a filename to write Json Lines."""
    fp = t.cast(_types.FileWrite, files.open_file(file_name, file_mode))

    return utility.Sink(jsonl_sink(fp, close_file=True))


def jsonl_sink(
    fp: _types.FileWrite, *, close_file: bool = False
) -> Generator[None, t.Any, None]:
    """Co-routine to write Json Lines file."""
    with contextlib.suppress(GeneratorExit):
        while True:
            value = yield
            fp.write(jsonlib.dumps(value))
            fp.write(b"\n")
    if close_file:
        fp.close()
