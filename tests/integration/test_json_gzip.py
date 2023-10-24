import gzip
import json
from pathlib import Path

import pytest
from json_streams import json_iter


@pytest.mark.skip()
def test_json_gzip():
    filename = Path("tests/data/objs.json.gz")

    num = 0
    for num, obj in enumerate(json_iter.load_from_file(filename)):  # noqa: B007
        assert isinstance(obj, dict)
    assert num == 2


def test_json_gzip_dump_and_load(entries: list[dict]):
    filename = Path("tests/data/gen/json_gzip_dump_and_load.json.gz")

    json_iter.dump_to_file(entries, filename)

    loaded_entries = list(json_iter.load_from_file(filename))

    assert loaded_entries == entries


def test_json_gzip_dump_fp(entries: list[dict]):
    filename = Path("tests/data/gen/json_gzip_dump_fp.json.gz")

    with open(filename, "wb") as fp:
        json_iter.dump(entries, fp)

    with gzip.open(filename) as fp:  # type: ignore
        loaded_entries = json.load(fp)

    assert loaded_entries == entries


def test_json_gzip_load_fp(entries: list[dict]):
    filename = Path("tests/data/gen/json_gzip_load_fp.json.gz")

    with gzip.open(filename, "wt") as fp:
        json.dump(entries, fp)

    with open(filename, "br") as fp:  # type: ignore
        loaded_entries = list(json_iter.load(fp))  # type: ignore

    assert loaded_entries == entries


def test_json_gzip_sink_and_load(entries: list[dict]):
    filename = Path("tests/data/gen/json_gzip_sink_and_load.json.gz")

    with json_iter.sink_from_file(filename) as sink:
        for entry in entries:
            sink.send(entry)

    loaded_entries = list(json_iter.load_from_file(filename))

    assert loaded_entries == entries


def test_json_gzip_sink_fp(entries: list[dict]):
    filename = Path("tests/data/gen/json_gzip_sink_fp.json.gz")

    with open(filename, mode="wb") as fp:
        with json_iter.sink(fp) as sink:
            for entry in entries:  # sourcery skip: no-loop-in-tests
                sink.send(entry)

    loaded_entries = list(json_iter.load_from_file(filename))

    assert loaded_entries == entries
