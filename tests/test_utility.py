import pytest  # type: ignore

from json_streams.utility import is_jsonl, get_name_of_file


@pytest.mark.parametrize("filename", [
    "test.jsonl",
    "test.jl",
    "test.jsonl.gz",
    "test.jl.gz",
])
def test_filename_is_jsonl(filename: str):
    assert is_jsonl(filename)


@pytest.mark.parametrize("filename", [
    "test.json",
    "test.json.gz",
])
def test_filename_is_not_jsonl(filename: str):
    assert not is_jsonl(filename)


@pytest.mark.parametrize("fp, expected", [(None, "")])
def test_get_name_of_file(fp, expected):
    assert get_name_of_file(fp) == expected
