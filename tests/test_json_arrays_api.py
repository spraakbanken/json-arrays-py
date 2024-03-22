import tempfile

import json_arrays
import pytest
from json_arrays import files


@pytest.mark.parametrize(
    "file_name",
    [
        "tests/data/array.json",
        "tests/data/array.jsonl",
        "tests/data/array.ndjson",
        "tests/data/array.json.gz",
        "tests/data/array.jsonl.gz",
        "tests/data/array.ndjson.gz",
    ],
)
def test_load_from_file(file_name: str, snapshot_json):
    assert list(json_arrays.load_from_file(file_name)) == snapshot_json


@pytest.mark.parametrize(
    "json_format", [json_arrays.JsonFormat.JSON, json_arrays.JsonFormat.JSON_LINES]
)
def test_dump(json_format: json_arrays.JsonFormat, snapshot, array_of_dicts: list[dict]) -> None:
    with tempfile.TemporaryFile() as fp:
        json_arrays.dump(array_of_dicts, fp, json_format=json_format)
        fp.seek(0)
        data_written = fp.read()

    assert data_written == snapshot


@pytest.mark.parametrize(
    "file_name",
    [
        "tests/data/gen/api_array.json",
        "tests/data/gen/api_array.jsonl",
        "tests/data/gen/api_array.ndjson",
        "tests/data/gen/api_array.json.gz",
        "tests/data/gen/api_array.jsonl.gz",
        "tests/data/gen/api_array.ndjson.gz",
    ],
)
def test_dump_to_file(file_name: str, snapshot, array_of_dicts: list[dict]) -> None:
    json_arrays.dump_to_file(array_of_dicts, file_name)

    with files.BinaryFileRead(file_name).file as fp:
        bytes_written = fp.read()
    assert bytes_written == snapshot


@pytest.mark.parametrize(
    "file_name",
    [
        "tests/data/gen/api_array.json",
        "tests/data/gen/api_array.jsonl",
        "tests/data/gen/api_array.ndjson",
        "tests/data/gen/api_array.json.gz",
        "tests/data/gen/api_array.jsonl.gz",
        "tests/data/gen/api_array.ndjson.gz",
    ],
)
def test_sink_from_file(file_name: str, snapshot, array_of_dicts: list[dict]) -> None:
    with json_arrays.sink_from_file(file_name) as sink:
        for obj in array_of_dicts:
            sink.send(obj)

    with files.BinaryFileRead(file_name).file as fp:
        bytes_written = fp.read()
    assert bytes_written == snapshot
