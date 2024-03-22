import json_arrays
import pytest


@pytest.mark.parametrize(
    "file_name",
    [
        "tests/data/array.json",
        "tests/data/array.jsonl",
        "tests/data/array.ndjson",
        "tests/data/array.json.gz",
        "tests/data/objs.jsonl.gz",
    ],
)
def test_load_file_name(file_name: str, snapshot_json):
    assert list(json_arrays.load_from_file(file_name)) == snapshot_json
