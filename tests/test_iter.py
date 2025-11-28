import io
import json
import typing as t
from collections.abc import Generator, Iterable

import pytest
from syrupy.assertion import SnapshotAssertion

from json_arrays import json_iter, jsonl_iter
from tests.utils import compare_iters

DATA = [
    {"a": 1},
    {"a": 2},
]


def gen_data() -> Generator[dict[str, int], None, None]:
    yield from DATA


@pytest.mark.parametrize(
    "it,data",
    [
        (json_iter, DATA[0]),
        (jsonl_iter, DATA[0]),
    ],
)
def test_dump_dict_memoryio(it: t.Any, data: dict[str, int]) -> None:
    out = io.BytesIO()
    it.dump(data, out)

    out.seek(0)
    for i in it.load(out):
        print(f"i = {i}")  # noqa: T201
        assert i == data


@pytest.mark.parametrize(
    "it",
    [
        json_iter,
        jsonl_iter,
    ],
)
def test_dump_array_memoryio(it: t.Any) -> None:
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
def test_dump_gen_memoryio(it: t.Any) -> None:
    out = io.BytesIO()

    it.dump(gen_data(), out)
    out.seek(0)
    compare_iters(it.load(out), gen_data())


@pytest.mark.parametrize(
    "it, file_name, file_mode", [(json_iter, "tests/data/array.json", "rb")]
)
def test_load_file_name(
    it: t.Any, file_name: str, file_mode: str, snapshot_json: SnapshotAssertion
) -> None:
    assert list(it.load_from_file(file_name, file_mode=file_mode)) == snapshot_json


@pytest.fixture(name="strings")
def fixture_strings() -> list[str]:
    return ["a", "b", "c"]


T = t.TypeVar("T")


def gen_values(lst: Iterable[T]) -> Generator[T, None, None]:
    """Create generator from iterable."""
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
def test_json_iter_dumps(it: t.Any) -> None:
    out = io.BytesIO()
    for x in json_iter.dumps(it):
        print(f"x = {x!r}")  # noqa: T201
        out.write(x)

    result = json.loads(out.getvalue())

    assert result == it


def test_dumps_gen_strings(strings: list[str]) -> None:
    out = io.BytesIO()
    for x in json_iter.dumps(gen_values(strings)):
        out.write(x)

    result = json.loads(out.getvalue())

    assert result == strings


def test_dumps_gen_list(strings: list[str]) -> None:
    out = io.BytesIO()
    for x in json_iter.dumps(gen_values(strings)):
        out.write(x)

    result = json.loads(out.getvalue())

    assert result == strings


def test_dumps_gen_dict(strings: list[str]) -> None:
    data = {"a": "a", "b": gen_values(strings), "c": "c"}

    out = io.BytesIO()
    for x in json_iter.dumps(data):
        out.write(x)

    result = json.loads(out.getvalue())

    expected = {"a": "a", "b": strings, "c": "c"}
    assert result == expected
