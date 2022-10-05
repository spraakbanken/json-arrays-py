import gzip
import json
from pathlib import Path

import pytest


from json_streams import jsonl_iter


def test_jsonl_gzip():
    file = Path("tests/data/objs.jsonl.gz")

    for num, obj in enumerate(jsonl_iter.load_from_file(file)):
        assert isinstance(obj, dict)
    assert num == 2


@pytest.fixture(name="entries")
def fixture_entries() -> list[dict]:
    return [
        {"a": "b"},
        {"a": {"b": 2}},
    ]


def test_jsonl_gzip_dump_and_load(entries: list[dict]):
    file = Path("tests/data/gen/jsonl_gzip_dump_and_load.jsonl.gz")

    jsonl_iter.dump_to_file(entries, file)

    loaded_entries = list(jsonl_iter.load_from_file(file))

    assert loaded_entries == entries


def test_jsonl_gzip_dump_fp(entries: list[dict]):
    filename = Path("tests/data/gen/jsonl_gzip_dump_fp.json.gz")

    with open(filename, "wb") as fp:
        jsonl_iter.dump(entries, fp)

    with gzip.open(filename, mode="rt") as fp:
        loaded_entries = [json.loads(line) for line in fp]

    assert loaded_entries == entries


def test_json_gzip_load_fp(entries: list[dict]):
    filename = Path("tests/data/gen/json_gzip_load_fp.json.gz")

    with gzip.open(filename, "wt") as fp:
        for entry in entries:
            json.dump(entry, fp)
            fp.write("\n")

    with open(filename, "rb") as fp:
        loaded_entries = list(jsonl_iter.load(fp))

    assert loaded_entries == entries


def test_jsonl_gzip_sink_and_load(entries: list[dict]):
    file = Path("tests/data/gen/jsonl_gzip_sink_and_load.jsonl.gz")

    with jsonl_iter.sink_from_file(file) as sink:
        for entry in entries:
            sink.send(entry)

    loaded_entries = list(jsonl_iter.load_from_file(file))

    assert loaded_entries == entries
