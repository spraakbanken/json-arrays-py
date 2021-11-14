import io
import json

import pytest  # type: ignore

from json_streams import json_iter, jsonl_iter
from .utils import compare_iters


DATA = [
    {"a": 1},
    {"a": 2},
]


def gen_data():
    yield from DATA


@pytest.mark.parametrize(
    "it,data",
    [
        (json_iter, DATA[0]),
        (jsonl_iter, DATA[0]),
    ],
)
def test_dump_dict_memoryio(it, data):
    out = io.BytesIO()
    it.dump(data, out)

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
def test_dump_array_memoryio(it):
    out = io.BytesIO()
    it.dump(DATA, out)

    out.seek(0)
    compare_iters(it.load(out), DATA)


@pytest.mark.parametrize(
    "it",
    [
        json_iter,
        jsonl_iter,
    ],
)
def test_dump_gen_memoryio(it):
    out = io.BytesIO()

    it.dump(gen_data(), out)
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
    with open(facit, encoding='utf-8') as fp:
        facit_it = json.load(fp)
    test_it = it.load_from_file(file_name, file_mode=file_mode)
    compare_iters(test_it, facit_it)


@pytest.fixture(name="strings")
def fixture_strings():
    return ["a", "b", "c"]


@pytest.fixture
def dicts():
    return [{"a": "a1"}, {"b": ["b1", "b2"]}]


def gen_values(lst):
    yield from lst


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
