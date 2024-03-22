import json_arrays
import pytest


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
