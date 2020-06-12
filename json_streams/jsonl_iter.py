from typing import Dict
from typing import BinaryIO
from typing import Iterable
from typing import Union

import codecs
import io

from json_streams import jsonlib
from json_streams.utils import to_bytes


def dump(data: Union[Dict, Iterable], fp: BinaryIO):

    if isinstance(data, dict):
        fp.write(to_bytes(jsonlib.dumps(data)))
        fp.write(b"\n")
        return

    try:
        for obj in data:
            fp.write(to_bytes(jsonlib.dumps(obj)))
            fp.write(b"\n")
    except TypeError:
        fp.write(to_bytes(jsonlib.dumps(data)))
        fp.write(b"\n")


def load(fp: BinaryIO) -> Iterable:
    for line in fp:
        yield jsonlib.loads(line)


def load_from_file(file_name: str, *, file_mode: str = None):
    if not file_mode:
        file_mode = "br"
    with open(file_name, "br") as fp:
        yield from load(fp)


def dump_to_file(obj, file_name, *, file_mode: str = None):
    if not file_mode:
        file_mode = "bw"
    with open(file_name, "bw") as fp:
        dump(obj, fp)
