import pytest
from json_arrays.utility import is_jsonl


@pytest.mark.parametrize(
    "filename, expected_is_jsonl",
    [
        ("test.json", False),
        ("test.json.gz", False),
        ("test.jsonl", True),
        ("test.jsonl.gz", True),
        ("test.jl", True),
        ("test.jl.gz", True),
        ("test.ndjson", True),
        ("test.ndjson.gz", True),
    ],
)
def test_guess_jsonl(filename: str, expected_is_jsonl: bool) -> None:  # noqa: FBT001
    assert is_jsonl(filename) == expected_is_jsonl
