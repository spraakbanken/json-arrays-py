from pathlib import Path

import pytest


from json_streams import json_iter


@pytest.mark.skip()
def test_json_gzip():
    file = Path("tests/data/objs.json.gz")

    for num, obj in enumerate(json_iter.load_from_file(file)):
        assert isinstance(obj, dict)
    assert num == 2


@pytest.fixture(name="entries")
def fixture_entries() -> list[dict]:
    return [
        {"a": "b"},
        {"a": {"b": 2}},
    ]


def test_json_gzip_dump_and_load(entries: list[dict]):
    file = Path("tests/data/gen/json_gzip_dump_and_load.json.gz")

    json_iter.dump_to_file(entries, file)

    loaded_entries = list(json_iter.load_from_file(file))

    assert loaded_entries == entries


def test_json_gzip_sink_and_load(entries: list[dict]):
    file = Path("tests/data/gen/json_gzip_sink_and_load.json.gz")

    with json_iter.sink_from_file(file) as sink:
        for entry in entries:
            sink.send(entry)

    loaded_entries = list(json_iter.load_from_file(file))

    assert loaded_entries == entries
