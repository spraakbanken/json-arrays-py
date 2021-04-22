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
    it.dump(data, out)
    # assert out.getvalue() == facit

    out.seek(0)
    for i in it.load(out):
        print("i = {i}".format(i=i))
        assert i == data


@pytest.mark.parametrize(
    "it,facit",
    [
        (json_iter, JSON_FACIT),
        (jsonl_iter, JSONL_FACIT),
    ],
)
def test_dump_array_memoryio(it, facit):
    out = io.BytesIO()
    it.dump(DATA, out)
    # assert facit == out.getvalue()

    out.seek(0)
    compare_iters(it.load(out), DATA)


@pytest.mark.parametrize(
    "it,facit",
    [
        (json_iter, JSON_FACIT),
        (jsonl_iter, JSONL_FACIT),
    ],
)
def test_dump_gen_memoryio(it, facit):
    out = io.BytesIO()

    it.dump(gen_data(), out)
    # assert facit == out.getvalue()
    out.seek(0)
    compare_iters(it.load(out), gen_data())


@pytest.mark.parametrize(
    "it,file_name,facit,file_mode",
    [
        (json_iter, "tests/data/array.json", None, "rb"),
    ],
)
def test_load_file_name(it, file_name: str, facit, file_mode):
    if not facit:
        facit = file_name
    with open(facit) as fp:
        facit_it = json.load(fp)
    test_it = it.load_from_file(file_name, file_mode=file_mode)
    compare_iters(test_it, facit_it)


@pytest.fixture
def strings():
    return ["a", "b", "c"]


@pytest.fixture
def dicts():
    return [{"a": "a1"}, {"b": ["b1", "b2"]}]


def gen_values(lst):
    for l in lst:
        yield l


@pytest.mark.parametrize(
    "it",
    [
        None,
        "a",
        1,
        {},
        {"a": "test"},
        {"a": "test", "b": {"c": "c1"}},
        {"1": 2},
        ["a", "b"],
    ],
)
def test_json_iter_dumps(it):
    out = io.BytesIO()
    for x in json_iter.dumps(it):
        print(f"x = {x}")
        out.write(x)

    result = json.loads(out.getvalue())

    assert result == it


def test_dumps_gen_strings(strings):
    out = io.BytesIO()
    for x in json_iter.dumps(gen_values(strings)):
        out.write(x)

    result = json.loads(out.getvalue())

    assert result == strings


def test_dumps_gen_list(strings):
    out = io.BytesIO()
    for x in json_iter.dumps(gen_values(strings)):
        out.write(x)

    result = json.loads(out.getvalue())

    assert result == strings


def test_dumps_gen_dict(strings):
    data = {"a": "a", "b": gen_values(strings), "c": "c"}

    out = io.BytesIO()
    for x in json_iter.dumps(data):
        out.write(x)

    result = json.loads(out.getvalue())

    expected = {"a": "a", "b": strings, "c": "c"}
    assert result == expected
