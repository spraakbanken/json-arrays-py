import io
import json

import pytest

from json_streams import json_iter, jsonl_iter
from .utils import compare_iters


DATA = [
    {"a": 1},
    {"a": 2},
]

JSON_FACIT = b'[\n{"a":1},\n{"a":2}\n]'
JSONL_FACIT = b'{"a":1}\n{"a":2}\n'


def gen_data():
    for i in DATA:
        yield i


@pytest.mark.parametrize(
    "it,data,facit",
    [
        (json_iter, DATA[0], b'{"a":1}'),
        (jsonl_iter, DATA[0], b'{"a":1}\n'),
    ],
)
def test_dump_dict_memoryio(it, data, facit):
    out = io.BytesIO()
    with it.array_sink(out) as sink:
        sink.send(data)

    # assert out.getvalue() == facit
    print(f"out = {out.getvalue()}")

    out.seek(0)
    for i in it.load(out):
        print("i = {i}".format(i=i))
        assert i == data
