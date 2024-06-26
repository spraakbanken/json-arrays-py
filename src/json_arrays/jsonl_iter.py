"""Handle JSON-LINES lazily."""

import contextlib
from typing import Iterable, Union

from json_arrays import _types, files, jsonlib, shared, utility


def dump(data: Union[dict, Iterable], fileobj: _types.File, **kwargs):
    fp = files.BinaryFileWrite(fileobj=fileobj)
    writer = shared.JsonArrayWriter(json_lines=True)
    did_write = False
    for chunk in writer.dumps(data, **kwargs):
        fp.write(chunk)
        did_write = True
    if did_write:
        fp.write(b"\n")
    fp.close()


def load(fileobj: _types.File, **kwargs) -> Iterable:
    fp = files.BinaryFileRead(fileobj=fileobj)
    for line in fp.file:
        yield jsonlib.loads(line, **kwargs)


def load_from_file(file_name: _types.Pathlike, *, file_mode: str = "rb", **kwargs):
    with files.open_file(file_name, file_mode) as fp:
        yield from load(fp, **kwargs)  # type: ignore


def dump_to_file(obj, file_name: _types.Pathlike, *, file_mode: str = "wb", **kwargs):
    with files.open_file(file_name, file_mode) as fp:
        dump(obj, fp, **kwargs)  # type: ignore


def sink(fileobj: _types.File):
    fp = files.BinaryFileWrite(fileobj=fileobj)
    return utility.Sink(jsonl_sink(fp, close_file=fp.needs_closing))  # type: ignore


def sink_from_file(file_name: _types.Pathlike, *, file_mode: str = "wb"):
    fp = files.open_file(file_name, file_mode)

    return utility.Sink(jsonl_sink(fp, close_file=True))  # type: ignore


def jsonl_sink(fp: _types.File, *, close_file: bool = False):
    with contextlib.suppress(GeneratorExit):
        while True:
            value = yield
            fp.write(jsonlib.dumps(value))
            fp.write(b"\n")
    if close_file:
        fp.close()
