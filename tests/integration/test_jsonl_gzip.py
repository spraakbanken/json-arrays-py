import gzip
import json
from pathlib import Path

from json_streams import jsonl_iter


def test_jsonl_gzip():
    filename = Path("tests/data/objs.jsonl.gz")

    num = 0
    for num, obj in enumerate(jsonl_iter.load_from_file(filename)):  # noqa: B007
        assert isinstance(obj, dict)
    assert num == 2


def test_jsonl_gzip_dump_and_load(entries: list[dict]):
    filename = Path("tests/data/gen/jsonl_gzip_dump_and_load.jsonl.gz")

    jsonl_iter.dump_to_file(entries, filename)

    loaded_entries = list(jsonl_iter.load_from_file(filename))

    assert loaded_entries == entries


def test_jsonl_gzip_dump_fp(entries: list[dict]):
    filename = Path("tests/data/gen/jsonl_gzip_dump_fp.json.gz")

    with open(filename, "wb") as fp:
        jsonl_iter.dump(entries, fp)

    with gzip.open(filename, mode="rt") as fp:  # type: ignore
        loaded_entries = [json.loads(line) for line in fp]

    assert loaded_entries == entries


def test_json_gzip_load_fp(entries: list[dict]):
    filename = Path("tests/data/gen/json_gzip_load_fp.json.gz")

    with gzip.open(filename, "wt") as fp:
        for entry in entries:
            json.dump(entry, fp)
            fp.write("\n")

    with open(filename, "rb") as fp:  # type: ignore
        loaded_entries = list(jsonl_iter.load(fp))  # type: ignore

    assert loaded_entries == entries


def test_jsonl_gzip_sink_and_load(entries: list[dict]):
    filename = Path("tests/data/gen/jsonl_gzip_sink_and_load.jsonl.gz")

    with jsonl_iter.sink_from_file(filename) as sink:
        for entry in entries:
            sink.send(entry)

    loaded_entries = list(jsonl_iter.load_from_file(filename))

    assert loaded_entries == entries


def test_jsonl_gzip_sink_fp(entries: list[dict]):
    filename = Path("tests/data/gen/jsonl_gzip_sink_fp.jsonl.gz")

    with open(filename, mode="wb") as fp:
        with jsonl_iter.sink(fp) as sink:
            for entry in entries:
                sink.send(entry)

    loaded_entries = list(jsonl_iter.load_from_file(filename))

    assert loaded_entries == entries
