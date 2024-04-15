import pytest
from json_arrays.utility import get_name_of_file, is_bzip2, is_gzip, is_jsonl


@pytest.mark.parametrize(
    "filename",
    [
        "test.jsonl",
        "test.jl",
        "test.ndjson",
        "test.jsonl.gz",
        "test.jl.gz",
        "test.ndjson.gz",
        "test.jsonl.bz2",
        "test.jl.bz2",
        "test.ndjson.bz2",
    ],
)
def test_filename_is_jsonl(filename: str):
    assert is_jsonl(filename)


@pytest.mark.parametrize(
    "filename",
    ["test.json.gz", "test.jsonl.gz", "test.jl.gz", "test.ndjson.gz"],
)
def test_filename_is_gzip(filename: str):
    assert is_gzip(filename)


@pytest.mark.parametrize(
    "filename",
    ["test.json.bz2", "test.jsonl.bz2", "test.jl.bz2", "test.ndjson.bz2"],
)
def test_filename_is_bzip2(filename: str):
    assert is_bzip2(filename)


@pytest.mark.parametrize(
    "filename",
    [
        "test.json",
        "test.json.gz",
    ],
)
def test_filename_is_not_jsonl(filename: str):
    assert not is_jsonl(filename)


@pytest.mark.parametrize(
    "filename",
    ["test.json", "test.jsonl", "test.jl", "test.ndjson"],
)
def test_filename_is_not_gzip(filename: str):
    assert not is_gzip(filename)


@pytest.mark.parametrize(
    "filename",
    ["test.json", "test.jsonl", "test.jl", "test.ndjson"],
)
def test_filename_is_not_bzip2(filename: str):
    assert not is_bzip2(filename)


@pytest.mark.parametrize("fp, expected", [(None, "")])
def test_get_name_of_file(fp, expected):
    assert get_name_of_file(fp) == expected
