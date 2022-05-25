from pathlib import Path

import pytest


import json_streams
from json_streams import jsonl_iter


def test_jsonl_gzip():
    file = Path("tests/data/objs.jsonl.gz")

    for num, obj in enumerate(json_streams.load_from_file(file)):
        assert isinstance(obj, dict)
    assert num == 2


@pytest.fixture(name="entries")
def fixture_entries() -> list[dict]:
    return [
        {"a": "b"},
        {"a": {"b": 2}},
    ]


def test_jsonl_gzip_dump_and_load(entries: list[dict]):
    file = Path("tests/data/gen/json_streams_gzip_dump_and_load.jsonl.gz")

    json_streams.dump_to_file(entries, file)

    loaded_entries = list(jsonl_iter.load_from_file(file))

    assert loaded_entries == entries


def test_jsonl_gzip_sink_and_load(entries: list[dict]):
    file = Path("tests/data/gen/json_streams_gzip_sink_and_load.jsonl.gz")

    with json_streams.sink_from_file(file) as sink:
        for entry in entries:
            sink.send(entry)

    loaded_entries = list(jsonl_iter.load_from_file(file))

    assert loaded_entries == entries
