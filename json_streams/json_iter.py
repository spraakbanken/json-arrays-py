""" Handle JSON lazily. """
from pathlib import Path
from typing import Dict
from typing import BinaryIO
from typing import Iterable
from typing import Optional, Union

import ijson

from json_streams import jsonlib
from json_streams import utils
from json_streams.utils import to_bytes


def dump(data: Union[Dict, Iterable], fp: BinaryIO):
    """Dump array to a file object.

    Parameters
    ----------
    fp :
        File object to write to. Must be writable.
    data :
        Iterable object to write.
    """

    if isinstance(data, dict):
        fp.write(to_bytes(jsonlib.dumps(data)))
        return

    try:
        it = iter(data)
    except TypeError:
        fp.write(to_bytes(jsonlib.dumps(data)))
        return

    fp.write(b"[\n")
    try:
        obj = next(it)
        fp.write(to_bytes(jsonlib.dumps(obj)))
    except StopIteration:
        pass
    else:
        for v in it:
            fp.write(b",\n")
            fp.write(to_bytes(jsonlib.dumps(v)))
    fp.write(b"\n]")


def dumps(obj) -> Iterable[bytes]:
    if isinstance(obj, str):
        yield to_bytes(jsonlib.dumps(obj))
        return
    elif isinstance(obj, dict):
        yield b"{"
        for i, (key, value) in enumerate(obj.items()):
            if i > 0:
                yield b","
            yield b'"%s":' % to_bytes(key)
            yield from dumps(value)
        yield b"}"
        return
    try:
        it = iter(obj)
    except TypeError:
        yield to_bytes(jsonlib.dumps(obj))
        return

    yield b"["
    for i, o in enumerate(it):
        if i > 0:
            yield b","
        yield to_bytes(jsonlib.dumps(o))

    yield b"]"


def load(fp: BinaryIO) -> Iterable:
    yield from ijson.items(fp, "item")


def load_eager(fp: BinaryIO):
    data = jsonlib.loads(fp.read())
    if isinstance(data, list):
        yield from data
    else:
        return data


def load_from_file(file_name: Path, *, file_mode: Optional[str] = None):
    if not file_mode:
        file_mode = "br"

    assert "b" in file_mode
    with open(file_name, file_mode) as fp:
        yield from load(fp)


def dump_to_file(gen: Iterable, file_name: Path, *, file_mode: str = None):
    if not file_mode:
        file_mode = "bw"
    assert "b" in file_mode
    with open(file_name, file_mode) as fp:
        return dump(gen, fp)


def sink(fp: BinaryIO):
    return utils.Sink(json_sink(fp))


def sink_from_file(file_name: Path, *, file_mode: str = None):
    if not file_mode:
        file_mode = "bw"
    assert "b" in file_mode
    fp = open(file_name, file_mode)
    return utils.Sink(json_sink(fp, close_file=True))


def json_sink(fp: BinaryIO, *, close_file: bool = False):
    is_first_value = True
    first_value = None
    try:
        while True:
            value = yield
            if is_first_value and first_value:
                fp.write(b"[\n")
                fp.write(to_bytes(jsonlib.dumps(first_value)))
                is_first_value = False
                fp.write(b",\n")
                fp.write(to_bytes(jsonlib.dumps(value)))
            elif is_first_value:
                first_value = value
            else:
                fp.write(b",\n")
                fp.write(to_bytes(jsonlib.dumps(value)))
    except GeneratorExit:
        if is_first_value and first_value:
            fp.write(to_bytes(jsonlib.dumps(first_value)))
        else:
            fp.write(b"\n]")
    if close_file:
        fp.close()
