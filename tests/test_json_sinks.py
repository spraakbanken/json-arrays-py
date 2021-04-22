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
    "it,data",
    [
        (json_iter, DATA[0]),
        (jsonl_iter, DATA[0]),
    ],
)
def test_dict_to_sink_memoryio(it, data):
    out = io.BytesIO()
    with it.sink(out) as sink:
        sink.send(data)

    # assert out.getvalue() == facit
    print(f"out = {out.getvalue()}")

    out.seek(0)
    for i in it.load(out):
        print("i = {i}".format(i=i))
        assert i == data


@pytest.mark.parametrize(
    "it",
    [
        json_iter,
        jsonl_iter,
    ],
)
def test_array_to_sink_memoryio(it):
    out = io.BytesIO()
    with it.sink(out) as sink:
        for data in DATA:
            sink.send(data)
    # assert facit == out.getvalue()

    print(f"out = {out.getvalue()}")
    out.seek(0)
    compare_iters(it.load(out), DATA)
