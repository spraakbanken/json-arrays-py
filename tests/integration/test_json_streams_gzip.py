import gzip
import json
from pathlib import Path

import json_streams
from json_streams import json_iter, jsonl_iter


def test_jsonl_gzip():
    file = Path("tests/data/objs.jsonl.gz")

    num = 0
    for num, obj in enumerate(json_streams.load_from_file(file)):  # noqa: B007
        assert isinstance(obj, dict)
    assert num == 2


def test_jsonl_gzip_dump_and_load(entries: list[dict]):
    file = Path("tests/data/gen/json_streams_gzip_dump_and_load.jsonl.gz")

    json_streams.dump_to_file(entries, file)

    loaded_entries = list(jsonl_iter.load_from_file(file))

    assert loaded_entries == entries


def test_json_gzip_dump_fp(entries: list[dict]):
    filename = Path("tests/data/gen/json_gzip_dump_fp.json.gz")

    with open(filename, "wb") as fp:
        json_streams.dump(entries, fp)

    with gzip.open(filename) as fp:  # type: ignore
        loaded_entries = json.load(fp)

    assert loaded_entries == entries


def test_json_gzip_load_fp(entries: list[dict]):
    filename = Path("tests/data/gen/json_gzip_load_fp.json.gz")

    with gzip.open(filename, "wt") as fp:
        json.dump(entries, fp)

    with open(filename, "rb") as fp:  # type: ignore
        loaded_entries = list(json_iter.load(fp))  # type: ignore

    assert loaded_entries == entries


def test_jsonl_gzip_sink_and_load(entries: list[dict]):
    file = Path("tests/data/gen/json_streams_gzip_sink_and_load.jsonl.gz")

    with json_streams.sink_from_file(file) as sink:
        for entry in entries:
            sink.send(entry)

    loaded_entries = list(jsonl_iter.load_from_file(file))

    assert loaded_entries == entries
